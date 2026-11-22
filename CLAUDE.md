# web-audit

Projekt robi **deterministyczny audyt SEO i dostępności (WCAG) dowolnej strony**: kod (Playwright + axe-core + Lighthouse) ocenia stronę i daje wyniki 0–100, model tylko uruchamia skrypt. Powstał jako projekt nauki Claude Code (MCP, skile, hooki, agenci) na przykładzie https://ntfy.pl/.

Folder lokalny: `~/Documents/dev/web-audit` | Repo: `github.com/pmackowka/web-audit`

Środowisko: macOS, zsh.

## Struktura projektu

| Ścieżka | Do czego służy |
|---------|----------------|
| `CLAUDE.md` | Ten plik. Claude wczytuje go automatycznie na początku każdej sesji. |
| `audit/` | Deterministyczny audyt: `run.mjs` (przeglądarka, sieć, Lighthouse, zapis raportu), `lib.mjs` (reguły SEO, mapowanie axe i Lighthouse, render), `lib.test.mjs`. |
| `package.json` | Zależności (`playwright`, `@axe-core/playwright`, `lighthouse`) i skrypty `npm run audit`, `npm test`. |
| `.claude/settings.json` | Konfiguracja sesji: MCP serwer Playwright, uprawnienia, hooki, zmienna `AUDIT_URL`. |
| `.claude/commands/` | Komendy slash: `/seo-audit` (pełny audyt SEO), `/summarize` (podsumowanie sesji). |
| `.claude/skills/` | Skile: `/audit <url>` (deterministyczny audyt SEO + a11y), `/audit-subpages` (równoległy audyt podstron), `/compare-reports` (porównanie raportów). |
| `docs/` | Notatki z nauki — jeden plik Markdown na temat. |
| `hooks/` | Skrypty hooków. `on-git-push.sh` wysyła powiadomienie macOS gdy Claude wykona `git push`. |
| `reports/` | Wygenerowane raporty SEO w formacie Markdown. |

## Jak uruchomić audyt

Deterministycznie (zalecane) — w sesji `/audit https://pmdata.pl/` albo w terminalu bez Claude'a:

```
npm install && npx playwright install chromium   # jednorazowo
npm run audit -- https://pmdata.pl/
```

Raport trafia do `reports/<host>-<data>.md`. Kod wyjścia: 0 = PASS, 1 = FAIL (są błędy), 2 = audyt się nie wykonał. Ten sam stan strony daje identyczny raport. Zakres: jedna strona; axe wykrywa tylko część problemów WCAG.

Wariant LLM (niedeterministyczny, do nauki): `/seo-audit` — Claude przechodzi przez checklistę z `.claude/commands/seo-audit.md` dla `$AUDIT_URL`.

## Tematy do nauki

- **MCP** — konfiguracja serwera Playwright w `settings.json`, narzędzia do kontroli przeglądarki
- **Skile** — tworzenie skili w `.claude/skills/nazwa/SKILL.md` (zalecany format wg Anthropic)
- **Komendy slash** — starszy format w `.claude/commands/`, nadal działa równolegle ze skilami
- **Hooki** — zdarzenie `PostToolUse` z matcherem `Bash`, wykrywanie `git push`, powiadomienia macOS
- **settings.json** — uprawnienia, zmienne env, MCP serwery
- **Agenci** — równoległe audyty wielu podstron (`/audit-subpages`, subagenci w Claude Code)
- **Pamięć** — porównywanie raportów między sesjami (system memory w `~/.claude/projects/-Users-p-Documents-dev-web-audit/memory/`)
