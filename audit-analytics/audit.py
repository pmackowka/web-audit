"""Pasywny audyt wdrożenia analityki i prywatności na stronie WWW.

Uruchomienie:
    uv run audit.py <url> --slug <firma> [--mask "Jan Kowalski" --mask jan@example.com]

Trzy przebiegi tej samej strony, każdy w świeżym kontekście przeglądarki:
    A – bez interakcji z banerem zgód,
    B – po kliknięciu „odrzuć / tylko niezbędne”,
    C – po kliknięciu „akceptuj wszystkie”.
B i C są pomijane, gdy w przebiegu A nie znaleziono odpowiedniego przycisku.

Wynik: reports/RRRR-MM-DD-<firma>/ z RAPORT.md (szkic z tabelami), screenshots/ (plansze dowodowe) i raw/.
Sekcje „Podsumowanie” i „Wnioski” uzupełnia człowiek albo Claude wg CLAUDE.md.
"""

import argparse
import base64
import datetime as dt
import json
import re
import shutil
import string
import time
import zlib
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

from evidence import render_evidence

ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"  # raporty obok kodu modułu
VIEWPORT = {"width": 1440, "height": 900}

# Znane CMP: (nazwa, selektor „odrzuć”, selektor „akceptuj”).
KNOWN_CMPS = [
    ("OneTrust", "#onetrust-reject-all-handler", "#onetrust-accept-btn-handler"),
    ("Cookiebot", "#CybotCookiebotDialogBodyButtonDecline", "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"),
    ("CookieYes", ".cky-btn-reject", ".cky-btn-accept"),
    ("Didomi", "#didomi-notice-disagree-button", "#didomi-notice-agree-button"),
]

# Rozpoznawanie przycisków po tekście, gdy CMP nie jest znane.
REJECT_RE = re.compile(r"odrzu|tylko (niezb|wymagan|konieczn)|niezbędne|odmawiam|nie zgadzam|reject|decline|deny|necessary only|only necessary", re.I)
ACCEPT_RE = re.compile(r"akceptuj|zaakceptuj|zgadzam się|zgoda na wszystk|zezwól|przyjmuj|accept|allow all|agree|ok, rozumiem", re.I)
# Nigdy nie klikamy przycisków, które mogą rozpocząć proces, wysłać formularz albo zużyć link.
FORBIDDEN_RE = re.compile(r"rozpocz|start|zacznij|wyślij|wysyłam|submit|zaloguj|login|log in|sign|zarejestr|kup|zamów|zapłać|dalej|next|test|regulamin|warunk|terms|kontynuuj|continue", re.I)
# Kontener przycisku musi wyglądać na baner cookies (samo „RODO”/„zgoda” nie wystarcza — to bywa formularz).
BANNER_TEXT_RE = r"cookie|ciasteczk|consent"

# Rozpoznawanie narzędzi po URL żądania: (wzorzec, narzędzie, firma, kategoria). Kolejność ma znaczenie.
TOOLS = [
    (r"googletagmanager\.com/gtm\.js", "Google Tag Manager", "Google", "tag-manager"),
    (r"googletagmanager\.com/gtag/js", "Google tag (gtag.js)", "Google", "tag-manager"),
    (r"/g/collect", "Google Analytics 4", "Google", "analytics"),
    (r"google-analytics\.com|analytics\.google\.com", "Google Analytics", "Google", "analytics"),
    (r"recaptcha", "reCAPTCHA", "Google", "security"),
    (r"googleadservices\.com|googleads\.g\.doubleclick\.net|/pagead/|google\.[a-z.]+/ccm/", "Google Ads", "Google", "ads"),
    (r"doubleclick\.net", "Google DoubleClick / Floodlight", "Google", "ads"),
    (r"connect\.facebook\.net|facebook\.com/tr", "Meta Pixel", "Meta", "ads"),
    (r"analytics\.tiktok\.com", "TikTok Pixel", "TikTok", "ads"),
    (r"snap\.licdn\.com|px\.ads\.linkedin\.com|linkedin\.com/(px|collect)", "LinkedIn Insight Tag", "LinkedIn", "ads"),
    (r"hotjar\.(com|io)", "Hotjar", "Hotjar / Contentsquare", "analytics"),
    (r"clarity\.ms", "Microsoft Clarity", "Microsoft", "analytics"),
    (r"bat\.bing\.com", "Microsoft Advertising UET", "Microsoft", "ads"),
    (r"browser-intake-datadoghq[^/]*/api/v2/replay", "Datadog Session Replay", "Datadog", "analytics"),
    (r"browser-intake-datadoghq|datadoghq-browser-agent\.com", "Datadog RUM / Logs", "Datadog", "monitoring"),
    (r"sentry\.io|sentry-cdn\.com", "Sentry", "Sentry", "monitoring"),
    (r"cookielaw\.org|onetrust\.com", "OneTrust", "OneTrust", "cmp"),
    (r"cookiebot\.com", "Cookiebot", "Usercentrics", "cmp"),
    (r"cookieyes\.com", "CookieYes", "CookieYes", "cmp"),
    (r"privacy-center\.org|didomi\.io", "Didomi", "Didomi", "cmp"),
    (r"usercentrics\.eu", "Usercentrics", "Usercentrics", "cmp"),
    (r"criteo\.(com|net)", "Criteo", "Criteo", "ads"),
    (r"hubspot|hs-scripts\.com|hs-analytics\.net|hsforms", "HubSpot", "HubSpot", "marketing"),
    (r"intercom", "Intercom", "Intercom", "marketing"),
    (r"amplitude\.com", "Amplitude", "Amplitude", "analytics"),
    (r"mixpanel\.com", "Mixpanel", "Mixpanel", "analytics"),
    (r"segment\.(com|io)", "Segment", "Twilio", "analytics"),
    (r"youtube\.com|ytimg\.com", "YouTube", "Google", "embed"),
    (r"fonts\.(googleapis|gstatic)\.com", "Google Fonts", "Google", "cdn"),
    (r"gstatic\.com|googleapis\.com", "Google (CDN/API)", "Google", "cdn"),
    (r"cloudflare|cdnjs|jsdelivr|unpkg", "CDN", "—", "cdn"),
]
TRACKING = {"analytics", "ads", "marketing", "monitoring", "tag-manager"}

# Ciasteczka → narzędzie (heurystyka po nazwie).
COOKIE_TOOLS = [
    (r"^_ga($|_)", "Google Analytics 4"), (r"^_gid$|^_gat", "Google Analytics"),
    (r"^_gcl_", "Google Ads (Conversion Linker)"), (r"^(IDE|test_cookie|DSID)$", "Google DoubleClick"),
    (r"^(NID|AEC|SOCS|CONSENT)$", "Google"), (r"^_fb[pc]$|^fr$", "Meta"), (r"^_tt|^ttwid", "TikTok"),
    (r"^(li_|bcookie|lidc|bscookie|UserMatchHistory|AnalyticsSyncHistory)", "LinkedIn"), (r"^_hj", "Hotjar"),
    (r"^_cl(ck|sk)$|^(CLID|ANONCHK|MUID)$", "Microsoft Clarity / Bing"), (r"^_uet", "Microsoft Advertising"),
    (r"^_dd_s$", "Datadog RUM"), (r"^Optanon", "OneTrust"), (r"^CookieConsent$", "Cookiebot"),
    (r"^cookieyes", "CookieYes"), (r"^didomi", "Didomi"), (r"^euconsent", "IAB TCF"),
    (r"^__cf|^cf_", "Cloudflare"), (r"^_hs|^hubspot", "HubSpot"),
]

# E-mail: TLD z liter, bez plików typu logo@2x.webp i wersji pakietów typu rum@5.23.3.
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.(?!(?:png|jpe?g|webp|gif|svg|avif|js|css)\b)[A-Za-z]{2,}\b")
JWT_RE = re.compile(r"eyJ[\w-]+\.eyJ[\w-]+\.[\w-]+")  # tokeny dostępowe (JWT)
# Telefon: z separatorami albo z prefiksem +48/0048 bez separatorów (gołe 9 cyfr to częściej ID niż telefon).
PHONE_RE = re.compile(r"(?<![\d.])(?:(?:\+?48[\s-]?)?\d{3}[\s-]\d{3}[\s-]\d{3}|(?:\+|00)48\d{9})(?![\d.])")
GA4_STANDARD = ["tid", "cid", "sid", "sct", "seg", "dl", "dr", "dt", "en", "gcs", "gcd", "npa", "dma", "_ss", "_fv", "_nsi"]

# Serializacja dataLayer: obiekty Arguments z gtag() → tablice, bez cykli i elementów DOM.
DATALAYER_JS = """() => {
  const seen = new WeakSet();
  const rep = (k, v) => {
    if (typeof v === 'function') return '[Function]';
    if (v && typeof v === 'object') {
      if (v === window) return '[Window]';
      if (typeof Element !== 'undefined' && v instanceof Element) return '[Element]';
      if (Object.prototype.toString.call(v) === '[object Arguments]') v = Array.from(v);
      if (seen.has(v)) return '[Circular]';
      seen.add(v);
    }
    return v;
  };
  try { return JSON.parse(JSON.stringify(window.dataLayer ?? null, rep)); }
  catch (e) { return {error: String(e)}; }
}"""

GLOBALS_JS = """() => ({
  gtm_keys: Object.keys(window.google_tag_manager || {}),
  onetrust: !!window.OneTrust, cookiebot: !!window.Cookiebot, didomi: !!window.Didomi,
  cookieyes: !!document.querySelector('.cky-consent-container'),
  tcf: typeof window.__tcfapi === 'function', datadog_rum: !!window.DD_RUM, datadog_logs: !!window.DD_LOGS,
  fbq: typeof window.fbq === 'function', ttq: !!window.ttq, hj: typeof window.hj === 'function',
  clarity: typeof window.clarity === 'function'
})"""

STORAGE_JS = """() => {
  const dump = s => { try { return Object.assign({}, s); } catch (e) { return {error: String(e)}; } };
  return {localStorage: dump(window.localStorage), sessionStorage: dump(window.sessionStorage)};
}"""

PRIVACY_LINKS_JS = """() => Array.from(document.querySelectorAll('a[href]'))
  .map(a => ({text: (a.innerText || a.getAttribute('aria-label') || '').trim().slice(0, 80), href: a.href}))
  .filter(l => /prywatno|privacy|cookie|rodo|gdpr|dane osobowe|polityk/i.test(l.text + ' ' + l.href))"""

# Kontener banera = najbliższy przodek fixed/sticky. Przycisk w formularzu albo typu submit → null (nie klikamy).
BANNER_OF_JS = """el => {
  if (el.closest('form') || (el.getAttribute('type') || '').toLowerCase() === 'submit') return null;
  let n = el;
  while (n && n !== document.body) {
    const p = getComputedStyle(n).position;
    if (p === 'fixed' || p === 'sticky') return n;
    n = n.parentElement;
  }
  return null;
}"""

# Wysokość liczona raz i maks. 40 kroków — infinite scroll nie zawiesi przebiegu.
SCROLL_JS = """async () => {
  const h = document.body.scrollHeight;
  for (let y = 0, i = 0; y < h && i < 40; y += 600, i++) {
    window.scrollTo(0, y); await new Promise(r => setTimeout(r, 250));
  }
  window.scrollTo(0, h);
}"""


# ---------- maskowanie ----------

def is_token(c: str) -> bool:
    """Token = ≥8 znaków, cyfra, bez spacji; slug typu „buty-nike-air-max-90-123456” (≥2 słowa) to nie token."""
    if len(c) < 8 or not re.search(r"\d", c) or not re.fullmatch(r"[\w.~+/=-]+", c):
        return False
    return sum(1 for w in c.split("-") if w.isalpha() and len(w) >= 3) < 2


def find_secrets(url: str, extra: list[str]) -> list[str]:
    """Tokeny z URL (ścieżka, wartości query, fragment #…) + dane podane przez --mask."""
    parts = urlsplit(url)
    values = [q.split("=", 1)[1] for q in parts.query.split("&") if "=" in q]  # bez parse_qsl: „+” w base64 zostaje
    candidates = parts.path.split("/") + [unquote(v) for v in values] + re.split(r"[/?&=#]", parts.fragment)
    found = [c for c in candidates if is_token(c)]
    return sorted(set(found + [e for e in extra if e]), key=len, reverse=True)


def secret_re(s: str) -> re.Pattern:
    """Wielkość liter bez znaczenia, spacja w --mask pasuje też do „+” i wielu spacji (Jan+Kowalski)."""
    return re.compile(r"[\s+]+".join(map(re.escape, s.split())), re.I)


def make_masker(secrets: list[str]):
    patterns = [(secret_re(s), re.sub(r"\s", "", s)[:4] + "…") for s in secrets if s.strip()]

    def mask(text) -> str:
        text = unquote(unquote("" if text is None else str(text)))  # %40, %20 itd. → postać jawna
        for rx, repl in patterns:
            text = rx.sub(repl, text)
        text = JWT_RE.sub("eyJ…(JWT)", text)
        text = EMAIL_RE.sub(lambda m: m.group()[:2] + "…@" + m.group().split("@")[1], text)
        return PHONE_RE.sub(lambda m: m.group()[:3] + "…", text)
    return mask


# ---------- przechwytywanie ----------

def decode_body(buf: bytes | None) -> str | None:
    """Body POST jako tekst; skompresowane (np. Datadog) próbujemy rozpakować."""
    if not buf:
        return None
    try:
        return buf.decode("utf-8")
    except UnicodeDecodeError:
        pass
    for wbits in (15, -15, 31):
        try:
            return "[zdekompresowane] " + zlib.decompress(buf, wbits).decode("utf-8", "replace")
        except zlib.error:
            continue
    return "[binarne, base64] " + base64.b64encode(buf).decode()


def find_consent_buttons(page) -> dict:
    """Szuka przycisków „odrzuć” i „akceptuj” banera zgód, niczego nie klika."""
    result = {"cmp": None, "reject": None, "accept": None}
    for frame in page.frames:
        for name, reject_sel, accept_sel in KNOWN_CMPS:
            for kind, sel in (("reject", reject_sel), ("accept", accept_sel)):
                loc = frame.locator(sel).first
                try:
                    if not result[kind] and loc.is_visible():
                        result[kind] = {"locator": loc, "text": loc.inner_text().strip()[:60], "how": f"{name}: {sel}"}
                        result["cmp"] = name
                except Exception:
                    continue
    # Fallback: przyciski po tekście, tylko w kontenerze wyglądającym na baner zgód.
    for frame in page.frames:
        for kind, rx in (("reject", REJECT_RE), ("accept", ACCEPT_RE)):
            if result[kind]:
                continue
            try:
                candidates = frame.get_by_role("button").all() + frame.locator("a[role=button], [class*=cookie] a").all()
            except Exception:
                continue
            for loc in candidates:
                try:
                    text = (loc.inner_text(timeout=1000) or "").strip()
                    if not text or len(text) > 60 or not rx.search(text) or FORBIDDEN_RE.search(text):
                        continue
                    if kind == "accept" and REJECT_RE.search(text):
                        continue
                    if not loc.is_visible():
                        continue
                    banner = loc.evaluate_handle(BANNER_OF_JS).as_element()
                    if banner is None or not re.search(BANNER_TEXT_RE, banner.inner_text(), re.I):
                        continue
                    result[kind] = {"locator": loc, "text": text, "how": "tekst przycisku"}
                    break
                except Exception:
                    continue
    return result


def wait_idle(page, extra_s: float):
    try:
        page.wait_for_load_state("networkidle", timeout=30_000)
    except PWTimeout:
        pass
    page.wait_for_timeout(extra_s * 1000)


def shot(page, path: Path, mask_texts: list[str]):
    """Zrzut widoku z zamaskowanymi elementami zawierającymi dane osobowe/tokeny."""
    try:
        page.screenshot(path=path, mask=[page.get_by_text(t) for t in mask_texts if t])
    except Exception as e:
        print(f"  ! zrzut {path.name} nieudany: {e}")


def safe_eval(page, js):
    """evaluate odporny na nawigację (np. CMP przeładowuje stronę po kliknięciu)."""
    try:
        return page.evaluate(js)
    except Exception:
        try:
            page.wait_for_load_state("load", timeout=30_000)
            return page.evaluate(js)
        except Exception as e:
            print(f"  ! evaluate nieudany: {type(e).__name__}")
            return None


def run_pass(browser, url: str, mode: str, out: Path, mask_texts: list[str], extra_urls: list[str]) -> dict:
    raw = out / "raw" / mode
    raw.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(locale="pl-PL", viewport=VIEWPORT, record_har_path=raw / "network.har",
                                  record_har_content="embed")
    t0 = time.monotonic()
    phase = ["przed"]
    requests = []

    def on_request(req):
        if not req.url.startswith("http"):  # data:, blob: — nie opuszczają przeglądarki
            return
        requests.append({
            "t": round(time.monotonic() - t0, 3), "phase": phase[0], "method": req.method,
            "host": urlsplit(req.url).hostname, "url": req.url, "type": req.resource_type,
            "referer": req.headers.get("referer"), "post_body": decode_body(req.post_data_buffer),
        })

    context.on("request", on_request)
    page = context.new_page()
    res = {"mode": mode, "final_url": url, "click": None, "buttons": {"reject": None, "accept": None}, "cmp_ui": None,
           "datalayer": [], "globals": {}, "storage": {}, "cookies": [], "requests": requests, "errors": []}
    try:
        _run_steps(page, context, url, mode, raw, mask_texts, extra_urls, res, phase)
    finally:  # dane częściowe i HAR zapisują się także po błędzie
        try:
            res["cookies"] = context.cookies()
        except Exception:
            pass
        context.close()
        for name in ("requests", "cookies", "storage", "datalayer"):
            (raw / f"{name}.json").write_text(json.dumps(res[name], ensure_ascii=False, indent=2))
        (raw / "pass.json").write_text(json.dumps({k: v for k, v in res.items() if k not in ("requests", "cookies", "storage", "datalayer")}, ensure_ascii=False, indent=2))
    return res


def _run_steps(page, context, url, mode, raw, mask_texts, extra_urls, res, phase):
    page.goto(url, wait_until="load", timeout=60_000)
    wait_idle(page, 8)
    res["final_url"] = page.url
    if mode == "A":  # jeden zrzut strony — tło planszy kontekstowej 00-strona.png
        shot(page, raw / "page.png", mask_texts)
    buttons = find_consent_buttons(page)
    res["cmp_ui"] = buttons["cmp"]
    res["buttons"] = {k: (buttons[k]["text"] + f" ({buttons[k]['how']})") if buttons[k] else None
                      for k in ("reject", "accept")}

    target = {"B": "reject", "C": "accept"}.get(mode)
    if target and buttons[target]:
        phase[0] = "po"
        buttons[target]["locator"].click(timeout=5000)
        res["click"] = buttons[target]["text"]
        wait_idle(page, 4)  # po kliknięciu CMP bywa przeładowuje stronę — safe_eval to obsługuje

    safe_eval(page, SCROLL_JS)
    page.wait_for_timeout(4000)

    res["datalayer"] = [{"url": page.url, "datalayer": safe_eval(page, DATALAYER_JS)}]  # dataLayer znika po nawigacji
    res["globals"] = safe_eval(page, GLOBALS_JS) or {}
    if mode == "A":
        res["privacy"] = check_privacy(page, context, mask_texts)
    # Kolejne strony (np. kategoria, produkt) w tym samym kontekście — jak wpisanie adresu przez odwiedzającego.
    for extra in extra_urls:
        try:
            page.goto(extra, wait_until="load", timeout=60_000)
            wait_idle(page, 8)
            safe_eval(page, SCROLL_JS)
            page.wait_for_timeout(4000)
            res["datalayer"].append({"url": page.url, "datalayer": safe_eval(page, DATALAYER_JS)})
        except Exception as e:
            res["errors"].append(f"{extra}: {type(e).__name__}")
    res["storage"] = safe_eval(page, STORAGE_JS) or {}


# Linki, których nie otwieramy nawet GET-em: mogą zmienić stan albo zużyć jednorazowy link.
UNSAFE_LINK_RE = re.compile(r"withdraw|wycofa|revoke|usu[nń]|delete|remove|unsubscribe|wypisz|logout|wyloguj|token|confirm|potwierd", re.I)


def check_privacy(page, context, secrets: list[str]) -> dict:
    """Linki do polityki prywatności/cookies + czy się otwierają (GET tylko na bezpieczne linki, maks. 3)."""
    links = page.evaluate(PRIVACY_LINKS_JS)
    body = page.inner_text("body")
    checked, seen = [], set()
    for link in links:
        href = link["href"].split("#")[0]
        safe = (re.search(r"polityk|privacy|cookie", link["text"], re.I) and not UNSAFE_LINK_RE.search(href)
                and not any(s.lower() in href.lower() for s in secrets) and not find_secrets(href, []))
        if href in seen or not href.startswith("http") or len(seen) >= 3 or not safe:
            continue
        seen.add(href)
        try:
            r = context.request.get(href, timeout=15_000)
            text = r.text() if r.ok else ""
            checked.append({**link, "status": r.status, "mentions_administrator": bool(re.search(r"administrator", text, re.I))})
        except Exception as e:
            checked.append({**link, "status": f"błąd: {type(e).__name__}", "mentions_administrator": None})
    return {"links": links, "checked": checked,
            "page_mentions_administrator": bool(re.search(r"administrator(em)? (danych|twoich danych)", body, re.I))}


# ---------- analiza ----------

def classify(url: str):
    for pattern, tool, company, cat in TOOLS:
        if re.search(pattern, url, re.I):
            return tool, company, cat
    return None, None, "other"


def base_domain(host: str) -> str:
    parts = (host or "").split(".")
    n = 3 if len(parts) > 2 and parts[-2] in {"com", "co", "org", "net", "gov", "edu"} else 2
    return ".".join(parts[-n:])


def ga4_hits(requests: list[dict]) -> list[dict]:
    """Rozpisuje żądania GA4 /g/collect; POST z batchem = kilka zdarzeń, parametry wspólne w URL."""
    hits = []
    for r in requests:
        if "/g/collect" not in r["url"]:
            continue
        shared = dict(parse_qsl(urlsplit(r["url"]).query))
        lines = [l for l in (r["post_body"] or "").split("\r\n") if l.strip()] or [""]
        for line in lines:
            params = {**shared, **dict(parse_qsl(line))}
            hits.append({"t": r["t"], "phase": r["phase"], "host": r["host"], "params": params})
    return hits


def leak_hits(requests, site_host, secrets):
    """Żądania do zewnętrznych hostów zawierające token z URL, e-mail lub telefon (URL, referer, body)."""
    out = []
    for r in requests:
        if base_domain(r["host"]) == base_domain(site_host):
            continue
        for where, val in (("URL", r["url"]), ("Referer", r["referer"]), ("body", r["post_body"])):
            if not val:
                continue
            text = unquote(unquote(val))
            what = []
            for s in secrets:
                if secret_re(s).search(text):
                    keys = set(re.findall(r'["&?]?([\w.\-]+)["]?[=:]"?[^"&\s]*' + secret_re(s).pattern, text, re.I))
                    short = re.sub(r"\s", "", s)[:4]  # poza f-stringiem: backslash w f-stringu wymaga Pythona 3.12+
                    what.append(f"token {short}… (pola: {', '.join(sorted(keys)) or '?'})")
            if JWT_RE.search(text):
                keys = set(re.findall(r'"?([\w.\-]+)"?[=:]"?[^"&\s]*eyJ[\w-]+\.eyJ', text))
                what.append(f"JWT (pola: {', '.join(sorted(keys)) or '?'})")
            what += [f"e-mail {e[:2]}…" for e in set(EMAIL_RE.findall(text)) if not e.endswith((".png", ".js", ".css"))]
            what += [f"telefon {p[:3]}…" for p in set(PHONE_RE.findall(text))]
            if what:
                out.append({"t": r["t"], "phase": r["phase"], "host": r["host"], "where": where, "what": what, "req": r})
    return out


def har_entries(path: Path) -> tuple[dict, str | None]:
    """URL → lista wpisów HAR (numer od 1, czas wysłania, status) w kolejności wysłania + czas pierwszego wpisu."""
    idx = defaultdict(list)
    entries = json.loads(path.read_text())["log"]["entries"] if path.exists() else []
    for i, e in enumerate(entries, 1):
        idx[e["request"]["url"]].append({"n": i, "time": e["startedDateTime"], "status": e["response"]["status"]})
    return idx, (entries[0]["startedDateTime"] if entries else None)


def select_evidence(passes: dict, out: Path) -> list[dict]:
    """Jedna plansza na (przebieg, narzędzie): najpierw wycieki (żądanie z największą liczbą trafień),
    potem tracking przed zgodą (A) i po odrzuceniu (B) dla narzędzi bez planszy wycieku."""
    items, covered = [], set()
    for m, p in passes.items():
        reqs = sorted(p["requests"], key=lambda r: r["t"])
        har, p["har_start"] = har_entries(out / "raw" / m / "network.har")
        har_of = {id(r): (har[r["url"]].pop(0) if har.get(r["url"]) else None) for r in reqs}

        best = {}
        by_req = defaultdict(list)
        for l in p["leaks"]:
            by_req[id(l["req"])].append(l)
        for leaks in by_req.values():
            r = leaks[0]["req"]
            key = classify(r["url"])[0] or r["host"]
            score = sum(len(l["what"]) for l in leaks)
            if key not in best or score > best[key][0]:
                best[key] = (score, r, leaks)
        for tool, (_, r, leaks) in sorted(best.items(), key=lambda kv: kv[1][1]["t"]):
            items.append({"mode": m, "tool": tool, "kind": "leak", "req": r, "har": har_of[id(r)],
                          "what": [w for l in leaks for w in l["what"]]})
            covered.add((m, tool))

        want = {"A": "przed", "B": "po"}.get(m)
        for r in reqs:
            tool, _, cat = classify(r["url"])
            if want and r["phase"] == want and cat in TRACKING - {"tag-manager"} and (m, tool) not in covered:
                covered.add((m, tool))
                items.append({"mode": m, "tool": tool, "kind": "consent", "req": r, "har": har_of[id(r)], "what": []})
    for n, it in enumerate(items, 1):
        labels = {"token": "token z URL", "JWT": "JWT", "e-mail": "e-mail", "telefon": "telefon"}
        found = sorted({labels[w.split(" ")[0]] for w in it["what"]})
        it["title"] = (f"{it['tool']} otrzymuje: {', '.join(found)}" if it["kind"] == "leak" else
                       f"{it['tool']} wysyła dane " + ("przed jakąkolwiek zgodą" if it["mode"] == "A" else "po odrzuceniu zgód"))
        it["file"] = f"E{n:02d}-{it['mode']}-{re.sub(r'[^a-z0-9]+', '-', it['tool'].lower()).strip('-')}.png"
    return items


# Zdarzenia e-commerce GA4 i reguły wg dokumentacji Google:
# https://developers.google.com/analytics/devguides/collection/ga4/reference/events
# https://developers.google.com/analytics/devguides/collection/ga4/ecommerce?client_type=gtm
ECOM_EVENTS = {"view_item_list", "select_item", "view_item", "add_to_wishlist", "add_to_cart", "remove_from_cart",
               "view_cart", "begin_checkout", "add_shipping_info", "add_payment_info", "purchase", "refund",
               "view_promotion", "select_promotion"}
# value „Required*” w referencji zdarzeń (sprawdzone dla każdego); refund: items „No*” (zwrot całego zamówienia).
VALUE_EVENTS = ECOM_EVENTS - {"view_item_list", "select_item", "view_promotion", "select_promotion"}
UA_KEYS = {"impressions", "detail", "add", "remove", "checkout", "purchase", "promoView", "promoClick", "click", "currencyCode"}
NUMERIC = ("price", "discount", "quantity", "index")


def is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate_ecommerce(pages: list[dict], ga4: list[dict]) -> tuple[list[list], Counter]:
    """Struktura pushy `ecommerce` w dataLayer vs wytyczne GA4 + czy zdarzenie dotarło do GA4.
    Zwraca wiersze [url, zdarzenie, problem, waga] i licznik zdarzeń e-commerce w dataLayer."""
    rows, seen = [], Counter()
    sent = Counter(h["params"].get("en") for h in ga4)
    no_items = {h["params"].get("en") for h in ga4 if h["params"].get("en") in ECOM_EVENTS - {"refund"}
                and not any(k.startswith("pr") and k[2:].isdigit() for k in h["params"])}
    for pg in pages:
        # gtag('event', 'view_item', {...}) trafia do dataLayer jako tablica — normalizujemy do postaci pushy GTM
        dl = []
        for e in pg["datalayer"] or []:
            if isinstance(e, dict):
                dl.append(e)
            elif isinstance(e, list) and len(e) >= 3 and e[0] == "event" and e[1] in ECOM_EVENTS and isinstance(e[2], dict):
                dl.append({"event": e[1], "ecommerce": e[2], "_gtag": True})
        for i, e in enumerate(dl):
            ec = e.get("ecommerce")
            if not isinstance(ec, dict):
                continue
            ev = e.get("event") or "—"
            seen[ev] += 1
            add = lambda problem, weight: rows.append([pg["url"], ev, problem, weight])
            if UA_KEYS & ec.keys():
                add(f"format Universal Analytics (`{', '.join(sorted(UA_KEYS & ec.keys()))}`) zamiast GA4 `items`", "wysoka")
                continue
            if ev not in ECOM_EVENTS:
                add("nazwa zdarzenia spoza zalecanych zdarzeń e-commerce GA4", "średnia")
            items = ec.get("items")
            if (not isinstance(items, list) or not items) and ev != "refund":
                add("brak tablicy `items` albo jest pusta", "wysoka")
            if not isinstance(items, list):
                items = []
            bad = [n for n, it in enumerate(items) if not isinstance(it, dict) or not (it.get("item_id") or it.get("item_name"))]
            if bad:
                add(f"{len(bad)} z {len(items)} produktów bez `item_id` i `item_name`", "wysoka")
            for key in NUMERIC:
                wrong = [it[key] for it in items if isinstance(it, dict) and key in it and not is_num(it[key])]
                if wrong:
                    add(f"`items[].{key}` nie jest liczbą (np. {json.dumps(wrong[0], ensure_ascii=False)})", "średnia")
            if "value" in ec and not is_num(ec["value"]):
                add(f"`value` nie jest liczbą ({json.dumps(ec['value'], ensure_ascii=False)})", "średnia")
            if "value" in ec and not ec.get("currency"):
                add("`value` bez `currency`", "wysoka")
            if ec.get("currency") and not re.fullmatch(r"[A-Z]{3}", str(ec["currency"])):
                add(f"`currency` nie w formacie ISO 4217 ({ec['currency']})", "średnia")
            if ev in VALUE_EVENTS and "value" not in ec:
                add("brak `value` (zalecane do raportowania)", "niska")
            if ev in {"purchase", "refund"} and not ec.get("transaction_id"):
                add("brak `transaction_id`", "wysoka")
            if is_num(ec.get("value")) and items and all(isinstance(it, dict) and is_num(it.get("price")) for it in items):
                total = sum(it["price"] * (it.get("quantity") if is_num(it.get("quantity")) else 1) for it in items)
                if abs(total - ec["value"]) > 0.01:
                    add(f"`value` {ec['value']} ≠ suma price×quantity {round(total, 2)}", "niska")
            # Model danych GTM pamięta ostatnią wartość `ecommerce`: problem tylko, gdy poprzedni push z tym kluczem nie był null.
            # gtag() nie używa modelu danych GTM, więc tam reguła nie dotyczy.
            prev = next((d for d in reversed(dl[:i]) if "ecommerce" in d and not d.get("_gtag")), None)
            if not e.get("_gtag") and prev is not None and prev["ecommerce"] is not None:
                add("brak `dataLayer.push({ecommerce: null})` przed zdarzeniem — dziedziczy poprzedni obiekt", "niska")
    for ev in seen:
        if ev in ECOM_EVENTS and not sent[ev]:
            rows.append(["—", ev, "zdarzenie w dataLayer, ale brak żądania GA4 z tym `en`", "średnia"])
        if ev in no_items:
            rows.append(["—", ev, "żądanie GA4 bez parametrów produktów `pr1…`", "wysoka"])
    grouped = Counter(tuple(r) for r in rows)  # identyczne problemy z powtórzonych pushy jako jeden wiersz
    return [[*r[:2], r[2] + (f" (×{n})" if n > 1 else ""), r[3]] for r, n in grouped.items()], seen


def cookie_tool(name: str) -> str:
    for pattern, tool in COOKIE_TOOLS:
        if re.search(pattern, name):
            return tool
    return "?"


def expiry(c, now) -> str:
    if c.get("expires", -1) in (-1, None) or c["expires"] < 0:
        return "sesja"
    days = (c["expires"] - now) / 86400
    return f"{days:.0f} dni" if days >= 1 else f"{days * 24:.1f} h"


def md_table(header: list[str], rows: list[list]) -> str:
    if not rows:
        return "_brak_"
    esc = lambda v: str(v).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def build_report(url, slug, passes, secrets, evidence) -> str:
    mask = make_masker(secrets)
    site_host = urlsplit(passes["A"]["final_url"]).hostname
    modes = list(passes)
    now = time.time()
    v = {"slug": slug, "date": dt.date.today().isoformat(), "url": mask(url), "site_host": site_host}

    # Przebiegi
    rows = []
    for m, p in passes.items():
        rows.append([m, p["click"] or "—", p["buttons"]["reject"] or "—", p["buttons"]["accept"] or "—",
                     len(p["requests"])])
    v["passes"] = md_table(["Przebieg", "Kliknięto", "Przycisk „odrzuć”", "Przycisk „akceptuj”", "Żądania"],
                           [[mask(c) for c in r] for r in rows])
    skipped = [m for m in "BC" if m not in passes]
    if skipped:
        v["passes"] += f"\n\nPominięte przebiegi: {', '.join(skipped)} — brak odpowiedniego przycisku w banerze (przebieg A)."

    # Zgody
    g = passes["A"]["globals"]
    cmp_found = [n for n, k in (("OneTrust", "onetrust"), ("Cookiebot", "cookiebot"), ("CookieYes", "cookieyes"),
                                ("Didomi", "didomi")) if any(p["globals"][k] for p in passes.values())]
    cmp_found += [classify(r["url"])[0] for p in passes.values() for r in p["requests"] if classify(r["url"])[2] == "cmp"]
    tcf = any(p["globals"]["tcf"] for p in passes.values())
    consent_cmds = []
    for m, p in passes.items():
        for e in (e for pg in p["datalayer"] for e in pg["datalayer"] or []):
            if isinstance(e, list) and e and e[0] == "consent":
                consent_cmds.append([m, json.dumps(e, ensure_ascii=False)])
    gcs_rows = []
    for m, p in passes.items():
        for ph in ("przed", "po"):
            hits = [h["params"] for h in p["ga4"] if h["phase"] == ph]
            if hits:
                gcs_rows.append([m, ph, ", ".join(sorted({h.get("gcs", "—") for h in hits})),
                                 ", ".join(sorted({h.get("gcd", "—") for h in hits})), len(hits)])
    track_rows = []
    for m, p in passes.items():
        for ph in ("przed", "po"):
            cnt = Counter(classify(r["url"])[0] for r in p["requests"]
                          if r["phase"] == ph and classify(r["url"])[2] in TRACKING)
            if cnt:
                track_rows.append([m, ph, "; ".join(f"{t} ×{n}" for t, n in cnt.most_common())])
    v["consent"] = "\n\n".join([
        f"- CMP: {', '.join(sorted(set(filter(None, cmp_found)))) or 'nie wykryto'}; IAB TCF (`__tcfapi`): {'tak' if tcf else 'nie'}.",
        "**Komendy `gtag('consent', …)` w dataLayer**\n\n" + md_table(["Przebieg", "Komenda"], consent_cmds),
        "**Parametry Consent Mode w żądaniach GA4** (faza = przed/po kliknięciu w baner)\n\n"
        + md_table(["Przebieg", "Faza", "gcs", "gcd", "Zdarzenia GA4"], gcs_rows),
        "**Żądania narzędzi śledzących/monitorujących**\n\n" + md_table(["Przebieg", "Faza", "Narzędzie × żądania"], track_rows),
    ])

    # Tagi
    all_urls = [(m, r) for m, p in passes.items() for r in p["requests"]]
    ids = defaultdict(set)
    for m, r in all_urls:
        u = r["url"]
        for rx, label in ((r"[?&]id=(GTM-[A-Z0-9]+)", "GTM"), (r"(GTM-[A-Z0-9]{4,})", "GTM"),
                          (r"[?&](?:id|tid)=(G-[A-Z0-9]+)", "GA4"), (r"[?&]id=(AW-\d+)", "Google Ads"),
                          (r"/(?:viewthroughconversion|conversion)/(\d{9,11})/", "Google Ads"), (r"facebook\.com/tr/?\?id=(\d+)", "Meta Pixel"),
                          (r"sdkid=([A-Z0-9]+)", "TikTok"), (r"[?&]pid=(\d+)", "LinkedIn"),
                          (r"hotjar-(\d+)\.js", "Hotjar"), (r"clarity\.ms/tag/(\w+)", "Clarity")):
            for found in re.findall(rx, u):
                ids[label].add(found)
    for k in (k for k in g["gtm_keys"] if re.match(r"(GTM|G|AW|DC|GT)-", k)):
        ids["GTM" if k.startswith("GTM-") else "GA4" if k.startswith("G-") else "Google tag"].add(k)
    gtm_loads = Counter(re.search(r"id=([\w-]+)", r["url"]).group(1) for m, r in all_urls
                        if m == "A" and re.search(r"(gtm|gtag/js)\.?j?s?\?id=", r["url"]) and re.search(r"id=([\w-]+)", r["url"]))
    tools_seen = Counter(classify(r["url"])[0] for m, r in all_urls if classify(r["url"])[0])
    sgtm = sorted({r["host"] for m, r in all_urls if "/g/collect" in r["url"]
                   and not re.search(r"google-analytics\.com|analytics\.google\.com", r["host"])}
                  | {r["host"] for m, r in all_urls if re.search(r"/gtm\.js\?id=", r["url"]) and "googletagmanager.com" not in r["host"]})
    pv = Counter((h["params"].get("tid"), h["phase"]) for h in passes["A"]["ga4"] if h["params"].get("en") == "page_view")
    v["tags"] = "\n".join([
        md_table(["Typ", "Identyfikatory"], [[k, ", ".join(sorted(s))] for k, s in sorted(ids.items())]),
        "",
        f"- Wczytania skryptów GTM/gtag w przebiegu A: {', '.join(f'{k} ×{n}' for k, n in gtm_loads.items()) or 'brak'}.",
        f"- `page_view` na identyfikator GA4 w przebiegu A: {', '.join(f'{t} ×{n}' for (t, _), n in pv.items()) or 'brak'}.",
        f"- Server-side GTM / własny endpoint: {', '.join(sgtm) or 'nie wykryto'}.",
        "- Datadog Session Replay: body żądań `/api/v2/replay` to blob multipart — Playwright go nie zapisuje; ocena tylko na podstawie faktu wysyłki." if any("/api/v2/replay" in r["url"] for _, r in all_urls) else "",
        f"- Globalne obiekty (A): " + ", ".join(k for k, val in g.items() if val is True) + ".",
        "- Narzędzia wg żądań (wszystkie przebiegi): " + "; ".join(f"{t} ×{n}" for t, n in tools_seen.most_common()) + ".",
    ])

    # GA4
    ga_rows = []
    for m, p in passes.items():
        for h in p["ga4"]:
            pr = h["params"]
            extra = {k: val for k, val in pr.items() if k.startswith(("ep.", "epn.", "up.", "upn."))}
            ga_rows.append([m, h["phase"], h["t"], pr.get("en"), pr.get("tid"), pr.get("cid"), pr.get("sid"),
                            mask(pr.get("dl")) or "—", mask(pr.get("dr")) or "—", pr.get("gcs") or "—", pr.get("gcd") or "—",
                            mask(json.dumps(extra, ensure_ascii=False)) if extra else "—"])
    events = Counter((m, h["params"].get("en")) for m, p in passes.items() for h in p["ga4"])
    v["ga4"] = ("Zdarzenia: " + (", ".join(f"{m}: {e} ×{n}" for (m, e), n in sorted(events.items(), key=str)) or "brak")
                + "\n\n" + md_table(["Przebieg", "Faza", "t [s]", "en", "tid", "cid", "sid", "dl", "dr", "gcs", "gcd", "ep./up."], ga_rows))

    # E-commerce: walidujemy przebieg z największą szansą na odpalone tagi (C po akceptacji, inaczej A)
    em = "C" if "C" in passes else "A"
    ec_rows, ec_seen = validate_ecommerce(passes[em]["datalayer"], passes[em]["ga4"])
    pages = ", ".join(f"`{mask(pg['url'])}`" for pg in passes[em]["datalayer"])
    v["ecommerce"] = (f"Przebieg {em}, strony: {pages}.\n\nZdarzenia e-commerce w dataLayer: "
                      + (", ".join(f"{e} ×{n}" for e, n in ec_seen.items())
                         or "nie wykryto. Strona bez sprzedaży → sekcja nie dotyczy; sklep → uruchom ponownie z `--extra-url` (kategoria, produkt)")
                      + ".\n\n" + (md_table(["Strona", "Zdarzenie", "Problem", "Waga"], [[mask(r[0]), *r[1:]] for r in ec_rows])
                                     if ec_seen else "")).rstrip()

    # Wycieki
    leak_rows = []
    for m, p in passes.items():
        for l in p["leaks"]:
            tool = classify(l["req"]["url"])[0] or l["host"]
            proof = next((f"`screenshots/{e['file']}`" for e in evidence if e["mode"] == m and e["tool"] == tool), "—")
            leak_rows.append([m, l["phase"], l["t"], l["host"], l["where"], mask("; ".join(l["what"])), proof])
    v["leaks"] = md_table(["Przebieg", "Faza", "t [s]", "Host", "Gdzie", "Co", "Dowód"], leak_rows)

    # Odbiorcy
    rec = defaultdict(lambda: {"cnt": Counter(), "data": set()})
    for m, p in passes.items():
        leaks_by_host = defaultdict(set)
        for l in p["leaks"]:
            leaks_by_host[l["host"]] |= {w.split(" (")[0].split(" ")[0] for w in l["what"]}
        for r in p["requests"]:
            if base_domain(r["host"]) == base_domain(site_host):
                continue
            e = rec[r["host"]]
            e["cnt"][m] += 1
            if r["referer"] and site_host in r["referer"]:
                e["data"].add("Referer ze stroną")
            if site_host in unquote(r["url"].split("?", 1)[-1] if "?" in r["url"] else "") or site_host in (r["post_body"] or ""):
                e["data"].add("URL strony w parametrach/body")
            if "/g/collect" in r["url"]:
                e["data"].add("cid/sid (identyfikatory GA)")
            e["data"] |= {f"⚠ {x}" for x in leaks_by_host[r["host"]]}
    rec_rows = []
    for host, e in sorted(rec.items(), key=lambda kv: -sum(kv[1]["cnt"].values())):
        tool, company, _ = classify("https://" + host + "/")
        if not tool:
            tool, company, _ = classify(next(r["url"] for p in passes.values() for r in p["requests"] if r["host"] == host))
        rec_rows.append([host, f"{company or '?'} / {tool or '?'}", *[e["cnt"].get(m, 0) if m in passes else "—" for m in "ABC"],
                         ", ".join(sorted(e["data"])) or "zasoby statyczne"])
    v["recipients"] = md_table(["Host", "Firma / narzędzie", "A", "B", "C", "Jakie dane"], rec_rows)

    # Ciasteczka
    ck = {}
    for m, p in passes.items():
        for c in p["cookies"]:
            key = (c["name"], c["domain"])
            ck.setdefault(key, {"c": c, "modes": set()})["modes"].add(m)
    ck_rows = [[mask(n), d, expiry(e["c"], now), cookie_tool(n), *[("✔" if m in e["modes"] else "—") if m in passes else "n/d" for m in "ABC"]]
               for (n, d), e in sorted(ck.items())]
    v["cookies"] = md_table(["Nazwa", "Domena", "Ważność", "Narzędzie", "A", "B", "C"], ck_rows)
    ls = {k for p in passes.values() for k in (p["storage"].get("localStorage") or {})}
    ss = {k for p in passes.values() for k in (p["storage"].get("sessionStorage") or {})}
    v["cookies"] += (f"\n\nKlucze localStorage: {mask(', '.join(sorted(ls))) or 'brak'}.  "
                     f"\nKlucze sessionStorage: {mask(', '.join(sorted(ss))) or 'brak'}.")

    # Prywatność
    pr = passes["A"].get("privacy") or {"links": [], "checked": [], "page_mentions_administrator": False}
    v["privacy"] = "\n".join([
        f"- Linki o prywatności/cookies na stronie: {len(pr['links'])}.",
        f"- Strona wprost wskazuje administratora danych: {'tak' if pr['page_mentions_administrator'] else 'nie znaleziono'}.",
        "", md_table(["Tekst linku", "URL", "HTTP", "Wzmianka o administratorze"],
                     [[mask(c["text"]), mask(c["href"]), mask(c["status"]), c["mentions_administrator"]] for c in pr["checked"]]),
    ])

    v["evidence"] = "\n".join(["- `screenshots/00-strona.png` — strona i adres (przebieg A)"]
                              + [f"- `screenshots/{e['file']}` — {e['title']}" for e in evidence])
    template = string.Template((ROOT / "report_template.md").read_text())
    return template.safe_substitute(v)


def main():
    ap = argparse.ArgumentParser(description="Pasywny audyt analityki i prywatności strony WWW")
    ap.add_argument("url")
    ap.add_argument("--slug", required=True, help="nazwa firmy w ścieżce, np. acme")
    ap.add_argument("--mask", action="append", default=[], help="tekst do zamaskowania (imię, e-mail); można powtarzać")
    ap.add_argument("--rebuild", action="store_true", help="zbuduj raport z istniejącego raw/ bez wczytywania strony")
    ap.add_argument("--extra-url", action="append", default=[],
                    help="kolejna strona w tym samym przebiegu, np. kategoria/produkt (walidacja e-commerce); można powtarzać")
    ap.add_argument("--headed", action="store_true", help="pokaż okno przeglądarki")
    args = ap.parse_args()

    # Sekrety tylko z głównego URL (adresy --extra-url to publiczne strony sklepu, slug produktu to nie token).
    secrets = find_secrets(args.url, args.mask)
    if args.rebuild:  # najnowszy istniejący audyt tej firmy, niezależnie od dzisiejszej daty
        found = sorted(REPORTS.glob(f"????-??-??-{args.slug}"))
        if not found:
            raise SystemExit(f"Brak audytu dla slug „{args.slug}” w reports/")
        out = found[-1]
        saved = out / "raw" / "secrets.json"  # --mask z przechwycenia działa też przy rebuildzie
        secrets = sorted(set(secrets) | set(json.loads(saved.read_text()) if saved.exists() else []), key=len, reverse=True)
        passes = load_passes(out)
    else:
        out = REPORTS / f"{dt.date.today().isoformat()}-{args.slug}"
        shutil.rmtree(out / "raw", ignore_errors=True)  # bez resztek B/C z wcześniejszego przebiegu tego dnia
        (out / "raw").mkdir(parents=True)
        (out / "raw" / "secrets.json").write_text(json.dumps(secrets, ensure_ascii=False))
        passes = capture(args.url, out, secrets, args.headed, args.extra_url)

    site_host = urlsplit(passes["A"]["final_url"]).hostname
    for p in passes.values():  # liczone raz na przebieg, używane w planszach i raporcie
        p["ga4"] = ga4_hits(p["requests"])
        p["leaks"] = leak_hits(p["requests"], site_host, secrets)
    evidence = select_evidence(passes, out)
    render_evidence(evidence, passes, args.url, out, make_masker(secrets))
    report = build_report(args.url, args.slug, passes, secrets, evidence)
    (out / "RAPORT.md").write_text(report)
    print(f"Gotowe: {out / 'RAPORT.md'}")


def load_passes(out: Path) -> dict:
    passes = {}
    for d in sorted(d for d in (out / "raw").iterdir() if (d / "pass.json").exists()):  # pomija .DS_Store itp.
        p = json.loads((d / "pass.json").read_text())
        for name in ("requests", "cookies", "storage", "datalayer"):
            p[name] = json.loads((d / f"{name}.json").read_text())
        p["requests"] = [r for r in p["requests"] if r["url"].startswith("http")]
        passes[d.name] = p
    return passes


def capture(url: str, out: Path, secrets: list[str], headed: bool, extra_urls: list[str]) -> dict:
    passes = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        print("Przebieg A: bez interakcji")
        passes["A"] = run_pass(browser, url, "A", out, secrets, extra_urls)
        for mode, kind in (("B", "reject"), ("C", "accept")):
            if passes["A"]["buttons"][kind]:
                print(f"Przebieg {mode}: klik „{kind}”")
                res = run_pass(browser, url, mode, out, secrets, extra_urls)
                if res["click"]:
                    passes[mode] = res
                else:  # przycisk nie pojawił się w tym przebiegu — nie udajemy „po odrzuceniu/akceptacji”
                    print(f"  ! przebieg {mode} pominięty: przycisk nie pojawił się")
                    shutil.rmtree(out / "raw" / mode, ignore_errors=True)
            else:
                print(f"Przebieg {mode}: pominięty (brak przycisku „{kind}”)")
        browser.close()
    return passes


if __name__ == "__main__":
    main()
