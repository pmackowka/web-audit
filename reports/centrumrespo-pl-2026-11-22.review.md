# Ocena audytora: https://centrumrespo.pl/

Raport: reports/centrumrespo-pl-2026-11-22.md · Ocena modelu (niedeterministyczna) — fakty i liczby wyłącznie z raportu.

## Werdykt
Status FAIL jest zasłużony: 4 błędy dotyczą jednego niedziałającego linku i trzech problemów dostępności powtarzanych przez wspólne szablony artykułu. Największe ryzyko to `seo-redirects`: 9 z 10 adresów pobranych z sitemapy przekierowuje, a 8 z nich przechodzi przez hop `http://`. Stąd prawdopodobnie bierze się `lh-is-on-https` (-19.2 pkt Best Practices na 8 stronach). SEO 98/100 zawyża obraz, bo Lighthouse ocenia stronę docelową, a nie to, że sitemapa i linki wskazują stare adresy. Best Practices 64/100 oddaje stan rzeczy, ale w większości tę ocenę obniżają dwie przyczyny: redirect przez HTTP i cookies stron trzecich.

## Priorytety napraw
| # | Id | Zasięg | Dlaczego teraz | Co zrobić |
|---|---|---|---|---|
| 1 | `seo-redirects` + `lh-is-on-https` | 9/10 stron (redirect), 8/10 (HTTPS) | Kategoria (1): łańcuch https → http → https przy każdym adresie z sitemapy. Strona `/suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/` ma 1 hop https → https i jako jedyna z przekierowanych nie ma `lh-is-on-https`, co wskazuje wspólną przyczynę | Reguły przekierowań mają kierować od razu na `https://` (wtedy hop przez `http://centrumrespo.pl/...` znika). W sitemapie podać docelowe URL-e zamiast starych slugów, np. `/trening/jak-zaczac-cwiczyc/` → `/trening/zaczac-cwiczyc-domu/` |
| 2 | `seo-broken-links` | 1 link (sprawdzono 100 ze 168) | Kategoria (1): HTTP 404 | Na `/dieta/smieciowe-czy-zdrowe-jedzenie/` usunąć albo poprawić link do `https://centrumrespo.pl/?post_type=przepisy&p=168341` (wpis „przepisy” nie istnieje lub nie jest opublikowany) |
| 3 | `lh-crawlable-anchors` | 1/10 stron | Ta sama strona co #2, uszkodzony link w treści artykułu | `div.blog-content__article > div.article > p > a` ma `href="http://Cheat meal. Czym jest i… czy ma sens?"`, czyli w polu URL wklejono tytuł zamiast adresu. Podać prawidłowy URL (link „przepisy na comfort food”, `p:nth-child(120) > a`) |
| 4 | `a11y-link-in-text-block` | 9/10 stron | Błąd, impact serious, szablon treści artykułu | Linki w treści mają domyślny kolor przeglądarki `#0000ee` bez podkreślenia (kontrast 2.23:1 względem `#000000`, wymagane 3:1). Dodać w CSS treści artykułu (`.blog-content__article`) `text-decoration: underline` dla `a` |
| 5 | `a11y-color-contrast` | 9/10 stron | Błąd, impact serious, metadane autora | Kolor `#7f7f7f` na `#ffffff` daje kontrast 4:1, wymagane 4.5:1. Przyciemnić kolor dla `.blog-content__authorMeta`, `.mobile > span`, `.author-bio__title`, `.rt-time`, `time` |
| 6 | `a11y-label-content-name-mismatch` | 1/10 (`/`) | Błąd, ale jeden element | `.isBlack.v2-button[aria-label="Oferta"]` pokazuje tekst „Sprawdź dietę”. Usunąć `aria-label` albo ustawić go tak, żeby zaczynał się od „Sprawdź dietę” |
| 7 | `seo-duplicate-title`, `seo-duplicate-description` | 2 strony | Skutek #1: `/dieta/dieta-dopasowana-...` i `/dieta/wyglada-moja-dieta/` przekierowują na ten sam `/dieta/dieta-responsywna-idealna-dla-ciebie/` | Usunąć jeden z tych adresów z sitemapy; to nie jest duplikat treści do przepisania |
| 8 | `seo-title` | 5/10 stron | Szablon tytułu | Sufiks ` - Blog Centrum Respo` wydłuża tytuły powyżej 60 znaków (66–79). Skrócić sufiks albo pomijać go, gdy tytuł jest długi |
| 9 | `lh-heading-order` | 10/10 stron | Wspólne komponenty banerów | `h4.blog-content-banner-2026-diet-newsletter__title`, `h4.blog-content-banner-2026-natalia__title`, na `/` `h4.check-diet-dual__title`: zamienić na poziom wynikający z kontekstu albo na `p`/`div` ze stylem |
| 10 | `lh-third-party-cookies`, `lh-inspector-issues` | 9/10 stron (bez `/`) | Ok. 17.3 i 3.4 pkt Best Practices; skrypty firm trzecich na podstronach blogowych | Zidentyfikować w DevTools (zakładki Application → Cookies, Issues), które skrypty ustawiają cookies stron trzecich. Hipoteza do sprawdzenia: wpisy w panelu Issues dotyczą tych samych cookies |
| 11 | `lh-image-alt` | 1/10 stron | Piksel śledzący user.com bez `alt` | `body.cr-offer-menu-page > div > img` (pixel `support.user.com`): dodać `alt=""`. W axe `a11y-image-alt` przeszło, więc piksel jest prawdopodobnie wstrzykiwany po załadowaniu strony |
| 12 | `lh-errors-in-console` | 1/10 (`/`) | Raport nie podaje treści błędu | Otworzyć konsolę na `/` i ustalić źródło; bez treści nie da się ocenić wpływu |

## Wspólne przyczyny
- **Przekierowania i sitemapa** (`seo-redirects`, `lh-is-on-https`, `seo-duplicate-title`, `seo-duplicate-description`): sitemapa wskazuje stare slugi, a reguła przekierowania (serwer lub wtyczka redirectów w CMS) generuje docelowy adres z `http://`. Szukać w konfiguracji przekierowań 301 i w generatorze sitemapy.
- **Szablon treści artykułu** (`a11y-link-in-text-block`, `lh-crawlable-anchors`): CSS `.blog-content__article .article` nie stylizuje linków (zostaje domyślne `#0000ee`). Uszkodzony `href` to błąd redakcyjny we wpisie.
- **Komponent metadanych autora** (`a11y-color-contrast`): ten sam kolor `#7f7f7f` w `.blog-content__authorMeta` i jego wariancie `.mobile`, a także w `.author-bio__title`. Jedna zmiana w CSS naprawia 9 stron.
- **Banery 2026** (`lh-heading-order`): `blog-content-banner-2026-diet-newsletter` i `blog-content-banner-2026-natalia` używają `h4` niezależnie od struktury artykułu.
- **Skrypty firm trzecich** (`lh-third-party-cookies`, `lh-inspector-issues`, `lh-image-alt`): występują na podstronach blogowych, a nie na `/`, więc ładuje je szablon artykułu lub tag manager z regułą dla bloga.

## Czego ten audyt nie wykazał
- **Próbka:** 10 stron i 100 ze 168 linków wewnętrznych. Ta liczba 404 to dolna granica, nie pełny obraz. Warto puścić pełny crawl linków.
- **Sitemapa:** `seo-sitemap` przeszło, ale 9 z 10 pobranych URL-i przekierowuje. Nie wiadomo, jaki odsetek całej sitemapy to stare adresy. Ręcznie: przejrzeć całą sitemapę pod kątem kodów 3xx.
- **Core Web Vitals:** niesprawdzone. Długie artykuły z banerami i skryptami firm trzecich mogą mieć problem z LCP/INP. Sprawdzić w PageSpeed Insights / CrUX.
- **Treść:** niesprawdzona. Serwis o diecie i zdrowiu podlega wyższym wymaganiom wobec wiarygodności treści. Audyt nie ocenia autorów, źródeł ani aktualności.
- **Klawiatura i czytnik ekranu:** nietestowane. `a11y-label-content-name-mismatch` sugeruje, że etykiety ARIA na przyciskach CTA warto przejrzeć ręcznie na całym serwisie.
- **Do ręcznej weryfikacji (`a11y-color-contrast`, info, 10/10 stron):** axe nie ustalił tła dla `.respo-sport-banner__*`, `.blog-content-banner-2026-natalia__*` (tło-obraz), `.blog-content-banner-2026-diet-newsletter__*` (nakładanie), `.footer-newsletter__*` i `.metamorfozy__title-accent2` na `/`. To nie jest stwierdzony błąd. Człowiek ma zmierzyć kontrast tekstu na rzeczywistym tle tych banerów (np. pipetą w DevTools).
- **Tylko mobile:** Lighthouse działał w trybie mobile, desktop nie był oceniany.

## Instrukcja dla agenta wdrażającego
1. Popraw reguły 301 tak, żeby wskazywały bezpośrednio adres `https://`, i zaktualizuj sitemapę do docelowych URL-i (lista par w `seo-redirects`). Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znikają `seo-redirects`, `lh-is-on-https`, `seo-duplicate-title`, `seo-duplicate-description`.
2. Na `/dieta/smieciowe-czy-zdrowe-jedzenie/` usuń lub popraw link do `?post_type=przepisy&p=168341` oraz wpisz prawidłowy URL w linku „przepisy na comfort food”. Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znikają `seo-broken-links`, `lh-crawlable-anchors`.
3. Dodaj podkreślenie linków w treści artykułu (`.blog-content__article a { text-decoration: underline; }`). Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znika `a11y-link-in-text-block`.
4. Zmień kolor `#7f7f7f` w komponencie metadanych autora i `.author-bio__title` na kolor z kontrastem co najmniej 4.5:1 na `#ffffff`. Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znika `a11y-color-contrast` (error).
5. Na `/` usuń `aria-label="Oferta"` z przycisku „Sprawdź dietę” albo ustaw etykietę zaczynającą się od widocznego tekstu. Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znika `a11y-label-content-name-mismatch`.
6. Skróć sufiks tytułu w szablonie bloga. Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znika `seo-title`.
7. Zmień `h4` w banerach `blog-content-banner-2026-*` i `check-diet-dual` na właściwy poziom lub element niebędący nagłówkiem. Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znika `lh-heading-order`.
8. Dodaj `alt=""` do piksela user.com (`body.cr-offer-menu-page > div > img`). Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znika `lh-image-alt`.
9. Ustal w DevTools źródła cookies stron trzecich, wpisów w panelu Issues i błędu konsoli na `/`; usuń lub zastąp zbędne skrypty. Weryfikacja: ponowny `npm run audit -- https://centrumrespo.pl/` i znikają `lh-third-party-cookies`, `lh-inspector-issues`, `lh-errors-in-console`.
