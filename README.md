# web-audit

Dwa niezależne audyty dowolnej strony: SEO i dostępność (WCAG) w `audit/` oraz analityka i prywatność (GA4, GTM, Consent Mode v2, ciasteczka, wycieki danych, e-commerce dataLayer) w `analytics/`. W audycie SEO kod (Playwright + axe-core + Lighthouse) ocenia stronę i generuje raport Markdown, który agent wdrażający poprawki może przyjąć jako wsad. Projekt powstał jako nauka Claude Code (MCP, skile, hooki, agenci) — stąd wariant LLM i notatki w `docs/`.

## Jak uruchomić audyt

Deterministyczny audyt SEO i dostępności (Playwright + axe-core + Lighthouse, wyniki 0–100) dowolnej strony:

```
npm install && npx playwright install chromium   # jednorazowo
npm run audit -- https://pmdata.pl/              # albo w sesji: /audit https://pmdata.pl/
```

Raport: `reports/<host>-<data>.md` (strona startowa + do 9 adresów z sitemapy). Kod wyjścia: 0 = PASS, 1 = FAIL, 2 = błąd uruchomienia. Testy reguł: `npm test`. W sesji `/audit <url>` agent `auditor` dopisuje krytyczną ocenę `reports/<host>-<data>.review.md` — opartą wyłącznie na raporcie (pilnują tego hooki).

Pasywny audyt analityki i prywatności (Python, uv) — szczegóły w [`analytics/README.md`](analytics/README.md):

```
cd analytics
uv sync && uv run playwright install chromium   # jednorazowo
uv run audit.py https://example.com --slug example   # albo w sesji: /analytics-audit <url> <firma>
```

Raport: `reports/analytics/<data>-<firma>/RAPORT.md` z planszami dowodowymi i surowym ruchem w `raw/` (tylko lokalnie, w `.gitignore`). Testy: `uv run python -m unittest test_audit.py`.

Wariant LLM (niedeterministyczny, do nauki):

```
/seo-audit
```

---

## Struktura projektu

```
web-audit/
│
├── analytics/                       # audyt analityki i prywatności (Python): audit.py, evidence.py,
│                                    # test_audit.py, report_template.md, pyproject.toml
│
├── audit/                           # deterministyczny audyt: run.mjs (przeglądarka, Lighthouse, zapis),
│                                    # lib.mjs (reguły SEO, mapowanie axe/Lighthouse, render), lib.test.mjs
├── package.json                     # zależności: playwright, @axe-core/playwright, lighthouse; skrypty audit/test
├── .mcp.json                        # rejestracja serwera MCP Playwright (dla wariantu LLM)
├── CLAUDE.md                        # instrukcje dla Claude — wczytywane automatycznie na starcie każdej sesji
├── README.md                        # ten plik — mapa projektu dla człowieka
│
├── .claude/
│   ├── settings.json                # konfiguracja sesji Claude Code:
│   │                                #   • env: AUDIT_URL — domyślny adres dla /seo-audit
│   │                                #   • hooks: rejestracja skryptu on-git-push.sh
│   │                                #   • permissions: lista dozwolonych/blokowanych operacji
│   │
│   ├── agents/auditor.md            # niezależny, krytyczny audytor: uruchamia audyt, pisze *.review.md; hooki we frontmatterze
│   ├── skills/audit/SKILL.md        # /audit <url> — context: fork, agent: auditor (osobny kontekst na każdą domenę)
│   │
│   └── commands/
│       └── seo-audit.md             # komenda /seo-audit — profesjonalny framework audytu SEO v2.0
│                                    # źródło: github.com/coreyhaines31/marketingskills/skills/seo-audit
│                                    # sprawdza: title, meta, H1-H3, OG, canonical, alt, HTTPS,
│                                    # viewport, robots.txt, sitemap, linki, schema, Core Web Vitals
│
├── docs/                            # notatki z nauki — jeden plik .md na temat (uzupełniaj w trakcie)
│
├── hooks/
│   └── on-git-push.sh               # uruchamiany przez Claude Code po wywołaniu narzędzia Bash (PostToolUse)
│                                    # wysyła natywne powiadomienie macOS gdy Claude wykona git push
│   ├── audit-guard.sh               # PreToolUse auditora: tylko `npm run audit -s -- <url>` i zapis *.review.md
│   └── check-review.sh              # Stop auditora: ocena musi istnieć i cytować tylko id z raportu
│
└── reports/                         # <host>-YYYY-MM-DD.md (raport z kodu) + <host>-YYYY-MM-DD.review.md (ocena modelu)
```

---

## Konfiguracja `settings.json` — linia po linii

Plik `.claude/settings.json` konfiguruje sesję Claude Code; serwery MCP są osobno w `.mcp.json`. Poniżej skrót z wyjaśnieniem (styl JSONC — `//` to komentarze, nie są częścią prawdziwego pliku JSON):

```jsonc
{
  // ── PERMISSIONS ──────────────────────────────────────────────────────────
  // Kontrola nad tym, o co Claude Code pyta użytkownika przed wykonaniem akcji.
  "permissions": {
    "allow": [
      // Wzorce komend Bash, które NIE wymagają potwierdzenia użytkownika.
      // Format: Bash(wzorzec) — gwiazdka (*) to wildcard dla dowolnych argumentów.
      "Bash(curl -sI *)",        // HEAD requesty HTTP (np. sprawdzanie nagłówków strony)
      "Bash(curl -s https://*)"  // GET requesty HTTPS (np. pobieranie sitemap, API GitHub)
    ],
    "deny": []  // komendy całkowicie zablokowane — tu: brak, nic nie blokujemy jawnie
  },

  // ── HOOKS ────────────────────────────────────────────────────────────────
  // Skrypty uruchamiane automatycznie w odpowiedzi na zdarzenia Claude Code.
  "hooks": {
    "PostToolUse": [            // zdarzenie: po każdym użyciu narzędzia przez Claude
      {
        "matcher": "Bash",      // filtr: reaguj tylko gdy narzędziem był Bash
        "hooks": [
          {
            "type": "command",                      // typ hooka: uruchom polecenie shell
            "command": "hooks/on-git-push.sh"       // skrypt sprawdza, czy Bash wykonał git push
                                                    // jeśli tak → wysyła natywne powiadomienie macOS
          }
        ]
      }
    ]
  },

  // ── ENV ──────────────────────────────────────────────────────────────────
  // Zmienne środowiskowe dostępne w sesjach Claude Code i w plikach komend slash.
  "env": {
    "AUDIT_URL": "https://pmdata.pl/"  // URL audytowanej strony — użyj $AUDIT_URL w komendach
                                     // zmień tę wartość, żeby audytować inną stronę
  }
}
```

---

## Jak to działa

Wariant deterministyczny (`/audit <url>` albo `npm run audit -- <url>`):

1. `audit/run.mjs` otwiera stronę startową i do 9 adresów z sitemapy w Chromium (Playwright) i zbiera fakty SEO (title, meta, canonical, H1, JSON-LD, linki).
2. Na każdej stronie axe-core sprawdza reguły WCAG 2.x A/AA, Lighthouse liczy wyniki SEO, Accessibility i Best Practices 0–100.
3. Reguły serwisu: robots.txt, sitemap, duplikaty title/description, do 100 linków wewnętrznych (statusy HTTP).
4. `audit/lib.mjs` grupuje ten sam problem z wielu stron (wspólny komponent), dodaje id reguły, naprawę, selektor + HTML i renderuje raport do `reports/`.
5. Przy `/audit <url>` agent `auditor` czyta raport i zapisuje krytyczną ocenę `*.review.md`; `audit-guard.sh` blokuje mu edycję raportu, `check-review.sh` odrzuca id spoza raportu.

Wariant LLM (`/seo-audit`):

1. Claude Code startuje sesję → wczytuje `CLAUDE.md`, `settings.json` i `.mcp.json`
2. `.mcp.json` rejestruje serwer MCP Playwright → Claude ma dostęp do przeglądarki
3. Wpisujesz `/seo-audit` → Claude dostaje instrukcje z `.claude/commands/seo-audit.md`
4. Claude otwiera `$AUDIT_URL` przez Playwright → czyta DOM, sprawdza wszystkie elementy SEO
5. Zapisuje raport do `reports/` → hook `on-git-push.sh` wysyła powiadomienie macOS gdy zmiany trafią na remote

---

## Własne komendy slash — jak działa `/seo-audit`

### Skąd Claude wie, że `/seo-audit` istnieje?

Claude Code automatycznie skanuje folder `.claude/commands/` w katalogu projektu przy starcie sesji. Każdy plik `.md` znaleziony w tym folderze staje się dostępną komendą slash — nazwa pliku (bez rozszerzenia) to nazwa komendy.

```
.claude/
└── commands/
    └── seo-audit.md   →   /seo-audit
    └── summarize.md   →   /summarize
```

Żeby stworzyć własną komendę `/cokolwiek`, wystarczy umieścić plik `cokolwiek.md` w `.claude/commands/`. Nie trzeba nigdzie rejestrować ani restartować — Claude widzi plik od razu w nowej sesji.

### Co zawiera plik komendy?

Plik `seo-audit.md` to zwykły Markdown z opcjonalnym frontmatter YAML na górze:

```markdown
---
name: seo-audit
description: When the user wants to audit...
---

# SEO Audit

Tutaj właściwe instrukcje dla Claude — co ma zrobić,
krok po kroku, jakich narzędzi użyć, jak zapisać wynik.
```

- **`name`** — wyświetlana nazwa (opcjonalne, domyślnie nazwa pliku)
- **`description`** — Claude używa tego opisu, żeby rozpoznać intencję użytkownika i zaproponować komendę nawet bez `/` (np. gdy piszesz „zrób audyt SEO")
- **Treść** — to są dosłowne instrukcje, które Claude dostaje jako kontekst po wpisaniu komendy

### Zmienne środowiskowe w komendzie

W treści pliku możesz używać zmiennych z `settings.json`. W `seo-audit.md` jest np.:

```
Audytowana strona: $AUDIT_URL
```

`$AUDIT_URL` pochodzi z sekcji `env` w `.claude/settings.json`:

```json
"env": {
  "AUDIT_URL": "https://pmdata.pl/"
}
```

Żeby audytować inną stronę, wystarczy zmienić wartość `AUDIT_URL` w `settings.json` — bez edytowania samej komendy.

### Zasięg komend — projekt vs. globalny

| Lokalizacja pliku | Widoczność |
|-------------------|-----------|
| `.claude/commands/` (w projekcie) | tylko w tym projekcie |
| `~/.claude/commands/` (katalog domowy) | we wszystkich projektach |

Komendy projektowe nadpisują globalne, jeśli mają tę samą nazwę.

---

## Custom subagent — `@seo-specialist`

### Czym różni się agent od komendy slash?

| Mechanizm | Co to jest | System prompt | Przykład |
|-----------|-----------|---------------|----------|
| **Komenda** `/seo-audit` | Instrukcja wklejona jako wiadomość użytkownika | Tylko domyślny prompt Claude Code | `/seo-audit` |
| **Agent** `seo-specialist` | Własny system prompt + własny kontekst | "Jesteś ekspertem SEO..." + domyślny prompt CC | `@seo-specialist /seo-audit` |

Agent daje ci **dodatkową warstwę system promptu** — możesz powiedzieć mu kim jest, jakie ma priorytety i jak ma pracować. Gdy połączysz agenta z komendą (`@seo-specialist /seo-audit`), dostajesz **system prompt (agent) + instrukcję (komenda)** — dwa w jednym.

### Plik agenta

`.claude/agents/seo-specialist.md`:
```markdown
---
name: seo-specialist
description: Specjalista SEO do audytu i optymalizacji stron...
tools: Read, Write, Bash, WebFetch, Glob, Grep, Agent
model: sonnet
skills:
  - audit-subpages
  - compare-reports
memory: project
---

Jesteś ekspertem SEO...
```

Kluczowe różnice vs. komenda:
- **Frontmatter** zawiera `tools` (lista dozwolonych narzędzi), `model` (może być inny niż sesja główna), `skills` (preloadowane skille — agent od razu ma ich treść w kontekście), `memory` (trwała pamięć między sesjami)
- **Body** to system prompt agenta — nie instrukcja do wykonania, tylko definicja kim jest

### Jak wywoływać

| Sposób | Przykład | Efekt |
|--------|----------|-------|
| `@`-mention | `@seo-specialist /seo-audit` | Agent + komenda — najpełniejszy przekaz |
| `@`-mention + opis | `@seo-specialist sprawdź SEO pmdata.pl` | Agent sam decyduje co zrobić |
| Natural language | *"Użyj seo-specialist do audytu"* | Claude decyduje czy delegować |
| CLI flag | `claude --agent seo-specialist` | Cała sesja działa jako ten agent |
| Ustawienie stałe | `"agent": "seo-specialist"` w settings.json | Domyślny agent dla projektu |

### Kiedy agent się ładuje?

Przy starcie sesji. Jeśli dodajesz/edytujesz plik `.claude/agents/*.md` — **zrestartuj sesję**. Wyjątek: tworzenie przez `/agents` działa od razu.

### Dokumentacja

Źródło: https://code.claude.com/docs/en/sub-agents — rozdział "Invoke subagents explicitly" o `@`-mention.

---

## MCP i Playwright — jak to naprawdę działa

### Co to jest MCP?

MCP (Model Context Protocol) to protokół, który pozwala Claude Code korzystać z zewnętrznych narzędzi — tu: z przeglądarki Chrome przez Playwright. Konfiguracja w `.mcp.json` startuje serwer MCP jako osobny proces (`@playwright/mcp`), a Claude komunikuje się z nim przez standardowe wejście/wyjście (stdio).

### Headless vs. widoczna przeglądarka

**Domyślnie przeglądarka NIE jest widoczna** — Playwright uruchamia Chromium w trybie headless (bez GUI). Claude otwiera strony, czyta ich zawartość i wykonuje akcje, ale nie zobaczysz żadnego okna przeglądarki na ekranie.

Żeby przeglądarka była widoczna, trzeba uruchomić MCP z flagą `--headed` w `.mcp.json`:

```json
"mcpServers": {
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest", "--headed"]
  }
}
```

Po tej zmianie (i restarcie sesji Claude Code) Chromium otworzy się jako widoczne okno — będziesz widzieć, jak Claude nawiguje po stronie.

### Co Claude robi przez MCP — narzędzia Playwright

Claude nie „klika jak człowiek" — wysyła kolejne wywołania narzędzi do serwera MCP. W praktyce wywołuje m.in.:

| Narzędzie MCP | Co robi |
|---------------|---------|
| `browser_navigate` | Otwiera URL w przeglądarce |
| `browser_snapshot` | Pobiera dostępnościowy snapshot DOM (tekst, atrybuty, struktura) |
| `browser_click` | Klika element na stronie |
| `browser_screenshot` | Robi zrzut ekranu strony |
| `browser_evaluate` | Uruchamia JavaScript bezpośrednio w kontekście strony |

Podczas audytu SEO Claude głównie używa `browser_navigate` i `browser_snapshot` — czyta strukturę DOM, tytuły, meta tagi, nagłówki, linki i atrybuty alt, bez konieczności klikania.

### Przepływ danych w audycie

```
Claude Code
    │
    │  wywołanie narzędzia MCP (np. browser_snapshot)
    ▼
Serwer MCP (@playwright/mcp)   ←→   Chromium (headless lub --headed)
    │
    │  zwraca snapshot DOM / zrzut ekranu / wynik JS
    ▼
Claude Code
    │
    │  analizuje dane, formułuje wyniki SEO
    ▼
reports/pmdata-pl-YYYY-MM-DD.md
```

### Kiedy używać `--headed`?

- **Debugging** — chcesz zobaczyć, co Claude widzi na stronie
- **Nauka** — obserwujesz, jak działa automatyzacja przeglądarki
- **Strony z CAPTCHA lub wykrywaniem botów** — tryb headless bywa blokowany

Na co dzień tryb headless jest szybszy i nie wymaga środowiska graficznego.
