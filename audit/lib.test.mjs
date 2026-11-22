// Testy czystej logiki: parser robots.txt i reguły SEO na sztucznych faktach.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { checkSeo, mapLighthouse, robotsBlocksAll } from './lib.mjs';

test('robotsBlocksAll wykrywa Disallow: / tylko dla User-agent: *', () => {
  assert.equal(robotsBlocksAll('User-agent: *\nDisallow: /'), true);
  assert.equal(robotsBlocksAll('User-agent: BadBot\nDisallow: /\n\nUser-agent: *\nDisallow: /admin'), false);
  assert.equal(robotsBlocksAll('User-agent: BadBot\nUser-agent: *\nDisallow: / # wszystko'), true);
  assert.equal(robotsBlocksAll('User-agent: *\nDisallow:'), false);
});

const goodFacts = {
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
  robots: { status: 200, body: 'User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml' },
  sitemap: { url: 'https://example.com/sitemap.xml', status: 200, locCount: 3 },
};

test('poprawna strona nie ma findingów', () => {
  const { findings, passed } = checkSeo(goodFacts);
  assert.deepEqual(findings, []);
  assert.equal(passed.length, 13);
});

test('noindex, brak H1 i dwa canonicale to błędy', () => {
  const { findings } = checkSeo({
    ...goodFacts,
    robotsMeta: 'noindex, follow',
    h1: [],
    canonicals: ['https://example.com/', 'https://example.com/x'],
  });
  const errors = findings.filter((f) => f.severity === 'error').map((f) => f.id).sort();
  assert.deepEqual(errors, ['seo-canonical', 'seo-h1', 'seo-noindex']);
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
