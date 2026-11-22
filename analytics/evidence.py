"""Plansze dowodowe PNG dla raportu audytu.

Zamiast zrzutu samego DevTools (nie da się go niezawodnie zautomatyzować ani zamaskować)
renderujemy żądanie z przechwyconego ruchu w układzie podobnym do panelu Network:
adres strony, czas wysłania z HAR, numer wpisu w HAR, parametry i body z podświetlonymi danymi.
Wszystkie teksty przechodzą przez funkcję maskującą przed renderowaniem.
"""

import base64
import datetime as dt
import html
import re
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

from playwright.sync_api import sync_playwright

# Zamaskowane wartości („7ea9…”, „ja…@domena”, „eyJ…(JWT)”) — to je podświetlamy.
MARK_RE = re.compile(r"[\w+]{2,4}…(?:@[\w.-]+)?|eyJ…\(JWT\)")
MODES = {"A": "A — bez interakcji z banerem", "B": "B — po kliknięciu „odrzuć”", "C": "C — po kliknięciu „akceptuj”"}

CSS = """
* { box-sizing: border-box; }
body { margin: 0; padding: 24px; background: #e8eaed; font: 14px/1.45 -apple-system, 'Segoe UI', Roboto, sans-serif; color: #202124; }
.card { width: 1200px; background: #fff; border: 1px solid #c4c7c5; border-radius: 10px; overflow: hidden; }
.bar { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #dee1e6; }
.dots span { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 6px; }
.addr { flex: 1; background: #fff; border-radius: 16px; padding: 6px 14px; font-family: Menlo, monospace; font-size: 13px; }
.stamp { font-size: 12px; color: #444; white-space: nowrap; }
h1 { margin: 0; padding: 14px 18px 4px; font-size: 18px; }
.badge { display: inline-block; margin-left: 8px; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: 600; background: #fce8e6; color: #a50e0e; }
.meta { padding: 4px 18px 12px; font-size: 13px; color: #444; }
.sec { border-top: 1px solid #dadce0; }
.sec h2 { margin: 0; padding: 7px 18px; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; background: #f1f3f4; color: #5f6368; }
table { width: 100%; border-collapse: collapse; font-family: Menlo, monospace; font-size: 12px; }
td { padding: 3px 18px; vertical-align: top; border-bottom: 1px solid #f1f3f4; word-break: break-all; }
td.k { width: 230px; color: #881391; word-break: normal; }
tr.hit td { background: #fff4e5; }
mark { background: #f9ab00; color: #000; padding: 0 2px; border-radius: 3px; font-weight: 700; }
pre { margin: 0; padding: 8px 18px; font: 12px/1.5 Menlo, monospace; white-space: pre-wrap; word-break: break-all; }
img { display: block; width: 100%; }
.foot { padding: 8px 18px; font-size: 11px; color: #5f6368; border-top: 1px solid #dadce0; }
"""


def _hl(text, mask) -> str:
    """Maskuje, escapuje HTML i podświetla zamaskowane dane."""
    return MARK_RE.sub(lambda m: f"<mark>{m.group()}</mark>", html.escape(mask(text)))


def _rows(pairs, mask) -> str:
    out = []
    for k, v in pairs:
        cell = _hl(v, mask)
        out.append(f'<tr class="{"hit" if "<mark>" in cell else ""}"><td class="k">{html.escape(k)}</td><td>{cell}</td></tr>')
    return "<table>" + "".join(out) + "</table>"


def _snippets(body: str, mask) -> list[str]:
    """Po jednym fragmencie body na parę (zamaskowana wartość, pole). Najpierw maskujemy całe body,
    potem tniemy — cięcie nie może przepołowić tokenu i zostawić go jawnym."""
    text = mask(body)
    seen, out = set(), []
    for m in MARK_RE.finditer(text):
        before = text[max(0, m.start() - 90): m.start()]
        key = (re.findall(r'"?([\w.-]+)"?\s*[:=]\s*"?[^"&,{]*$', before) or ["?"])[-1]
        if (m.group(), key) in seen:
            continue
        seen.add((m.group(), key))
        out.append("⋯" + before + text[m.start(): m.end() + 40] + "⋯")
    return out[:8]


def _payload(req: dict, mask) -> str:
    body = req.get("post_body")
    if not body:
        return "<pre>brak body albo body binarne (blob), którego Playwright nie przechwytuje</pre>"
    if "/g/collect" in req["url"]:  # GA4: każda linia body = osobne zdarzenie
        events = [l for l in body.split("\r\n") if l.strip()]
        return "".join(f"<pre><b>zdarzenie {i}</b></pre>" + _rows(parse_qsl(l), mask) for i, l in enumerate(events, 1))
    frags = _snippets(body, mask)
    if frags:
        return f"<pre>{len(frags)} fragment(y) body z trafieniami:</pre>" + "".join(f"<pre>{_hl(f, lambda x: x)}</pre>" for f in frags)
    return f"<pre>{_hl(body[:600] + ('⋯' if len(body) > 600 else ''), mask)}</pre>"


def _when(har) -> str:
    if not har:
        return "brak wpisu w HAR"
    t = dt.datetime.fromisoformat(har["time"].replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    return t.strftime("%Y-%m-%d %H:%M:%S.") + f"{t.microsecond // 1000:03d} UTC"


def _bar(url: str, stamp: str, mask) -> str:
    return ('<div class="bar"><div class="dots"><span style="background:#ff5f57"></span><span style="background:#febc2e">'
            f'</span><span style="background:#28c840"></span></div><div class="addr">🔒 {_hl(url, mask)}</div>'
            f'<div class="stamp">{html.escape(stamp)}</div></div>')


def _card(item: dict, page_url: str, mask) -> str:
    r, har = item["req"], item["har"]
    phase = "przed kliknięciem w baner" if r["phase"] == "przed" else "po kliknięciu w baner"
    badge = "WYCIEK" if item["kind"] == "leak" else "BEZ ZGODY"
    found = f"<br>Wykryto: {_hl('; '.join(item['what']), mask)}" if item["what"] else ""
    headers = [("Request Method", r["method"]), ("Status Code", str(har["status"]) if har else "?"),
               ("Resource Type", r["type"]), ("Referer", r.get("referer") or "—")]
    return f"""<div class="card">{_bar(page_url, _when(har), mask)}
<h1>{html.escape(item['title'])}<span class="badge">{badge}</span></h1>
<div class="meta">Przebieg {MODES[item['mode']]} · faza: {phase} · +{r['t']} s od wejścia ·
HAR: <code>raw/{item['mode']}/network.har</code>, wpis #{har['n'] if har else '?'}{found}</div>
<div class="sec"><h2>General</h2>{_rows([("Request URL", r["url"].split("?")[0])] + headers, mask)}</div>
<div class="sec"><h2>Query String Parameters</h2>{_rows(parse_qsl(urlsplit(r["url"]).query), mask)}</div>
<div class="sec"><h2>Payload</h2>{_payload(r, mask)}</div>
<div class="foot">Plansza wygenerowana przez analytics/audit.py z ruchu przechwyconego w Chromium (Playwright). Tokeny i dane osobowe zamaskowane.</div>
</div>"""


def _context_card(page_url: str, stamp: str, page_png: Path, mask) -> str:
    img = base64.b64encode(page_png.read_bytes()).decode() if page_png.exists() else ""
    shot = f'<img src="data:image/png;base64,{img}">' if img else "<pre>brak zrzutu strony</pre>"
    return f"""<div class="card">{_bar(page_url, stamp, mask)}{shot}
<div class="foot">Przebieg A — wczytanie strony bez interakcji. Chromium (Playwright), pl-PL, 1440×900. Adres i czas pierwszego żądania z HAR.</div></div>"""


def render_evidence(items: list[dict], passes: dict, page_url: str, out: Path, mask) -> None:
    """Renderuje 00-strona.png (kontekst) i E*.png (po jednej planszy na znalezisko) do screenshots/."""
    shots = out / "screenshots"
    shots.mkdir(exist_ok=True)
    for old in [*shots.glob("E*.png"), shots / "00-strona.png"]:  # bez nieaktualnych plansz z poprzednich przebiegów
        old.unlink(missing_ok=True)
    start = passes["A"].get("har_start")
    stamp = _when({"time": start}) if start else ""
    cards = {"00-strona.png": _context_card(page_url, stamp, out / "raw" / "A" / "page.png", mask)}
    for it in items:
        cards[it["file"]] = _card(it, page_url, mask)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1260, "height": 900})
        for name, card in cards.items():
            page.set_content(f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>{card}")
            page.locator(".card").screenshot(path=shots / name)
        browser.close()
