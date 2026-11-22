// Uruchomienie: npm run audit -- https://example.com/
// Otwiera stronę w Chromium (Playwright), zbiera fakty SEO, odpala axe-core i Lighthouse, zapisuje raport Markdown do reports/.
// Kod wyjścia: 0 = brak błędów, 1 = są błędy (status FAIL), 2 = audyt się nie wykonał.
import { mkdir, writeFile } from 'node:fs/promises';
import { createServer } from 'node:net';
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
import lighthouse from 'lighthouse';
import { checkSeo, mapAxe, mapLighthouse, renderReport, sitemapUrlsFromRobots } from './lib.mjs';

const WCAG_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];

// Wolny port dla Chrome DevTools Protocol — stały 9222 mógłby trafić w inną, już otwartą przeglądarkę.
function freePort() {
  return new Promise((resolve, reject) => {
    const server = createServer().listen(0, () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    }).on('error', reject);
  });
}

async function fetchText(url) {
  try {
    const res = await fetch(url, { redirect: 'follow' });
    return { status: res.status, body: res.ok ? await res.text() : '' };
  } catch (err) {
    return { status: 0, body: '', error: err.message };
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
    };
  });

  const jsonLd = dom.jsonLdRaw.map((raw) => {
    try { JSON.parse(raw); return { valid: true }; } catch (err) { return { valid: false, error: err.message }; }
  });

  const origin = new URL(page.url()).origin;
  const robots = await fetchText(`${origin}/robots.txt`);
  const sitemapUrl = sitemapUrlsFromRobots(robots.body)[0] ?? `${origin}/sitemap.xml`;
  const sitemapRes = await fetchText(sitemapUrl);

  return {
    status: response.status(),
    finalUrl: page.url(),
    redirects: redirects.length > 1 ? redirects : [],
    xRobotsTag: response.headers()['x-robots-tag'] ?? null,
    ...dom,
    jsonLd,
    robots,
    sitemap: { url: sitemapUrl, status: sitemapRes.status, locCount: (sitemapRes.body.match(/<loc>/g) ?? []).length },
  };
}

async function main() {
  const input = process.argv[2];
  let url;
  try {
    url = new URL(input).href;
  } catch {
    console.error('Użycie: npm run audit -- https://example.com/');
    process.exit(2);
  }

  // Lighthouse łączy się z tym samym Chromium przez CDP i otwiera w nim własną kartę.
  const port = await freePort();
  const browser = await chromium.launch({ args: [`--remote-debugging-port=${port}`] });
  try {
    const page = await (await browser.newContext()).newPage();
    const response = await page.goto(url, { waitUntil: 'networkidle' });
    if (!response) throw new Error(`Brak odpowiedzi dla ${url}`);

    const facts = await collectFacts(page, response);
    const axeResults = await new AxeBuilder({ page }).withTags(WCAG_TAGS).analyze();
    const seo = checkSeo(facts);
    const a11y = mapAxe(axeResults);

    const lhResult = await lighthouse(url, { port, logLevel: 'error', onlyCategories: ['seo', 'accessibility'] });
    if (!lhResult) throw new Error('Lighthouse nie zwrócił wyniku');
    const ownIds = new Set([...seo.findings, ...a11y.findings].map((f) => f.id));

    const date = new Date().toISOString().slice(0, 10);
    const report = renderReport({
      url,
      finalUrl: facts.finalUrl,
      date,
      axeVersion: axeResults.testEngine.version,
      wcagTags: WCAG_TAGS,
      seo,
      a11y,
      lighthouse: mapLighthouse(lhResult.lhr, ownIds),
    });

    const file = `reports/${new URL(url).hostname.replaceAll('.', '-')}-${date}.md`;
    await mkdir('reports', { recursive: true });
    await writeFile(file, report);

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
