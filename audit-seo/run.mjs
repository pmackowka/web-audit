// Uruchomienie (z katalogu głównego repo): npm --prefix audit-seo run audit -- https://example.com/
// Audytuje stronę startową i kolejne adresy z sitemapy (do MAX_PAGES): fakty SEO, axe-core, Lighthouse;
// potem reguły całego serwisu (robots.txt, sitemap, duplikaty, linki wewnętrzne) i zapis raportu Markdown do audit-seo/reports/.
// Kod wyjścia: 0 = brak błędów, 1 = są błędy (status FAIL), 2 = audyt się nie wykonał.
import { mkdir, writeFile } from 'node:fs/promises';
import { createServer } from 'node:net';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
import lighthouse from 'lighthouse';
import {
  LH_CATEGORIES, checkPage, checkSite, groupFindings, mapAxe, mapLighthouse, parseSitemap, renderReport, sitemapUrlsFromRobots,
} from './lib.mjs';

const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
// Limity trzymają audyt cudzej strony na poziomie zwykłego odwiedzającego, a czas — w kilku minutach.
const MAX_PAGES = 10;
const MAX_CHILD_SITEMAPS = 5;
const MAX_LINKS = 100;
const NON_HTML = /\.(pdf|jpe?g|png|gif|webp|svg|xml|zip|mp4|docx?|xlsx?)$/i;

// Wolny port dla Chrome DevTools Protocol — stały 9222 mógłby trafić w inną, już otwartą przeglądarkę.
function freePort() {
  return new Promise((resolve, reject) => {
    const server = createServer().listen(0, () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    }).on('error', reject);
  });
}

const withoutHash = (url) => {
  const u = new URL(url);
  u.hash = '';
  return u.href;
};

// Zapytania HTTP idą przez kontekst przeglądarki (ten sam User-Agent), żeby ochrona przed botami nie zawyżała błędów.
async function fetchText(request, url) {
  try {
    const res = await request.get(url);
    return { status: res.status(), body: res.ok() ? await res.text() : '' };
  } catch {
    return { status: 0, body: '' };
  }
}

async function fetchStatus(request, url) {
  try {
    const head = await request.head(url);
    if (![405, 501].includes(head.status())) return head.status();
    return (await request.get(url)).status();
  } catch {
    return 0;
  }
}

async function collectFacts(page, response) {
  // Łańcuch przekierowań odtwarzamy od końcowego żądania wstecz.
  const redirects = [];
  for (let req = response.request(); req; req = req.redirectedFrom()) redirects.unshift(req.url());

  const dom = await page.evaluate(() => {
    const meta = (sel) => document.querySelector(sel)?.getAttribute('content') ?? null;
    return {
      title: document.title,
      metaDescription: meta('meta[name="description"]'),
      robotsMeta: meta('meta[name="robots"]'),
      viewport: meta('meta[name="viewport"]'),
      canonicals: [...document.querySelectorAll('link[rel="canonical"]')].map((l) => l.href),
      h1: [...document.querySelectorAll('h1')].map((h) => h.textContent.trim().replace(/\s+/g, ' ')),
      og: {
        'og:title': meta('meta[property="og:title"]'),
        'og:description': meta('meta[property="og:description"]'),
        'og:image': meta('meta[property="og:image"]'),
      },
      jsonLdRaw: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent),
      links: [...document.querySelectorAll('a[href]')].map((a) => a.href),
    };
  });

  const jsonLd = dom.jsonLdRaw.map((raw) => {
    try { JSON.parse(raw); return { valid: true }; } catch (err) { return { valid: false, error: err.message }; }
  });

  return {
    status: response.status(),
    finalUrl: page.url(),
    redirects: redirects.length > 1 ? redirects : [],
    xRobotsTag: response.headers()['x-robots-tag'] ?? null,
    ...dom,
    jsonLd,
  };
}

// Jedna strona: fakty SEO + axe w Playwright, potem Lighthouse w osobnej karcie tego samego Chromium.
// Błąd strony nie przerywa audytu — trafia do tabeli stron.
async function auditPage(context, url, port) {
  const page = await context.newPage();
  try {
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 60_000 });
    if (!response) throw new Error('brak odpowiedzi');
    const facts = await collectFacts(page, response);
    const axeResults = await new AxeBuilder({ page }).withTags(WCAG_TAGS).analyze();
    const lhResult = await lighthouse(url, { port, logLevel: 'error', onlyCategories: LH_CATEGORIES });
    if (!lhResult) throw new Error('Lighthouse nie zwrócił wyniku');
    return {
      url, status: facts.status, facts, seo: checkPage(facts), axe: mapAxe(axeResults),
      axeVersion: axeResults.testEngine.version, lhr: lhResult.lhr,
    };
  } catch (err) {
    return { url, status: 0, error: err.message.split('\n')[0] };
  } finally {
    await page.close();
  }
}

// Adresy stron z sitemapy (z obsługą indeksu sitemap). Zwraca też liczbę <loc> do reguły seo-sitemap.
async function readSitemap(request, sitemapUrl) {
  const res = await fetchText(request, sitemapUrl);
  if (res.status !== 200) return { status: res.status, locs: [] };
  const parsed = parseSitemap(res.body);
  if (!parsed.isIndex) return { status: 200, locs: parsed.locs };
  const locs = [];
  for (const child of parsed.locs.slice(0, MAX_CHILD_SITEMAPS)) {
    const childRes = await fetchText(request, child);
    if (childRes.status === 200) locs.push(...parseSitemap(childRes.body).locs);
  }
  return { status: 200, locs };
}

async function main() {
  let startUrl;
  try {
    startUrl = new URL(process.argv[2]).href;
  } catch {
    console.error('Użycie: npm --prefix audit-seo run audit -- https://example.com/');
    process.exit(2);
  }

  // Lighthouse łączy się z tym samym Chromium przez CDP i otwiera w nim własną kartę.
  const port = await freePort();
  const browser = await chromium.launch({ args: [`--remote-debugging-port=${port}`] });
  try {
    const context = await browser.newContext();
    const { request } = context;

    const home = await auditPage(context, startUrl, port);
    if (home.error) throw new Error(`strona startowa: ${home.error}`);
    const origin = new URL(home.facts.finalUrl).origin;

    const robots = await fetchText(request, `${origin}/robots.txt`);
    const sitemapUrl = sitemapUrlsFromRobots(robots.body)[0] ?? `${origin}/sitemap.xml`;
    const sitemap = await readSitemap(request, sitemapUrl);

    // Kolejne strony: adresy z sitemapy w jej kolejności, z tej samej domeny, bez plików i bez strony startowej.
    const seen = new Set([startUrl, home.facts.finalUrl].map(withoutHash));
    const nextUrls = [];
    for (const loc of sitemap.locs) {
      let url;
      try { url = withoutHash(loc); } catch { continue; }
      if (nextUrls.length >= MAX_PAGES - 1) break;
      if (new URL(url).origin !== origin || NON_HTML.test(new URL(url).pathname) || seen.has(url)) continue;
      seen.add(url);
      nextUrls.push(url);
    }
    const pages = [home];
    for (const url of nextUrls) pages.push(await auditPage(context, url, port));
    const ok = pages.filter((p) => !p.error);

    // Linki wewnętrzne ze wszystkich stron; adresy audytowanych stron mają już status, więc ich nie odpytujemy.
    const sources = new Map();
    for (const p of ok) {
      for (const href of p.facts.links) {
        let url;
        try { url = withoutHash(href); } catch { continue; }
        if (new URL(url).origin !== origin || seen.has(url)) continue;
        sources.set(url, new Set([...(sources.get(url) ?? []), p.url]));
      }
    }
    const linkUrls = [...sources.keys()].sort();
    const broken = [];
    for (const url of linkUrls.slice(0, MAX_LINKS)) {
      const status = await fetchStatus(request, url);
      if (status === 0 || status >= 400) broken.push({ url, status, sources: [...sources.get(url)].sort() });
    }

    const site = checkSite({
      robots,
      sitemap: { url: sitemapUrl, status: sitemap.status, locCount: sitemap.locs.length },
      pages: ok.map((p) => ({ url: p.url, status: p.status, title: p.facts.title, metaDescription: p.facts.metaDescription })),
      links: { total: linkUrls.length, checked: Math.min(linkUrls.length, MAX_LINKS), broken },
      failed: pages.filter((p) => p.error).map((p) => ({ url: p.url, error: p.error })),
    });

    // Lighthouse mapujemy na końcu, żeby odsyłał do własnych reguł (także serwisowych), zamiast je dublować.
    const siteIds = site.findings.map((f) => f.id);
    for (const p of ok) {
      p.lighthouse = mapLighthouse(p.lhr, new Set([...siteIds, ...p.seo.findings.map((f) => f.id), ...p.axe.findings.map((f) => f.id)]));
    }

    const groups = groupFindings([
      ...site.findings.map((finding) => ({ page: null, finding })),
      ...ok.flatMap((p) => [...p.seo.findings, ...p.axe.findings, ...p.lighthouse.findings].map((finding) => ({ page: p.url, finding }))),
    ]);
    const manualGroups = groupFindings(ok.flatMap((p) => p.axe.manual.map((finding) => ({ page: p.url, finding }))));
    const failing = new Set(groups.map((g) => g.id));
    const passed = [...new Set([...site.passed, ...ok.flatMap((p) => [...p.seo.passed, ...p.axe.passed])])]
      .filter((id) => !failing.has(id)).sort();

    const date = new Date().toISOString().slice(0, 10);
    const report = renderReport({
      url: startUrl,
      date,
      engines: `Lighthouse ${home.lighthouse.version} (${home.lighthouse.formFactor}), axe-core ${home.axeVersion}`,
      wcagTags: WCAG_TAGS,
      pages: pages.map((p) => ({ url: p.url, status: p.status, error: p.error, lighthouse: p.lighthouse ?? null })),
      groups,
      manualGroups,
      passed,
    });

    // Raporty obok kodu (audit-seo/reports/), niezależnie od katalogu, z którego uruchomiono npm.
    const dir = fileURLToPath(new URL('reports/', import.meta.url));
    await mkdir(dir, { recursive: true });
    const abs = join(dir, `${new URL(startUrl).hostname.replaceAll('.', '-')}-${date}.md`);
    await writeFile(abs, report);
    // Ścieżka względem katalogu wywołania (INIT_CWD ustawia npm) — tę ścieżkę czyta hook check-review.sh.
    const file = relative(process.env.INIT_CWD ?? process.cwd(), abs);

    const statusLine = report.split('\n').find((l) => l.startsWith('- Status:'));
    console.log(`${file}\n${statusLine}`);
    process.exitCode = statusLine.includes('FAIL') ? 1 : 0;
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(`Audyt nie wykonał się: ${err.message}`);
  process.exit(2);
});
