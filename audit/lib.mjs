// Czysta logika audytu: reguły SEO, mapowanie wyników axe i render raportu.
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

const lengthIssue = (value, [min, max]) => value.length < min || value.length > max;

// facts — zebrane przez run.mjs dane o stronie (patrz collectFacts).
export function checkSeo(facts) {
  const out = [];
  const passed = [];
  const check = (id, failed) => (failed ? out.push(failed) : passed.push(id));

  check('seo-http-status', facts.status !== 200 &&
    finding('seo-http-status', 'error', `Strona zwraca HTTP ${facts.status}.`, 'Strona do indeksacji musi zwracać 200.'));

  check('seo-https', !facts.finalUrl.startsWith('https://') &&
    finding('seo-https', 'error', 'Strona nie działa na HTTPS.', 'Włącz HTTPS i przekieruj 301 z HTTP.'));

  check('seo-redirects', facts.redirects.length > 1 &&
    finding('seo-redirects', 'warning', `Łańcuch ${facts.redirects.length} przekierowań.`,
      'Skróć do jednego przekierowania 301.', facts.redirects));

  const noindex = [facts.robotsMeta, facts.xRobotsTag].some((v) => /noindex/i.test(v ?? ''));
  check('seo-noindex', noindex &&
    finding('seo-noindex', 'error', 'Strona ma noindex (meta robots lub X-Robots-Tag).',
      'Usuń noindex, jeśli strona ma być w Google.', [`meta: ${facts.robotsMeta}`, `header: ${facts.xRobotsTag}`]));

  const title = facts.title.trim();
  check('seo-title', !title
    ? finding('seo-title', 'error', 'Brak <title>.', 'Dodaj unikalny tytuł strony.')
    : lengthIssue(title, TITLE_RANGE) &&
      finding('seo-title', 'warning', `Tytuł ma ${title.length} znaków (zalecane ${TITLE_RANGE.join('–')}).`,
        'Dopasuj długość tytułu.', [title]));

  const description = (facts.metaDescription ?? '').trim();
  check('seo-meta-description', !description
    ? finding('seo-meta-description', 'warning', 'Brak meta description.', 'Dodaj opis strony.')
    : lengthIssue(description, DESCRIPTION_RANGE) &&
      finding('seo-meta-description', 'warning',
        `Meta description ma ${description.length} znaków (zalecane ${DESCRIPTION_RANGE.join('–')}).`,
        'Dopasuj długość opisu.', [description]));

  const canonicalFinding = () => {
    if (facts.canonicals.length === 0) return finding('seo-canonical', 'warning', 'Brak link rel=canonical.', 'Dodaj samoodwołujący się canonical.');
    if (facts.canonicals.length > 1) return finding('seo-canonical', 'error', `${facts.canonicals.length} tagi canonical.`, 'Zostaw jeden canonical.', facts.canonicals);
    if (facts.canonicals[0] !== facts.finalUrl) return finding('seo-canonical', 'warning', 'Canonical wskazuje inny URL niż strona.',
      'Sprawdź, czy to zamierzone.', [`canonical: ${facts.canonicals[0]}`, `strona: ${facts.finalUrl}`]);
    return false;
  };
  check('seo-canonical', canonicalFinding());

  check('seo-h1', facts.h1.length === 0
    ? finding('seo-h1', 'error', 'Brak nagłówka H1.', 'Dodaj jeden H1 opisujący temat strony.')
    : facts.h1.length > 1 &&
      finding('seo-h1', 'warning', `${facts.h1.length} nagłówki H1.`, 'Zostaw jeden H1.', facts.h1));

  check('seo-viewport', !facts.viewport &&
    finding('seo-viewport', 'error', 'Brak meta viewport.', 'Dodaj <meta name="viewport" content="width=device-width, initial-scale=1">.'));

  const missingOg = Object.entries(facts.og).filter(([, v]) => !v).map(([k]) => k);
  check('seo-open-graph', missingOg.length > 0 &&
    finding('seo-open-graph', 'warning', `Brak tagów Open Graph: ${missingOg.join(', ')}.`, 'Uzupełnij tagi og:*.'));

  const invalidJsonLd = facts.jsonLd.filter((b) => !b.valid);
  check('seo-structured-data', facts.jsonLd.length === 0
    ? finding('seo-structured-data', 'info', 'Brak danych strukturalnych JSON-LD.', 'Rozważ schema.org (np. Organization, WebSite).')
    : invalidJsonLd.length > 0 &&
      finding('seo-structured-data', 'error', `${invalidJsonLd.length} blok(i) JSON-LD z błędem składni.`, 'Popraw JSON.', invalidJsonLd.map((b) => b.error)));

  const robotsFinding = () => {
    if (facts.robots.status !== 200) return finding('seo-robots-txt', 'warning', `robots.txt zwraca HTTP ${facts.robots.status}.`, 'Dodaj /robots.txt.');
    if (robotsBlocksAll(facts.robots.body)) return finding('seo-robots-txt', 'error', 'robots.txt blokuje cały serwis (Disallow: / dla *).', 'Usuń blokadę.');
    if (sitemapUrlsFromRobots(facts.robots.body).length === 0) return finding('seo-robots-txt', 'warning', 'robots.txt nie wskazuje sitemapy.', 'Dodaj linię Sitemap: <url>.');
    return false;
  };
  check('seo-robots-txt', robotsFinding());

  check('seo-sitemap', facts.sitemap.status !== 200
    ? finding('seo-sitemap', 'warning', `Sitemap ${facts.sitemap.url} zwraca HTTP ${facts.sitemap.status}.`, 'Opublikuj sitemap.xml.')
    : facts.sitemap.locCount === 0 &&
      finding('seo-sitemap', 'warning', 'Sitemap nie zawiera żadnego <loc>.', 'Uzupełnij sitemapę.', [facts.sitemap.url]));

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
};
const ownIdFor = (category, auditId) => (category === 'accessibility' ? `a11y-${auditId}` : LH_TO_OWN[auditId]);

// Wynik kategorii = średnia ważona audytów (0–1). Utracone punkty audytu = (1 - wynik) * waga / suma wag * 100.
// ownFindingIds — id problemów z checkSeo/mapAxe; audyt bez odpowiednika dostaje własny finding `lh-<id>`.
export function mapLighthouse(lhr, ownFindingIds) {
  const categories = [];
  const findings = [];
  for (const id of ['seo', 'accessibility']) {
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

// Stała kolejność (ważność, potem id) — ten sam stan strony daje identyczny raport.
const sortFindings = (list) => [...list].sort((a, b) =>
  SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity) || a.id.localeCompare(b.id));

const code = (text) => `\`${String(text).replaceAll('`', "'")}\``;

const renderFinding = (f) => [
  `### [${f.severity}] ${f.id}`,
  '',
  `- Problem: ${f.message}`,
  `- Naprawa: ${f.fix}`,
  ...(f.details.length ? ['- Szczegóły:', ...f.details.map((d) => `  - ${code(d)}`)] : []),
  ...(f.nodes?.length ? [
    `- Elementy (${f.nodes.length} z ${f.totalNodes}):`,
    ...f.nodes.flatMap((n) => [
      `  - Selektor: ${code(n.selector)}`,
      ...(n.html ? [`    - HTML: ${code(n.html)}`] : []),
      ...(n.todo ? [`    - Do zrobienia: ${n.todo}`] : []),
    ]),
  ] : []),
  '',
];

const AGENT_GUIDE = [
  '## Jak czytać ten raport (dla agenta wdrażającego poprawki)',
  '',
  '1. Napraw najpierw `error`, potem `warning`; `info` i sekcja ręcznej weryfikacji wymagają oceny człowieka.',
  '2. Każdy problem ma id reguły, opis, sposób naprawy i listę elementów (selektor CSS + fragment HTML) — po nich znajdź miejsce w kodzie źródłowym.',
  '3. Kolumna „Zobacz” w tabeli Lighthouse wskazuje id problemu w tym raporcie, którego poprawa odzyska punkty.',
  '4. Po wdrożeniu poprawek uruchom audyt ponownie (komenda na dole); poprawka jest skuteczna, gdy problem znika z raportu.',
  '',
];

export function renderReport({ url, finalUrl, date, axeVersion, wcagTags, seo, a11y, lighthouse }) {
  const all = [...seo.findings, ...a11y.findings, ...lighthouse.findings];
  const count = (sev) => all.filter((f) => f.severity === sev).length;
  const status = count('error') > 0 ? 'FAIL' : 'PASS';
  const section = (title, list, empty) => [`## ${title}`, '', ...(list.length ? sortFindings(list).flatMap(renderFinding) : [empty, ''])];
  const seoIds = (f) => f.id.startsWith('seo-') || (f.id.startsWith('lh-') && lighthouse.categories.find((c) => c.id === 'seo').lost.some((l) => l.seeId === f.id));

  return [
    `# Audyt SEO i dostępności: ${url}`,
    '',
    `- Data: ${date}`,
    `- URL końcowy: ${finalUrl}`,
    `- Status: **${status}** (błędy: ${count('error')}, ostrzeżenia: ${count('warning')}, info: ${count('info')}, do ręcznej weryfikacji: ${a11y.manual.length})`,
    `- Wyniki Lighthouse: ${lighthouse.categories.map((c) => `${c.title} **${c.score}/100**`).join(', ')}`,
    `- Silniki: Lighthouse ${lighthouse.version} (${lighthouse.formFactor}), axe-core ${axeVersion} (tagi: ${wcagTags.join(', ')})`,
    '- Zakres: jedna strona; automaty wykrywają tylko część problemów WCAG, reszta wymaga testu ręcznego.',
    '',
    ...AGENT_GUIDE,
    '## Wyniki Lighthouse (0–100)',
    '',
    '| Kategoria | Wynik | Audyt bez punktów | Utracone pkt | Zobacz |',
    '|---|---|---|---|---|',
    ...lighthouse.categories.flatMap((c) => (c.lost.length
      ? c.lost.map((l, i) => `| ${i === 0 ? c.title : ''} | ${i === 0 ? c.score : ''} | ${l.title.replaceAll('|', '/')} | ${l.points} | ${l.seeId} |`)
      : [`| ${c.title} | ${c.score} | — | 0 | — |`])),
    '',
    ...section('SEO', [...seo.findings, ...lighthouse.findings.filter(seoIds)], 'Brak problemów.'),
    ...section('Dostępność (WCAG)', [...a11y.findings, ...lighthouse.findings.filter((f) => !seoIds(f))], 'Brak naruszeń wykrytych automatycznie.'),
    ...section('Do ręcznej weryfikacji (axe incomplete)', a11y.manual, 'Brak.'),
    '## Zaliczone reguły',
    '',
    [...seo.passed, ...a11y.passed].sort().join(', ') || 'Brak.',
    '',
    '## Ponowny audyt',
    '',
    `\`npm run audit -- ${url}\` w repozytorium audytu.`,
    '',
  ].join('\n');
}
