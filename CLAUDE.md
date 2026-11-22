# web-audit

Dwa niezależne audyty dowolnej strony, każdy w osobnym folderze z własnym kodem, zależnościami, README i raportami w `reports/`:

- `audit-seo/` — SEO i dostępność (WCAG). Node: Playwright + axe-core + Lighthouse, wyniki 0–100; model tylko uruchamia skrypt.
- `audit-analytics/` — analityka i prywatność (GA4, GTM, Consent Mode v2, ciasteczka, wycieki danych, e-commerce dataLayer). Python (uv) + Playwright; zasady i procedura w `audit-analytics/CLAUDE.md`.

Moduły nie dzielą kodu. Powstał jako projekt nauki Claude Code (MCP, skile, hooki, agenci) na przykładzie https://ntfy.pl/.

Folder lokalny: `~/Documents/dev/web-audit` | Repo: `github.com/pmackowka/web-audit`

Środowisko: macOS, zsh.

## Struktura projektu

| Ścieżka | Do czego służy |
|---------|----------------|
| `CLAUDE.md` | Ten plik. Claude wczytuje go automatycznie na początku każdej sesji. |
| `audit-seo/` | `run.mjs` (przeglądarka, sieć, Lighthouse, zapis raportu), `lib.mjs` (reguły SEO, mapowanie axe i Lighthouse, render), `lib.test.mjs`, `package.json`; raporty w `audit-seo/reports/`: `<host>-<data>.md` (z kodu) i `<host>-<data>.review.md` (ocena audytora). |
| `audit-analytics/` | `audit.py` (3 przebiegi zgód A/B/C, analiza, raport), `evidence.py` (plansze dowodowe z HAR), `test_audit.py`, `pyproject.toml`; raporty w `audit-analytics/reports/<data>-<firma>/` (`raw/` w `.gitignore`). |
| `.claude/settings.json` | Konfiguracja sesji: MCP serwer Playwright, uprawnienia, hooki, zmienna `AUDIT_URL`. |
| `.claude/commands/` | Komendy slash: `/seo-audit` (pełny audyt SEO), `/summarize` (podsumowanie sesji). |
| `.claude/agents/auditor.md` | Agent `auditor`: uruchamia audyt SEO i pisze krytyczną ocenę `*.review.md` opartą wyłącznie na raporcie; hooki we frontmatterze. |
| `.claude/skills/` | Skile: `/audit <url>` (audyt SEO w kontekście agenta `auditor`), `/analytics-audit <url> <firma>` (audyt analityki), `/audit-subpages`, `/compare-reports`. |
| `docs/` | Notatki z nauki — jeden plik Markdown na temat. |
| `hooks/` | `on-git-push.sh` (powiadomienie macOS po `git push`), `audit-guard.sh` (auditor może tylko uruchomić audyt i zapisać `*.review.md`), `check-review.sh` (ocena musi cytować tylko id z raportu). |

## Jak uruchomić audyt

- SEO: `/audit <url>` albo `npm --prefix audit-seo run audit -- <url>` z katalogu głównego (raz: `npm --prefix audit-seo install && npx --prefix audit-seo playwright install chromium`). Kod wyjścia: 0 = PASS, 1 = FAIL, 2 = audyt się nie wykonał. Szczegóły w `audit-seo/README.md`.
- Analityka: `/analytics-audit <url> <firma>` albo `cd audit-analytics && uv run audit.py <url> --slug <firma>`. Szczegóły w `audit-analytics/README.md`.
- Wariant LLM (niedeterministyczny, do nauki): `/seo-audit` — checklista z `.claude/commands/seo-audit.md` dla `$AUDIT_URL`.

## Tematy do nauki

- **MCP** — konfiguracja serwera Playwright w `settings.json`, narzędzia do kontroli przeglądarki
- **Skile** — tworzenie skili w `.claude/skills/nazwa/SKILL.md` (zalecany format wg Anthropic)
- **Komendy slash** — starszy format w `.claude/commands/`, nadal działa równolegle ze skilami
- **Hooki** — zdarzenie `PostToolUse` z matcherem `Bash`, wykrywanie `git push`, powiadomienia macOS
- **settings.json** — uprawnienia, zmienne env, MCP serwery
- **Agenci** — równoległe audyty wielu podstron (`/audit-subpages`, subagenci w Claude Code)
- **Pamięć** — porównywanie raportów między sesjami (system memory w `~/.claude/projects/-Users-p-Documents-dev-web-audit/memory/`)
