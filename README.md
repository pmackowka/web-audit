# web-audit

Dwa niezależne audyty dowolnej strony. Każdy ma własny folder z kodem, instrukcją i wynikami w `reports/`:

| Folder | Audyt | Instrukcja |
|---|---|---|
| [`audit-seo/`](audit-seo/) | SEO i dostępność (WCAG) — Lighthouse 0–100, axe-core | [README](audit-seo/README.md) |
| [`audit-analytics/`](audit-analytics/) | Analityka i prywatność — GA4, GTM, Consent Mode v2, ciasteczka, wycieki danych, e-commerce dataLayer | [README](audit-analytics/README.md) |

Projekt powstał jako nauka Claude Code (MCP, skile, hooki, agenci); notatki są w [`docs/`](docs/).
