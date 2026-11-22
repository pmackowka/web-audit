# audit-seo

Deterministyczny audyt SEO i dostępności (WCAG) dowolnej strony. Kod (Playwright + axe-core + Lighthouse) ocenia stronę i generuje raport Markdown z wynikami 0–100 — ten sam stan strony daje ten sam raport.

## Uruchomienie

Z katalogu głównego repo:

```bash
npm --prefix audit-seo install && npx --prefix audit-seo playwright install chromium   # raz
npm --prefix audit-seo run audit -- https://example.com/
npm --prefix audit-seo test                                                             # testy reguł
```

W Claude Code: `/audit <url>` — audyt uruchamia agent `auditor` i dopisuje krytyczną ocenę opartą wyłącznie na raporcie (pilnują tego hooki).

## Co sprawdza

Strona startowa + do 9 adresów z sitemapy: Lighthouse (SEO, Accessibility, Best Practices, wersja mobilna), axe-core (WCAG 2.x A/AA), title, meta, canonical, H1, JSON-LD. Dla całego serwisu: robots.txt, sitemap, duplikaty title/description, do 100 linków wewnętrznych.

Kod wyjścia: 0 = PASS, 1 = FAIL (są błędy), 2 = audyt się nie wykonał.

## Wyniki (`reports/`)

- `<host>-<data>.md` — raport z kodu: wyniki, problemy z id reguły, selektorem i sposobem naprawy.
- `<host>-<data>.review.md` — ocena audytora (model) z priorytetami poprawek.
