// Czysta logika audytu: reguły SEO (strona i serwis), mapowanie wyników axe i Lighthouse, grupowanie i render raportu.
// Bez przeglądarki i sieci — te same fakty zawsze dają ten sam wynik, dlatego da się to testować.

export const SEVERITY_ORDER = ['error', 'warning', 'info'];

// Progi długości to konwencje branżowe (ucinanie w SERP), nie reguły Google.
const TITLE_RANGE = [30, 60];
const DESCRIPTION_RANGE = [70, 160];

const finding = (id, severity, message, fix, details = []) => ({ id, severity, message, fix, details });

// Czy robots.txt blokuje cały serwis dla `User-agent: *`.
// Grupy rozdziela kolejna linia User-agent po linii z regułą.
export function robotsBlocksAll(robotsTxt) {
  let groupAgents = [];
  let inRules = false;
  for (const raw of robotsTxt.split(/\r?\n/)) {
    const line = raw.replace(/#.*/, '').trim();
    const match = line.match(/^([a-z-]+)\s*:\s*(.*)$/i);
    if (!match) continue;
    const [, key, value] = match;
    const field = key.toLowerCase();
    if (field === 'user-agent') {
      if (inRules) { groupAgents = []; inRules = false; }
      groupAgents.push(value.trim());
    } else if (field === 'disallow' || field === 'allow') {
      inRules = true;
      if (field === 'disallow' && value.trim() === '/' && groupAgents.includes('*')) return true;
    }
  }
  return false;
}

export function sitemapUrlsFromRobots(robotsTxt) {
  return [...robotsTxt.matchAll(/^\s*sitemap\s*:\s*(\S+)/gim)].map((m) => m[1]);
}

const decodeXml = (s) => s.replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&quot;', '"').replaceAll('&apos;', "'").replaceAll('&amp;', '&');

// Sitemap może być listą stron (<urlset>) albo indeksem innych sitemap (<sitemapindex>).
export function parseSitemap(xml) {
  return {
    isIndex: /<sitemapindex[\s>]/i.test(xml),
    locs: [...xml.matchAll(/<loc>\s*(?:<!\[CDATA\[)?\s*([^<\]]+?)\s*(?:\]\]>)?\s*<\/loc>/gi)].map((m) => decodeXml(m[1])),
  };
}

const lengthIssue = (value, [min, max]) => value.length < min || value.length > max;

// Reguły pojedynczej strony. facts — dane zebrane przez run.mjs (collectFacts).
export function checkPage(facts) {
  const out = [];
  const passed = [];
  const check = (id, failed) => (failed ? out.push(failed) : passed.push(id));

  check('seo-http-status', facts.status !== 200 &&
    finding('seo-http-status', 'error', `Strona zwraca HTTP ${facts.status}.`, 'Strona do indeksacji musi zwracać 200.'));

  check('seo-https', !facts.finalUrl.startsWith('https://') &&
    finding('seo-https', 'error', 'Strona nie działa na HTTPS.', 'Włącz HTTPS i przekieruj 301 z HTTP.'));

  check('seo-redirects', facts.redirects.length > 1 &&
    finding('seo-redirects', 'warning', `Łańcuch ${facts.redirects.length - 1} przekierowań.`,
      'Linkuj bezpośrednio do adresu docelowego albo skróć łańcuch do jednego 301.', facts.redirects));

  const noindex = [facts.robotsMeta, facts.xRobotsTag].some((v) => /noindex/i.test(v ?? ''));
  check('seo-noindex', noindex &&
    finding('seo-noindex', 'error', 'Strona ma noindex (meta robots lub X-Robots-Tag).',
      'Usuń noindex, jeśli strona ma być w Google.', [`meta: ${facts.robotsMeta}`, `header: ${facts.xRobotsTag}`]));

  const title = facts.title.trim();
  check('seo-title', !title
    ? finding('seo-title', 'error', 'Brak <title>.', 'Dodaj unikalny tytuł strony.')
    : lengthIssue(title, TITLE_RANGE) &&
      finding('seo-title', 'warning', `Tytuł ma ${title.length} znaków (zalecane ${TITLE_RANGE.join('–')}).`,
        'Skróć albo wydłuż tytuł tak, żeby główna fraza była na początku i nie był ucinany w wynikach Google.', [title]));

  const description = (facts.metaDescription ?? '').trim();
  check('seo-meta-description', !description
    ? finding('seo-meta-description', 'warning', 'Brak meta description.', 'Dodaj <meta name="description"> opisujący stronę w 70–160 znakach.')
    : lengthIssue(description, DESCRIPTION_RANGE) &&
      finding('seo-meta-description', 'warning',
        `Meta description ma ${description.length} znaków (zalecane ${DESCRIPTION_RANGE.join('–')}).`,
        'Dopasuj długość opisu do 70–160 znaków.', [description]));

  const canonicalFinding = () => {
    if (facts.canonicals.length === 0) return finding('seo-canonical', 'warning', 'Brak link rel=canonical.', 'Dodaj <link rel="canonical"> wskazujący na adres tej strony.');
    if (facts.canonicals.length > 1) return finding('seo-canonical', 'error', `${facts.canonicals.length} tagi canonical.`, 'Zostaw jeden canonical.', facts.canonicals);
    if (facts.canonicals[0] !== facts.finalUrl) return finding('seo-canonical', 'warning', 'Canonical wskazuje inny URL niż strona.',
      'Sprawdź, czy to zamierzone; jeśli nie — ustaw canonical na adres tej strony.', [`canonical: ${facts.canonicals[0]}`, `strona: ${facts.finalUrl}`]);
    return false;
  };
  check('seo-canonical', canonicalFinding());

  check('seo-h1', facts.h1.length === 0
    ? finding('seo-h1', 'error', 'Brak nagłówka H1.', 'Dodaj jeden H1 opisujący temat strony.')
    : facts.h1.length > 1 &&
      finding('seo-h1', 'warning', `${facts.h1.length} nagłówki H1.`, 'Zostaw jeden H1, pozostałe zamień na H2.', facts.h1));

  check('seo-viewport', !facts.viewport &&
    finding('seo-viewport', 'error', 'Brak meta viewport.', 'Dodaj <meta name="viewport" content="width=device-width, initial-scale=1">.'));

  const missingOg = Object.entries(facts.og).filter(([, v]) => !v).map(([k]) => k);
  check('seo-open-graph', missingOg.length > 0 &&
    finding('seo-open-graph', 'warning', `Brak tagów Open Graph: ${missingOg.join(', ')}.`, 'Uzupełnij brakujące tagi og:* w <head>.'));

  const invalidJsonLd = facts.jsonLd.filter((b) => !b.valid);
  check('seo-structured-data', facts.jsonLd.length === 0
    ? finding('seo-structured-data', 'info', 'Brak danych strukturalnych JSON-LD.', 'Rozważ schema.org (np. Organization, WebSite, Article).')
    : invalidJsonLd.length > 0 &&
      finding('seo-structured-data', 'error', `${invalidJsonLd.length} blok(i) JSON-LD z błędem składni.`, 'Popraw JSON.', invalidJsonLd.map((b) => b.error)));

  return { findings: out, passed };
}

// Reguły całego serwisu: robots.txt, sitemap, duplikaty między stronami, niedziałające linki wewnętrzne.
export function checkSite(site) {
  const out = [];
  const passed = [];
  const check = (id, failed) => (failed ? out.push(failed) : passed.push(id));

  const robotsFinding = () => {
    if (site.robots.status !== 200) return finding('seo-robots-txt', 'warning', `robots.txt zwraca HTTP ${site.robots.status}.`, 'Dodaj /robots.txt.');
    if (robotsBlocksAll(site.robots.body)) return finding('seo-robots-txt', 'error', 'robots.txt blokuje cały serwis (Disallow: / dla *).', 'Usuń blokadę.');
    if (sitemapUrlsFromRobots(site.robots.body).length === 0) return finding('seo-robots-txt', 'warning', 'robots.txt nie wskazuje sitemapy.', 'Dodaj linię Sitemap: <url>.');
    return false;
  };
  check('seo-robots-txt', robotsFinding());

  check('seo-sitemap', site.sitemap.status !== 200
    ? finding('seo-sitemap', 'warning', `Sitemap ${site.sitemap.url} zwraca HTTP ${site.sitemap.status}.`, 'Opublikuj sitemap.xml i wskaż ją w robots.txt.')
    : site.sitemap.locCount === 0 &&
      finding('seo-sitemap', 'warning', 'Sitemap nie zawiera żadnego <loc>.', 'Uzupełnij sitemapę.', [site.sitemap.url]));

  // Duplikaty liczone tylko wśród stron, które zwróciły 200.
  const duplicates = (field) => {
    const groups = new Map();
    for (const page of site.pages.filter((p) => p.status === 200)) {
      const value = (page[field] ?? '').trim();
      if (value) groups.set(value, [...(groups.get(value) ?? []), page.url]);
    }
    return [...groups].filter(([, urls]) => urls.length > 1).sort(([a], [b]) => a.localeCompare(b))
      .map(([value, urls]) => `"${value}" → ${urls.join(', ')}`);
  };
  const dupTitles = duplicates('title');
  check('seo-duplicate-title', dupTitles.length > 0 &&
    finding('seo-duplicate-title', 'warning', `${dupTitles.length} tytuł(y) powtarza się na kilku stronach.`, 'Nadaj każdej stronie unikalny <title>.', dupTitles));
  const dupDescriptions = duplicates('metaDescription');
  check('seo-duplicate-description', dupDescriptions.length > 0 &&
    finding('seo-duplicate-description', 'warning', `${dupDescriptions.length} meta description powtarza się na kilku stronach.`, 'Nadaj każdej stronie unikalny opis.', dupDescriptions));

  check('seo-broken-links', site.links.broken.length > 0 &&
    finding('seo-broken-links', 'error',
      `${site.links.broken.length} z ${site.links.checked} sprawdzonych linków wewnętrznych zwraca błąd (wszystkich: ${site.links.total}).`,
      'Popraw adres linku albo przywróć stronę docelową (ewentualnie przekierowanie 301).',
      site.links.broken.map((l) => `HTTP ${l.status} ${l.url} ← linkowany z: ${l.sources.join(', ')}`)));

  return { findings: out, passed };
}

// Element strony, którego dotyczy problem: selektor CSS, fragment HTML i co konkretnie poprawić.
// Agent naprawiający stronę szuka po selektorze/HTML-u odpowiedniego miejsca w kodzie źródłowym.
const MAX_NODES = 10;
const MAX_HTML = 300;
const clip = (text, max) => (text.length > max ? `${text.slice(0, max)}…` : text);
// failureSummary z axe: nagłówek ("Fix any of the following:") + po jednym warunku w linii → jedna linia z separatorem "; ".
const joinSummary = (text) => {
  const [head, ...rest] = (text ?? '').split('\n').map((l) => l.trim()).filter(Boolean);
  return rest.length ? `${head} ${rest.join('; ')}` : head ?? '';
};
const node = (selector, html, todo) => ({
  selector,
  html: clip((html ?? '').replace(/\s+/g, ' ').trim(), MAX_HTML),
  todo: joinSummary(todo),
});
const limitNodes = (nodes) => [...nodes].sort((a, b) => a.selector.localeCompare(b.selector)).slice(0, MAX_NODES);

// axe: critical/serious → error, moderate/minor → warning.
// `incomplete` to przypadki, których axe nie umie rozstrzygnąć — idą do ręcznej weryfikacji, nie do błędów.
const axeFinding = (v, severity) => ({
  ...finding(`a11y-${v.id}`, severity, `${v.help} (${v.nodes.length} elem., impact: ${v.impact ?? 'n/d'}).`,
    `${v.description} Dokumentacja: ${v.helpUrl}`),
  nodes: limitNodes(v.nodes.map((n) => node(n.target.join(' '), n.html, n.failureSummary))),
  totalNodes: v.nodes.length,
});

export function mapAxe(results) {
  const findings = results.violations.map((v) => axeFinding(v, ['critical', 'serious'].includes(v.impact) ? 'error' : 'warning'));
  const manual = results.incomplete.map((v) => axeFinding(v, 'info'));
  const passed = results.passes.map((p) => `a11y-${p.id}`);
  return { findings, manual, passed };
}

export const LH_CATEGORIES = ['seo', 'accessibility', 'best-practices'];

// Audyty Lighthouse, które sprawdzamy już własną regułą — wtedy raport odsyła do niej zamiast dublować problem.
// Audyty dostępności Lighthouse to reguły axe o tych samych id.
const LH_TO_OWN = {
  'document-title': 'seo-title',
  'meta-description': 'seo-meta-description',
  'http-status-code': 'seo-http-status',
  canonical: 'seo-canonical',
  'robots-txt': 'seo-robots-txt',
  'is-crawlable': 'seo-noindex',
  'image-alt': 'a11y-image-alt',
  'is-on-https': 'seo-https',
};
const ownIdFor = (category, auditId) => (category === 'accessibility' ? `a11y-${auditId}` : LH_TO_OWN[auditId]);

// Wynik kategorii = średnia ważona audytów (0–1). Utracone punkty audytu = (1 - wynik) * waga / suma wag * 100.
// ownFindingIds — id problemów z checkPage/checkSite/mapAxe; audyt bez odpowiednika dostaje własny finding `lh-<id>`.
export function mapLighthouse(lhr, ownFindingIds) {
  const categories = [];
  const findings = [];
  for (const id of LH_CATEGORIES.filter((c) => lhr.categories[c])) {
    const category = lhr.categories[id];
    const scored = category.auditRefs.filter((ref) => ref.weight > 0 && lhr.audits[ref.id].score !== null);
    const totalWeight = scored.reduce((sum, ref) => sum + ref.weight, 0);
    const lost = [];
    for (const ref of scored) {
      const audit = lhr.audits[ref.id];
      if (audit.score >= 1) continue;
      const points = Math.round(((1 - audit.score) * ref.weight / totalWeight) * 1000) / 10;
      const own = ownIdFor(id, ref.id);
      const seeId = own && ownFindingIds.has(own) ? own : `lh-${ref.id}`;
      lost.push({ auditId: ref.id, title: audit.title, points, seeId });
      if (seeId.startsWith('lh-') && !findings.some((f) => f.id === seeId)) {
        const items = audit.details?.items ?? [];
        findings.push({
          ...finding(seeId, 'warning', `${audit.title} (Lighthouse, -${points} pkt w kategorii ${category.title}).`,
            audit.description.replace(/\s+/g, ' ')),
          category: id,
          nodes: limitNodes(items.filter((i) => i.node).map((i) => node(i.node.selector, i.node.snippet, i.node.explanation))),
          totalNodes: items.length,
        });
      }
    }
    lost.sort((a, b) => b.points - a.points || a.auditId.localeCompare(b.auditId));
    categories.push({ id, title: category.title, score: Math.round(category.score * 100), lost });
  }
  return { version: lhr.lighthouseVersion, formFactor: lhr.configSettings.formFactor, categories, findings };
}

const SECTIONS = [
  ['seo', 'SEO'],
  ['a11y', 'Dostępność (WCAG)'],
  ['bp', 'Dobre praktyki (Lighthouse)'],
];
const sectionOf = (f) => {
  if (f.id.startsWith('seo-')) return 'seo';
  if (f.id.startsWith('a11y-')) return 'a11y';
  return { seo: 'seo', accessibility: 'a11y' }[f.category] ?? 'bp';
};

// Łączy ten sam problem z wielu stron w jedną grupę: id → najgorsza waga + lista wystąpień (strona, opis, elementy).
// entries: [{ page: url | null (cały serwis), finding }]
export function groupFindings(entries) {
  const groups = new Map();
  for (const { page, finding: f } of entries) {
    const group = groups.get(f.id) ?? { id: f.id, severity: f.severity, fix: f.fix, section: sectionOf(f), items: [] };
    if (SEVERITY_ORDER.indexOf(f.severity) < SEVERITY_ORDER.indexOf(group.severity)) group.severity = f.severity;
    group.items.push({ page, message: f.message, details: f.details, nodes: f.nodes ?? [], totalNodes: f.totalNodes ?? 0 });
    groups.set(f.id, group);
  }
  return [...groups.values()]
    .map((g) => ({ ...g, items: [...g.items].sort((a, b) => (a.page ?? '').localeCompare(b.page ?? '')) }))
    .sort((a, b) => SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity) || a.id.localeCompare(b.id));
}

const code = (text) => `\`${String(text).replaceAll('`', "'")}\``;
const pathOf = (url, origin) => (url && url.startsWith(origin) ? url.slice(origin.length) || '/' : url ?? 'cały serwis');

const renderNodes = (nodes, indent) => nodes.flatMap((n) => [
  `${indent}- Selektor: ${code(n.selector)}`,
  ...(n.html ? [`${indent}  - HTML: ${code(n.html)}`] : []),
  ...(n.todo ? [`${indent}  - Do zrobienia: ${n.todo}`] : []),
]);

// Elementy pełne tylko przy pierwszej stronie; na kolejnych — gdy selektory się powtarzają (np. nawigacja), sam odsyłacz.
const renderGroup = (g, pagesTotal, origin) => {
  const pageCount = g.items.filter((i) => i.page).length;
  const scope = pageCount ? ` — ${pageCount} z ${pagesTotal} stron` : ' — cały serwis';
  const firstSelectors = new Set(g.items[0].nodes.map((n) => n.selector));
  return [
    `### [${g.severity}] ${g.id}${scope}`,
    '',
    `- Naprawa: ${g.fix}`,
    ...g.items.flatMap((item, index) => {
      const repeated = index > 0 && item.nodes.length > 0 && item.nodes.every((n) => firstSelectors.has(n.selector));
      return [
        `- Strona: ${pathOf(item.page, origin)}`,
        `  - Problem: ${item.message}`,
        ...item.details.map((d) => `  - Szczegół: ${code(d)}`),
        ...(item.nodes.length && repeated ? [`  - Elementy: ${item.totalNodes} — te same selektory co przy pierwszej stronie.`] : []),
        ...(item.nodes.length && !repeated ? [`  - Elementy (${item.nodes.length} z ${item.totalNodes}):`, ...renderNodes(item.nodes, '    ')] : []),
      ];
    }),
    '',
  ];
};

const AGENT_GUIDE = [
  '## Jak czytać ten raport (dla agenta wdrażającego poprawki)',
  '',
  '1. Raport wygenerował kod, nie model — liczby i listy problemów są powtarzalne dla tego samego stanu strony.',
  '2. Napraw najpierw `error`, potem `warning`; `info` i sekcja ręcznej weryfikacji wymagają oceny człowieka.',
  '3. Każdy problem ma id reguły, sposób naprawy, strony, na których wystąpił, i elementy (selektor CSS + HTML) — po nich znajdź miejsce w kodzie źródłowym. Problem na wielu stronach zwykle oznacza wspólny komponent (nagłówek, stopka, szablon).',
  '4. Tabela utraconych punktów wskazuje id problemu, którego poprawa podniesie wynik Lighthouse.',
  '5. Po wdrożeniu uruchom audyt ponownie (komenda na dole); poprawka jest skuteczna, gdy problem znika z raportu.',
  '',
];

const avg = (values) => (values.length ? Math.round(values.reduce((a, b) => a + b, 0) / values.length) : '—');

// pages: [{ url, status, lighthouse: mapLighthouse(...) | null, error?: string }]
export function renderReport({ url, date, engines, wcagTags, pages, groups, manualGroups, passed }) {
  const origin = new URL(url).origin;
  const count = (sev) => groups.filter((g) => g.severity === sev).length;
  const status = count('error') > 0 ? 'FAIL' : 'PASS';
  const scoreOf = (page, id) => page.lighthouse?.categories.find((c) => c.id === id)?.score;
  const categoryTitles = LH_CATEGORIES.map((id) => pages.find((p) => p.lighthouse)?.lighthouse.categories.find((c) => c.id === id)?.title ?? id);
  const averages = LH_CATEGORIES.map((id) => avg(pages.map((p) => scoreOf(p, id)).filter((s) => s !== undefined)));
  const severityOn = (page, sev) => groups.filter((g) => g.severity === sev && g.items.some((i) => i.page === page.url)).length;

  // Utracone punkty zsumowane po stronach i podzielone przez liczbę stron = wkład audytu w średni wynik.
  const lost = new Map();
  for (const page of pages) {
    for (const c of page.lighthouse?.categories ?? []) {
      for (const l of c.lost) {
        const key = `${c.title}|${l.auditId}`;
        const entry = lost.get(key) ?? { category: c.title, title: l.title, seeId: l.seeId, pages: 0, points: 0 };
        entry.pages += 1;
        entry.points += l.points;
        lost.set(key, entry);
      }
    }
  }
  const audited = pages.filter((p) => p.lighthouse).length || 1;
  const lostRows = [...lost.values()]
    .map((e) => ({ ...e, avgPoints: Math.round((e.points / audited) * 10) / 10 }))
    .sort((a, b) => b.avgPoints - a.avgPoints || a.category.localeCompare(b.category) || a.title.localeCompare(b.title));

  const section = (key, title) => {
    const list = groups.filter((g) => g.section === key);
    return [`## ${title}`, '', ...(list.length ? list.flatMap((g) => renderGroup(g, pages.length, origin)) : ['Brak problemów wykrytych automatycznie.', ''])];
  };

  return [
    `# Audyt SEO i dostępności: ${url}`,
    '',
    `- Data: ${date}`,
    `- Status: **${status}** (problemy: błędy ${count('error')}, ostrzeżenia ${count('warning')}, info ${count('info')}, do ręcznej weryfikacji ${manualGroups.length})`,
    `- Średnie wyniki Lighthouse (${audited} str.): ${categoryTitles.map((t, i) => `${t} **${averages[i]}/100**`).join(', ')}`,
    `- Zakres: ${pages.length} stron (strona startowa + kolejne adresy z sitemapy), robots.txt, sitemap, linki wewnętrzne`,
    `- Silniki: ${engines}, axe tagi: ${wcagTags.join(', ')}`,
    '- Nie sprawdzono: wydajności (Core Web Vitals), treści i jej jakości, profilu linków zewnętrznych, obsługi klawiaturą i czytnikiem ekranu (test ręczny).',
    '',
    ...AGENT_GUIDE,
    '## Strony',
    '',
    `| Strona | HTTP | ${categoryTitles.join(' | ')} | Błędy | Ostrzeżenia |`,
    `|---|---|${categoryTitles.map(() => '---|').join('')}---|---|`,
    ...pages.map((p) => `| ${pathOf(p.url, origin)} | ${p.error ? `błąd: ${p.error.replaceAll('|', '/')}` : p.status} | ${LH_CATEGORIES.map((id) => scoreOf(p, id) ?? '—').join(' | ')} | ${severityOn(p, 'error')} | ${severityOn(p, 'warning')} |`),
    `| **Średnia** | | ${averages.join(' | ')} | | |`,
    '',
    '## Utracone punkty Lighthouse',
    '',
    ...(lostRows.length ? [
      '| Kategoria | Audyt | Stron | Śr. utrata pkt | Zobacz |',
      '|---|---|---|---|---|',
      ...lostRows.map((r) => `| ${r.category} | ${r.title.replaceAll('|', '/')} | ${r.pages} | ${r.avgPoints} | ${r.seeId} |`),
    ] : ['Brak — wszystkie strony mają 100 we wszystkich kategoriach.']),
    '',
    ...SECTIONS.flatMap(([key, title]) => section(key, title)),
    '## Do ręcznej weryfikacji (axe incomplete)',
    '',
    ...(manualGroups.length ? manualGroups.flatMap((g) => renderGroup(g, pages.length, origin)) : ['Brak.', '']),
    '## Zaliczone reguły (na wszystkich stronach)',
    '',
    passed.length ? passed.join(', ') : 'Brak.',
    '',
    '## Ponowny audyt',
    '',
    `\`npm run audit -- ${url}\` w repozytorium web-audit.`,
    '',
  ].join('\n');
}
