---
name: analytics-audit
description: Pasywny audyt analityki i prywatności strony (GA4, GTM, Consent Mode v2, ciasteczka, wycieki danych, e-commerce dataLayer) — skrypt analytics/audit.py i uzupełnienie raportu. Użyj, gdy użytkownik wpisze /analytics-audit <url> <firma>.
argument-hint: <url> <firma> [url-kategorii url-produktu…]
disable-model-invocation: true
---

Przeprowadź pasywny audyt strony. Argumenty: `$ARGUMENTS` — pierwszy to URL, drugi to slug firmy, kolejne (opcjonalne) to dodatkowe strony do walidacji e-commerce.

1. Przeczytaj `analytics/CLAUDE.md` i stosuj jego zasady oraz procedurę bez wyjątków.
2. W `analytics/` uruchom `uv run audit.py <URL> --slug <firma>`, dodając `--extra-url <adres>` dla każdej dodatkowej strony.
3. Wykonaj kroki 3–8 procedury z `analytics/CLAUDE.md`.
