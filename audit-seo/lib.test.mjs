// Testy czystej logiki: parsery (robots.txt, sitemap), reguły strony i serwisu, punktacja Lighthouse, grupowanie.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { checkPage, checkSite, groupFindings, mapLighthouse, parseSitemap, robotsBlocksAll } from './lib.mjs';

test('robotsBlocksAll wykrywa Disallow: / tylko dla User-agent: *', () => {
  assert.equal(robotsBlocksAll('User-agent: *\nDisallow: /'), true);
  assert.equal(robotsBlocksAll('User-agent: BadBot\nDisallow: /\n\nUser-agent: *\nDisallow: /admin'), false);
  assert.equal(robotsBlocksAll('User-agent: BadBot\nUser-agent: *\nDisallow: / # wszystko'), true);
  assert.equal(robotsBlocksAll('User-agent: *\nDisallow:'), false);
});

test('parseSitemap rozpoznaje indeks, CDATA i encje', () => {
  assert.deepEqual(parseSitemap('<sitemapindex><sitemap><loc>https://a.pl/s1.xml</loc></sitemap></sitemapindex>'),
    { isIndex: true, locs: ['https://a.pl/s1.xml'] });
  assert.deepEqual(parseSitemap('<urlset><url><loc> https://a.pl/?a=1&amp;b=2 </loc></url><url><loc><![CDATA[https://a.pl/x]]></loc></url></urlset>'),
    { isIndex: false, locs: ['https://a.pl/?a=1&b=2', 'https://a.pl/x'] });
});

const goodPage = {
  status: 200,
  finalUrl: 'https://example.com/',
  redirects: [],
  xRobotsTag: null,
  robotsMeta: null,
  title: 'Przykładowy tytuł strony o odpowiedniej długości',
  metaDescription: 'Opis strony, który ma odpowiednią długość, żeby nie był ucięty w wynikach wyszukiwania.',
  canonicals: ['https://example.com/'],
  h1: ['Nagłówek'],
  viewport: 'width=device-width, initial-scale=1',
  og: { 'og:title': 'a', 'og:description': 'b', 'og:image': 'c' },
  jsonLd: [{ valid: true }],
};

test('poprawna strona nie ma findingów', () => {
  const { findings, passed } = checkPage(goodPage);
  assert.deepEqual(findings, []);
  assert.equal(passed.length, 11);
});

test('noindex, brak H1 i dwa canonicale to błędy', () => {
  const { findings } = checkPage({
    ...goodPage,
    robotsMeta: 'noindex, follow',
    h1: [],
    canonicals: ['https://example.com/', 'https://example.com/x'],
  });
  const errors = findings.filter((f) => f.severity === 'error').map((f) => f.id).sort();
  assert.deepEqual(errors, ['seo-canonical', 'seo-h1', 'seo-noindex']);
});

test('checkSite wykrywa duplikaty tytułów i niedziałające linki', () => {
  const { findings } = checkSite({
    robots: { status: 200, body: 'User-agent: *\nAllow: /\nSitemap: https://a.pl/sitemap.xml' },
    sitemap: { url: 'https://a.pl/sitemap.xml', status: 200, locCount: 3 },
    pages: [
      { url: 'https://a.pl/', status: 200, title: 'Ten sam', metaDescription: 'A' },
      { url: 'https://a.pl/b', status: 200, title: 'Ten sam', metaDescription: 'B' },
      { url: 'https://a.pl/c', status: 404, title: 'Ten sam', metaDescription: 'A' },
    ],
    links: { total: 2, checked: 2, broken: [{ url: 'https://a.pl/x', status: 404, sources: ['https://a.pl/'] }] },
  });
  assert.deepEqual(findings.map((f) => f.id), ['seo-duplicate-title', 'seo-broken-links']);
  assert.deepEqual(findings[0].details, ['"Ten sam" → https://a.pl/, https://a.pl/b']);
});

test('mapLighthouse liczy utracone punkty i odsyła do własnego findingu', () => {
  const lhr = {
    lighthouseVersion: 'x',
    configSettings: { formFactor: 'mobile' },
    categories: {
      seo: { title: 'SEO', score: 0.75, auditRefs: [{ id: 'canonical', weight: 1 }, { id: 'hreflang', weight: 3 }, { id: 'structured-data', weight: 0 }] },
      accessibility: { title: 'Accessibility', score: 1, auditRefs: [{ id: 'label', weight: 7 }] },
    },
    audits: {
      canonical: { score: 0, title: 'Canonical', description: 'd' },
      hreflang: { score: 1, title: 'Hreflang', description: 'd' },
      'structured-data': { score: null, title: 'SD', description: 'd' },
      label: { score: 1, title: 'Label', description: 'd' },
    },
  };
  const result = mapLighthouse(lhr, new Set(['seo-canonical']));
  const seo = result.categories.find((c) => c.id === 'seo');
  assert.equal(seo.score, 75);
  assert.deepEqual(seo.lost, [{ auditId: 'canonical', title: 'Canonical', points: 25, seeId: 'seo-canonical' }]);
  assert.deepEqual(result.findings, []);
});

test('groupFindings łączy ten sam problem z wielu stron i bierze najgorszą wagę', () => {
  const f = (severity) => ({ id: 'seo-h1', severity, message: 'm', fix: 'x', details: [] });
  const groups = groupFindings([
    { page: 'https://a.pl/b', finding: f('warning') },
    { page: 'https://a.pl/', finding: f('error') },
  ]);
  assert.equal(groups.length, 1);
  assert.equal(groups[0].severity, 'error');
  assert.deepEqual(groups[0].items.map((i) => i.page), ['https://a.pl/', 'https://a.pl/b']);
});
