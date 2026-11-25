# Audyt SEO i dostępności: https://centrumrespo.pl/

- Data: 2026-11-22
- **Wynik SEO i dostępności: 77/100** (średnia Lighthouse z 3 kategorii − 2 × 4 błędów) — liczony skryptem, porównywalny między domenami
- Status: **FAIL** (problemy: błędy 4, ostrzeżenia 11, info 0, do ręcznej weryfikacji 1)
- Średnie wyniki Lighthouse (10 str.): SEO **98/100**, Accessibility **92/100**, Best Practices **64/100**
- Zakres: 10 stron (strona startowa + kolejne adresy z sitemapy), robots.txt, sitemap, linki wewnętrzne
- Silniki: Lighthouse 13.6.0 (mobile), axe-core 4.14.1, axe tagi: wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa
- Nie sprawdzono: wydajności (Core Web Vitals), treści i jej jakości, profilu linków zewnętrznych, obsługi klawiaturą i czytnikiem ekranu (test ręczny).

## Jak czytać ten raport (dla agenta wdrażającego poprawki)

1. Raport wygenerował kod, nie model — liczby i listy problemów są powtarzalne dla tego samego stanu strony.
2. Napraw najpierw `error`, potem `warning`; `info` i sekcja ręcznej weryfikacji wymagają oceny człowieka.
3. Każdy problem ma id reguły, sposób naprawy, strony, na których wystąpił, i elementy (selektor CSS + HTML) — po nich znajdź miejsce w kodzie źródłowym. Problem na wielu stronach zwykle oznacza wspólny komponent (nagłówek, stopka, szablon).
4. Tabela utraconych punktów wskazuje id problemu, którego poprawa podniesie wynik Lighthouse.
5. Po wdrożeniu uruchom audyt ponownie (komenda na dole); poprawka jest skuteczna, gdy problem znika z raportu.

## Strony

| Strona | HTTP | SEO | Accessibility | Best Practices | Błędy | Ostrzeżenia |
|---|---|---|---|---|---|---|
| / | 200 | 100 | 99 | 96 | 1 | 2 |
| /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/ | 200 | 92 | 86 | 58 | 2 | 7 |
| /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/ | 200 | 100 | 92 | 77 | 2 | 4 |
| /suplementacja/suplementacja-prozdrowotna/ | 200 | 100 | 92 | 58 | 2 | 6 |
| /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/ | 200 | 100 | 92 | 58 | 2 | 6 |
| /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/ | 200 | 100 | 92 | 58 | 2 | 5 |
| /dieta/wyglada-moja-dieta/ | 200 | 100 | 91 | 58 | 2 | 6 |
| /dieta/smieciowe-czy-zdrowe-jedzenie/ | 200 | 92 | 92 | 58 | 2 | 7 |
| /trening/jak-szybko-zbudowac-forme/ | 200 | 100 | 92 | 58 | 2 | 5 |
| /trening/jak-zaczac-cwiczyc/ | 200 | 100 | 91 | 58 | 2 | 5 |
| **Średnia** | | 98 | 92 | 64 | | |

## Utracone punkty Lighthouse

| Kategoria | Audyt | Stron | Śr. utrata pkt | Zobacz |
|---|---|---|---|---|
| Best Practices | Uses third-party cookies | 9 | 17.3 | lh-third-party-cookies |
| Best Practices | Does not use HTTPS | 8 | 15.4 | lh-is-on-https |
| Best Practices | Issues were logged in the `Issues` panel in Chrome Devtools | 9 | 3.4 | lh-inspector-issues |
| Accessibility | Background and foreground colors do not have a sufficient contrast ratio. | 9 | 3.1 | a11y-color-contrast |
| Accessibility | Links rely on color to be distinguishable. | 9 | 3.1 | a11y-link-in-text-block |
| Accessibility | Heading elements are not in a sequentially-descending order | 10 | 1.5 | lh-heading-order |
| SEO | Image elements do not have `[alt]` attributes | 1 | 0.8 | lh-image-alt |
| SEO | Links are not crawlable | 1 | 0.8 | lh-crawlable-anchors |
| Accessibility | Image elements do not have `[alt]` attributes | 1 | 0.5 | lh-image-alt |
| Best Practices | Browser errors were logged to the console | 1 | 0.4 | lh-errors-in-console |

## SEO

### [error] seo-broken-links — cały serwis

- Naprawa: Popraw adres linku albo przywróć stronę docelową (ewentualnie przekierowanie 301).
- Strona: cały serwis
  - Problem: 1 z 100 sprawdzonych linków wewnętrznych zwraca błąd (wszystkich: 168).
  - Szczegół: `HTTP 404 https://centrumrespo.pl/?post_type=przepisy&p=168341 ← linkowany z: https://centrumrespo.pl/dieta/smieciowe-czy-zdrowe-jedzenie/`

### [warning] lh-crawlable-anchors — 1 z 10 stron

- Naprawa: Search engines may use `href` attributes on links to crawl websites. Ensure that the `href` attribute of anchor elements links to an appropriate destination, so more pages of the site can be discovered. [Learn how to make links crawlable](https://support.google.com/webmasters/answer/9112205)
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Links are not crawlable (Lighthouse, -7.7 pkt w kategorii SEO).
  - Elementy (1 z 1):
    - Selektor: `div.blog-content__article > div.article > p > a`
      - HTML: `<a href="http://Cheat meal. Czym jest i… czy ma sens?">`

### [warning] lh-image-alt — 1 z 10 stron

- Naprawa: Informative elements should aim for short, descriptive alternate text. Decorative elements can be ignored with an empty alt attribute. [Learn more about the `alt` attribute](https://dequeuniversity.com/rules/axe/4.14/image-alt).
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Image elements do not have `[alt]` attributes (Lighthouse, -7.7 pkt w kategorii SEO).
  - Elementy (1 z 1):
    - Selektor: `body.cr-offer-menu-page > div > img`
      - HTML: `<img src="https://support.user.com/media/uploads/1t1nnm-user-com-support/pixel-a243e…" onload="dataLayer.push({'event':'user_info','respo-klient':'false','prospekt-respo…">`
      - Do zrobienia: Fix any of the following: Element does not have an alt attribute; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute; Element's default semantics were not overridden with role="none" or role="presentation"

### [warning] seo-duplicate-description — cały serwis

- Naprawa: Nadaj każdej stronie unikalny opis.
- Strona: cały serwis
  - Problem: 1 meta description powtarza się na kilku stronach.
  - Szczegół: `"Czym jest dieta responsywna i dlaczego jest najlepiej dopasowana? ✓ Kliknij i sprawdź na Respo!" → https://centrumrespo.pl/dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/, https://centrumrespo.pl/dieta/wyglada-moja-dieta/`

### [warning] seo-duplicate-title — cały serwis

- Naprawa: Nadaj każdej stronie unikalny <title>.
- Strona: cały serwis
  - Problem: 1 tytuł(y) powtarza się na kilku stronach.
  - Szczegół: `"Dieta responsywna to idealna dieta dla Ciebie - Blog Centrum Respo" → https://centrumrespo.pl/dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/, https://centrumrespo.pl/dieta/wyglada-moja-dieta/`

### [warning] seo-redirects — 9 z 10 stron

- Naprawa: Linkuj bezpośrednio do adresu docelowego albo skróć łańcuch do jednego 301.
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/`
  - Szczegół: `http://centrumrespo.pl/dieta/dieta-responsywna-idealna-dla-ciebie/`
  - Szczegół: `https://centrumrespo.pl/dieta/dieta-responsywna-idealna-dla-ciebie/`
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/dieta/smieciowe-czy-zdrowe-jedzenie/`
  - Szczegół: `http://centrumrespo.pl/odchudzanie/cheat-meal-kiedy-i-jak/`
  - Szczegół: `https://centrumrespo.pl/odchudzanie/cheat-meal-kiedy-i-jak/`
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/dieta/wyglada-moja-dieta/`
  - Szczegół: `http://centrumrespo.pl/dieta/dieta-responsywna-idealna-dla-ciebie/`
  - Szczegół: `https://centrumrespo.pl/dieta/dieta-responsywna-idealna-dla-ciebie/`
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/`
  - Szczegół: `http://centrumrespo.pl/dietetyka-kliniczna/dietoterapia-chorob-tarczycy/`
  - Szczegół: `https://centrumrespo.pl/dietetyka-kliniczna/dietoterapia-chorob-tarczycy/`
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/odchudzanie/tluszcze-a-odchudzanie-fakty-mity/`
  - Szczegół: `http://centrumrespo.pl/dieta/dobre-zrodla-makroskladnikow-tluszcze/`
  - Szczegół: `https://centrumrespo.pl/dieta/dobre-zrodla-makroskladnikow-tluszcze/`
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/suplementacja/suplementacja-prozdrowotna/`
  - Szczegół: `http://centrumrespo.pl/suplementacja/jaka-jest-odpowiednia-suplementacja/`
  - Szczegół: `https://centrumrespo.pl/suplementacja/jaka-jest-odpowiednia-suplementacja/`
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Łańcuch 1 przekierowań.
  - Szczegół: `https://centrumrespo.pl/suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/`
  - Szczegół: `https://centrumrespo.pl/dieta/witamina-d-od-kopciuszka-do-krolowej-witamin/`
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/trening/jak-szybko-zbudowac-forme/`
  - Szczegół: `http://centrumrespo.pl/trening/jak-zbudowac-miesnie/`
  - Szczegół: `https://centrumrespo.pl/trening/jak-zbudowac-miesnie/`
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Łańcuch 2 przekierowań.
  - Szczegół: `https://centrumrespo.pl/trening/jak-zaczac-cwiczyc/`
  - Szczegół: `http://centrumrespo.pl/trening/zaczac-cwiczyc-domu/`
  - Szczegół: `https://centrumrespo.pl/trening/zaczac-cwiczyc-domu/`

### [warning] seo-title — 5 z 10 stron

- Naprawa: Skróć albo wydłuż tytuł tak, żeby główna fraza była na początku i nie był ucinany w wynikach Google.
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Tytuł ma 66 znaków (zalecane 30–60).
  - Szczegół: `Dieta responsywna to idealna dieta dla Ciebie - Blog Centrum Respo`
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Tytuł ma 63 znaków (zalecane 30–60).
  - Szczegół: `Cheat meal - na czym polega i czy ma sens? - Blog Centrum Respo`
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Tytuł ma 66 znaków (zalecane 30–60).
  - Szczegół: `Dieta responsywna to idealna dieta dla Ciebie - Blog Centrum Respo`
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Tytuł ma 79 znaków (zalecane 30–60).
  - Szczegół: `Dieta przy niedoczynności tarczycy - zalecenia i jadłospis - Blog Centrum Respo`
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Tytuł ma 73 znaków (zalecane 30–60).
  - Szczegół: `Suplementy diety, czyli wszystko, co musisz wiedzieć - Blog Centrum Respo`

## Dostępność (WCAG)

### [error] a11y-color-contrast — 9 z 10 stron

- Naprawa: Ensure the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/color-contrast?application=playwright
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `.author-bio__title`
      - HTML: `<span class="author-bio__title">Doktor dietetyki i dietetyk sportowy, twórca Metody Respo</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.mobile > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2021-06-28T10:19:08+02:00">28 czerwca 2021</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.mobile > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-10-12T10:46:18+02:00">12 października 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.mobile > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 8</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2021-06-28T10:19:08+02:00"]`
      - HTML: `<time datetime="2021-06-28T10:19:08+02:00">28 czerwca 2021</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-10-12T10:46:18+02:00"]`
      - HTML: `<time datetime="2026-10-12T10:46:18+02:00">12 października 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Elements must meet minimum color contrast ratio thresholds (7 elem., impact: serious).
  - Elementy (7 z 7):
    - Selektor: `.author-bio__title`
      - HTML: `<span class="author-bio__title">Dietetyczka kliniczna, konsultantka merytoryczna Respo</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.mobile > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2023-04-05T15:10:10+02:00">5 kwietnia 2023</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.mobile > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-09-09T07:43:33+02:00">9 września 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.mobile > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 10</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.rt-time`
      - HTML: `<span class="rt-time"> 10</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2023-04-05T15:10:10+02:00"]`
      - HTML: `<time datetime="2023-04-05T15:10:10+02:00">5 kwietnia 2023</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-09-09T07:43:33+02:00"]`
      - HTML: `<time datetime="2026-09-09T07:43:33+02:00">9 września 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy: 6 — te same selektory co przy pierwszej stronie.
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `.blog-content__authorMeta > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2022-10-22T21:55:00+02:00">22 października 2022</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-01-13T12:59:31+01:00">13 stycznia 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 10</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.rt-time`
      - HTML: `<span class="rt-time"> 10</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2022-10-22T21:55:00+02:00"]`
      - HTML: `<time datetime="2022-10-22T21:55:00+02:00">22 października 2022</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-01-13T12:59:31+01:00"]`
      - HTML: `<time datetime="2026-01-13T12:59:31+01:00">13 stycznia 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Elements must meet minimum color contrast ratio thresholds (5 elem., impact: serious).
  - Elementy (5 z 5):
    - Selektor: `.blog-content__authorMeta > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2023-04-03T16:11:50+02:00">3 kwietnia 2023</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-01-13T11:49:03+01:00">13 stycznia 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 8</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2023-04-03T16:11:50+02:00"]`
      - HTML: `<time datetime="2023-04-03T16:11:50+02:00">3 kwietnia 2023</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-01-13T11:49:03+01:00"]`
      - HTML: `<time datetime="2026-01-13T11:49:03+01:00">13 stycznia 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `.blog-content__authorMeta > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2023-02-20T10:28:00+01:00">20 lutego 2023</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-01-13T11:59:58+01:00">13 stycznia 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 11</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.rt-time`
      - HTML: `<span class="rt-time"> 11</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2023-02-20T10:28:00+01:00"]`
      - HTML: `<time datetime="2023-02-20T10:28:00+01:00">20 lutego 2023</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-01-13T11:59:58+01:00"]`
      - HTML: `<time datetime="2026-01-13T11:59:58+01:00">13 stycznia 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `.blog-content__authorMeta > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2023-06-15T15:13:06+02:00">15 czerwca 2023</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-01-19T14:51:01+01:00">19 stycznia 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 14</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.rt-time`
      - HTML: `<span class="rt-time"> 14</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2023-06-15T15:13:06+02:00"]`
      - HTML: `<time datetime="2023-06-15T15:13:06+02:00">15 czerwca 2023</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-01-19T14:51:01+01:00"]`
      - HTML: `<time datetime="2026-01-19T14:51:01+01:00">19 stycznia 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Elements must meet minimum color contrast ratio thresholds (5 elem., impact: serious).
  - Elementy (5 z 5):
    - Selektor: `.blog-content__authorMeta > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2023-08-11T12:52:49+02:00">11 sierpnia 2023</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-09-28T10:45:03+02:00">28 września 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 8</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2023-08-11T12:52:49+02:00"]`
      - HTML: `<time datetime="2023-08-11T12:52:49+02:00">11 sierpnia 2023</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-09-28T10:45:03+02:00"]`
      - HTML: `<time datetime="2026-09-28T10:45:03+02:00">28 września 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `.blog-content__authorMeta > span:nth-child(1)`
      - HTML: `<span>Publikacja: <time datetime="2023-08-04T08:29:24+02:00">4 sierpnia 2023</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(3)`
      - HTML: `<span>Aktualizacja: <time datetime="2026-01-21T09:11:23+01:00">21 stycznia 2026</time></span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.blog-content__authorMeta > span:nth-child(5)`
      - HTML: `<span><span class="span-reading-time rt-reading-time"><span class="rt-label rt-prefix"></span> <span class="rt-time"> 13</span> <span class="rt-label rt-postfix"></span></span>min czytania</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.rt-time`
      - HTML: `<span class="rt-time"> 13</span>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2023-08-04T08:29:24+02:00"]`
      - HTML: `<time datetime="2023-08-04T08:29:24+02:00">4 sierpnia 2023</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `time[datetime="2026-01-21T09:11:23+01:00"]`
      - HTML: `<time datetime="2026-01-21T09:11:23+01:00">21 stycznia 2026</time>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4 (foreground color: #7f7f7f, background color: #ffffff, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1

### [error] a11y-label-content-name-mismatch — 1 z 10 stron

- Naprawa: Ensure that elements labelled through their content must have their visible text as part of their accessible name Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/label-content-name-mismatch?application=playwright
- Strona: /
  - Problem: Elements must have their visible text as part of their accessible name (1 elem., impact: serious).
  - Elementy (1 z 1):
    - Selektor: `.isBlack.v2-button[aria-label="Oferta"]`
      - HTML: `<a href="https://centrumrespo.pl/oferta/?menu=goal" class="v2-button isBlack" aria-label="Oferta" onclick="window.Amp.logEvent('Go Offer', { button: 'want-lose-weight' });"> <span>Sprawdź dietę</span> </a>`
      - Do zrobienia: Fix any of the following: Text inside the element is not included in the accessible name

### [error] a11y-link-in-text-block — 9 z 10 stron

- Naprawa: Ensure links are distinguished from surrounding text in a way that does not rely on color Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/link-in-text-block?application=playwright
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Links must be distinguishable without relying on color (10 elem., impact: serious).
  - Elementy (10 z 10):
    - Selektor: `a:nth-child(6)`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-sokowa-efekty-opinie/">dieta sokowa</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `a:nth-child(7)`
      - HTML: `<a href="https://centrumrespo.pl/dietetyka-kliniczna/dieta-bezlaktozowa/">dieta bez laktozy</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(25) > a:nth-child(2)`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-kapusciana-czy-warto/">dieta kapuściana</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(25) > a:nth-child(3)`
      - HTML: `<a href="https://centrumrespo.pl/odchudzanie/dieta-1000-kcal-zasady/">dieta 1000 kalorii,</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(25) > a:nth-child(4)`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-kopenhaska-zasady-jadlospis/">dieta kopenhaska</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(25) > a:nth-child(5)`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-dukana/">dieta Dukana</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(77) > a`
      - HTML: `<a href="https://centrumrespo.pl/aplikacja/">aplikację Respo</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(89) > a`
      - HTML: `<a href="https://centrumrespo.pl/oferta/?menu=goal">Dietetyk online</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(9) > a`
      - HTML: `<a href="https://centrumrespo.pl/odchudzanie/jak-uniknac-efektu-jojo/">efektem jo-jo</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(95) > a`
      - HTML: `<a href="https://centrumrespo.pl/kalkulator-bmi/">kalkulator BMI online</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Links must be distinguishable without relying on color (3 elem., impact: serious).
  - Elementy (3 z 3):
    - Selektor: `p:nth-child(120) > a`
      - HTML: `<a href="http://Cheat meal. Czym jest i… czy ma sens?">przepisy na comfort food</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(17) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-na-redukcje-plan-jadlospis/">diety redukcyjnej</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(45) > a`
      - HTML: `<a href="https://centrumrespo.pl/dietetyka-kliniczna/insulinoopornosc/">insulinooporności</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Links must be distinguishable without relying on color (10 elem., impact: serious).
  - Elementy: 10 — te same selektory co przy pierwszej stronie.
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Links must be distinguishable without relying on color (7 elem., impact: serious).
  - Elementy (7 z 7):
    - Selektor: `p:nth-child(103) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/kwasy-omega-3-6-9-kompendium-wiedzy/">kwasy omega-3</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(106) > a`
      - HTML: `<a href="https://centrumrespo.pl/dietetyka-kliniczna/nadczynnosc-tarczycy/">nadczynności tarczycy</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(115) > a`
      - HTML: `<a href="https://centrumrespo.pl/zdrowie/probiotyki/">Probiotyki</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(15) > a`
      - HTML: `<a href="https://centrumrespo.pl/dzieci/niedoczynnosc-tarczycy-u-dziecka/">Niedoczynność tarczycy u dzieci</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(32) > a`
      - HTML: `<a href="https://centrumrespo.pl/dietetyka-kliniczna/hashimoto/">dieta przy Hashimoto</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(78) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-hashimoto-przepisy/">przepisy w diecie na Hashimoto</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(80) > a`
      - HTML: `<a href="https://centrumrespo.pl/suplementacja/suplementacja-chorobach-tarczycy/">suplementów na tarczycę</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Links must be distinguishable without relying on color (7 elem., impact: serious).
  - Elementy (7 z 7):
    - Selektor: `p:nth-child(10) > a`
      - HTML: `<a href="https://centrumrespo.pl/odchudzanie/skuteczna-dieta/">dieta odchudzająca</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(113) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/na-czym-smazyc/">najlepszy tłuszcz do smażenia</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(116) > a:nth-child(1)`
      - HTML: `<a href="https://centrumrespo.pl/kalkulator-kalorii/">kalkulator zapotrzebowania kalorycznego</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(116) > a:nth-child(2)`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-na-redukcje-plan-jadlospis/">diety redukcyjnej</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(13) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/trojglicerydy-czym-sa-i-jak-obnizyc-ich-poziom/">trójglicerydy</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(21) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/ile-tluszczu-na-redukcji/">Ile jeść tłuszczu na redukcji</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(26) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-niskotluszczowa/">dieta niskotłuszczowa</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Links must be distinguishable without relying on color (1 elem., impact: serious).
  - Elementy (1 z 1):
    - Selektor: `p:nth-child(110) > a`
      - HTML: `<a href="https://centrumrespo.pl/oferta/?menu=goal">dietetycy online</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Links must be distinguishable without relying on color (2 elem., impact: serious).
  - Elementy (2 z 2):
    - Selektor: `p:nth-child(50) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/witamina-k-czyli-o-krwi-krzepnieciu-i-kosciach/">witamina K</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(52) > a`
      - HTML: `<a href="https://centrumrespo.pl/dietetyka-kliniczna/rola-witamin-w-organizmie/">role tych witamin</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Links must be distinguishable without relying on color (7 elem., impact: serious).
  - Elementy (7 z 7):
    - Selektor: `p:nth-child(103) > a[href$="atlas/"]`
      - HTML: `<a href="https://centrumrespo.pl/atlas/">atlas ćwiczeń</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(108) > a`
      - HTML: `<a href="https://centrumrespo.pl/oferta/?menu=goal">dietetycy online</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(13) > a`
      - HTML: `<a href="https://centrumrespo.pl/odchudzanie/rekompozycja-sylwetki/">rekompozycja sylwetki</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(22) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dieta-na-mase-miesniowa/">dieta na masę mięśniową</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(59) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/dobre-zrodla-makroskladnikow-tluszcze/">dobre źródła tłuszczu</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(64) > a`
      - HTML: `<a href="https://centrumrespo.pl/suplementacja/jak-brac-kreatyne/">kreatyny</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(65) > a`
      - HTML: `<a href="https://centrumrespo.pl/dieta/suplementy-na-mase-i-rzezbe-czyli-o-suplementach-w-sportach-silowych/">suplementach na masę i rzeźbę.</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Links must be distinguishable without relying on color (4 elem., impact: serious).
  - Elementy (4 z 4):
    - Selektor: `p:nth-child(68) > a[href$="atlas/"]`
      - HTML: `<a href="https://centrumrespo.pl/atlas/">atlasie ćwiczeń</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(70) > a`
      - HTML: `<a href="https://centrumrespo.pl/aplikacja/">Aplikacja do treningu</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(74) > a`
      - HTML: `<a href="https://centrumrespo.pl/metoda-respo/">metody Respo</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text
    - Selektor: `p:nth-child(91) > a`
      - HTML: `<a href="https://centrumrespo.pl/trening/10000-krokow-dziennie-efekty/">co daje 10000 kroków dziennie</a>`
      - Do zrobienia: Fix any of the following: The link has insufficient color contrast of 2.23:1 with the surrounding text. (Minimum contrast is 3:1, link text: #0000ee, surrounding text: #000000); The link has no styling (such as underline) to distinguish it from the surrounding text

### [warning] lh-heading-order — 10 z 10 stron

- Naprawa: Properly ordered headings that do not skip levels convey the semantic structure of the page, making it easier to navigate and understand when using assistive technologies. [Learn more about heading order](https://dequeuniversity.com/rules/axe/4.14/heading-order).
- Strona: /
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (1 z 1):
    - Selektor: `div.check-diet-dual__inner > div.check-diet-dual__case > div.check-diet-dual__label > h4.check-diet-dual__title`
      - HTML: `<h4 class="check-diet-dual__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (2 z 2):
    - Selektor: `div.blog-content-banner-2026-diet-newsletter__inner > div.blog-content-banner-2026-diet-newsletter__content > div.blog-content-banner-2026-diet-newsletter__copy > h4.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.4 pkt w kategorii Accessibility).
  - Elementy (2 z 2):
    - Selektor: `div.blog-content-banner-2026-diet-newsletter__inner > div.blog-content-banner-2026-diet-newsletter__content > div.blog-content-banner-2026-diet-newsletter__copy > h4.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (2 z 2):
    - Selektor: `div.blog-content-banner-2026-diet-newsletter__inner > div.blog-content-banner-2026-diet-newsletter__content > div.blog-content-banner-2026-diet-newsletter__copy > h4.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.4 pkt w kategorii Accessibility).
  - Elementy (1 z 1):
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (1 z 1):
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (1 z 1):
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (2 z 2):
    - Selektor: `div.blog-content-banner-2026-diet-newsletter__inner > div.blog-content-banner-2026-diet-newsletter__content > div.blog-content-banner-2026-diet-newsletter__copy > h4.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.4 pkt w kategorii Accessibility).
  - Elementy (1 z 1):
    - Selektor: `div.blog-content-banner-2026-diet-newsletter__inner > div.blog-content-banner-2026-diet-newsletter__content > div.blog-content-banner-2026-diet-newsletter__copy > h4.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Heading elements are not in a sequentially-descending order (Lighthouse, -1.5 pkt w kategorii Accessibility).
  - Elementy (2 z 2):
    - Selektor: `div.blog-content-banner-2026-diet-newsletter__inner > div.blog-content-banner-2026-diet-newsletter__content > div.blog-content-banner-2026-diet-newsletter__copy > h4.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid
    - Selektor: `div.blog-content-banner-2026-natalia__inner > div.blog-content-banner-2026-natalia__content > div > h4.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title">`
      - Do zrobienia: Fix any of the following: Heading order invalid

## Dobre praktyki (Lighthouse)

### [warning] lh-errors-in-console — 1 z 10 stron

- Naprawa: Errors logged to the console indicate unresolved problems. They can come from network request failures and other browser concerns. [Learn more about this errors in console diagnostic audit](https://developer.chrome.com/docs/lighthouse/best-practices/errors-in-console/)
- Strona: /
  - Problem: Browser errors were logged to the console (Lighthouse, -3.8 pkt w kategorii Best Practices).

### [warning] lh-inspector-issues — 9 z 10 stron

- Naprawa: Issues logged to the `Issues` panel in Chrome Devtools indicate unresolved problems. They can come from network request failures, insufficient security controls, and other browser concerns. Open up the Issues panel in Chrome DevTools for more details on each issue.
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Issues were logged in the `Issues` panel in Chrome Devtools (Lighthouse, -3.8 pkt w kategorii Best Practices).

### [warning] lh-is-on-https — 8 z 10 stron

- Naprawa: All sites should be protected with HTTPS, even ones that don't handle sensitive data. This includes avoiding [mixed content](https://developers.google.com/web/fundamentals/security/prevent-mixed-content/what-is-mixed-content), where some resources are loaded over HTTP despite the initial request being served over HTTPS. HTTPS prevents intruders from tampering with or passively listening in on the communications between your app and your users, and is a prerequisite for HTTP/2 and many new web platform APIs. [Learn more about HTTPS](https://developer.chrome.com/docs/lighthouse/pwa/is-on-https/).
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Does not use HTTPS (Lighthouse, -19.2 pkt w kategorii Best Practices).

### [warning] lh-third-party-cookies — 9 z 10 stron

- Naprawa: Third-party cookies may be blocked in some contexts. [Learn more about preparing for third-party cookie restrictions](https://privacysandbox.google.com/cookies/prepare/overview).
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Uses third-party cookies (Lighthouse, -19.2 pkt w kategorii Best Practices).

## Do ręcznej weryfikacji (axe incomplete)

### [info] a11y-color-contrast — 10 z 10 stron

- Naprawa: Ensure the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/color-contrast?application=playwright
- Strona: /
  - Problem: Elements must meet minimum color contrast ratio thresholds (21 elem., impact: serious).
  - Elementy (10 z 21):
    - Selektor: `.about-cancer-fighters__media-money`
      - HTML: `<p class="about-cancer-fighters__media-money">600 000,00 zł</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.footer-newsletter__checkbox-label > span:nth-child(1)`
      - HTML: `<span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.footer-newsletter__submit-button`
      - HTML: `<button class="footer-newsletter__submit-button" type="button">Zapisz się</button>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it is overlapped by another element
    - Selektor: `.footer-newsletter__title`
      - HTML: `<h2 class="footer-newsletter__title"> Dołącz do ponad <b>130 tys. osób</b> i regularnie odbieraj porady dietetyków oraz przepisy od zespołu dr Michała Wrzoska. </h2>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it is overlapped by another element
    - Selektor: `.frontpage-b > .two-columns__inner > .two-columns__content > .two-columns__list > .two-columns__list-container > .banner-in-list.two-columns__banner > .two-columns__banner-title`
      - HTML: `<p class="two-columns__banner-title"> Podoba Ci się<br><strong>Aplikacja Respo?</strong> </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it is overlapped by another element
    - Selektor: `.frontpage-b > .two-columns__inner > .two-columns__content > .two-columns__list > .two-columns__list-container > .banner-in-list.two-columns__banner > .two-columns__button-holder > .isBlack.v2-button > span`
      - HTML: `<span>Sprawdź dietę</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it is overlapped by another element
    - Selektor: `.metamorfozy__title-accent2`
      - HTML: `<div class="metamorfozy__title-accent2">744 671</div>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__button > .v2-button__label`
      - HTML: `<span class="v2-button__label">Zacznij współpracę</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /dieta/dieta-dopasowana-sprawdz-czy-ty-i-dieta-jestescie-dla-siebie-stworzone/
  - Problem: Elements must meet minimum color contrast ratio thresholds (15 elem., impact: serious).
  - Elementy (10 z 15):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /dieta/smieciowe-czy-zdrowe-jedzenie/
  - Problem: Elements must meet minimum color contrast ratio thresholds (14 elem., impact: serious).
  - Elementy (10 z 14):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /dieta/wyglada-moja-dieta/
  - Problem: Elements must meet minimum color contrast ratio thresholds (15 elem., impact: serious).
  - Elementy (10 z 15):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /dietetyka-kliniczna/choroby-ktore-utrudniaja-chudniecie/
  - Problem: Elements must meet minimum color contrast ratio thresholds (15 elem., impact: serious).
  - Elementy (10 z 15):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /odchudzanie/tluszcze-a-odchudzanie-fakty-mity/
  - Problem: Elements must meet minimum color contrast ratio thresholds (15 elem., impact: serious).
  - Elementy (10 z 15):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /suplementacja/suplementacja-prozdrowotna/
  - Problem: Elements must meet minimum color contrast ratio thresholds (14 elem., impact: serious).
  - Elementy (10 z 14):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /suplementacja/witamina-d-niedobor-suplementacja-bezpieczna-dawka/
  - Problem: Elements must meet minimum color contrast ratio thresholds (14 elem., impact: serious).
  - Elementy (10 z 14):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /trening/jak-szybko-zbudowac-forme/
  - Problem: Elements must meet minimum color contrast ratio thresholds (15 elem., impact: serious).
  - Elementy (10 z 15):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
- Strona: /trening/jak-zaczac-cwiczyc/
  - Problem: Elements must meet minimum color contrast ratio thresholds (13 elem., impact: serious).
  - Elementy (10 z 13):
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(2)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content__authorMetaSeparator:nth-child(4)`
      - HTML: `<span class="blog-content__authorMetaSeparator">·</span>`
      - Do zrobienia: Fix any of the following: Element content is too short to determine if it is actual text content
    - Selektor: `.blog-content-banner-2026-diet-newsletter__p`
      - HTML: `<p class="blog-content-banner-2026-diet-newsletter__p"> Dołącz do <b>ponad 130 000 osób</b> i&nbsp;regularnie otrzymuj porady dietetyczne oraz kulinarne. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-diet-newsletter__title`
      - HTML: `<h4 class="blog-content-banner-2026-diet-newsletter__title"> Zadbaj o&nbsp;<b>zdrowie</b> z&nbsp;newsletterem Respo </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `.blog-content-banner-2026-natalia__p`
      - HTML: `<p class="blog-content-banner-2026-natalia__p"> W&nbsp;Respo każda dieta jest szyta na miarę. Z&nbsp;nami osiągniesz cel zdrowo, bez zbędnych restrykcji i&nbsp;jedząc tylko to, co lubisz, z&nbsp;pomocą doświadczonego dietetyka klinicznego. </p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__title`
      - HTML: `<h4 class="blog-content-banner-2026-natalia__title"> Dołącz do ponad <span class="blog-content-banner-2026-natalia__titleAccent">98 124</span> zadowolonych Podopiecznych! </h4>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.blog-content-banner-2026-natalia__titleAccent`
      - HTML: `<span class="blog-content-banner-2026-natalia__titleAccent">98 124</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a background image
    - Selektor: `.respo-sport-banner__description`
      - HTML: `<p class="respo-sport-banner__description">Opieka dietetyka sportowego i indywidualny plan żywieniowy dopasowany do Twojej dyscypliny, treningów i sportowych celów. Nie pozwól, by źle dobrana dieta ograniczała Twój progres.</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title`
      - HTML: `<p class="respo-sport-banner__title"><strong>Trenujesz regularnie?</strong><br> My robimy dietę.<span class="respo-sport-banner__title-extra"> Ty robisz wynik.</span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element
    - Selektor: `.respo-sport-banner__title > strong`
      - HTML: `<strong>Trenujesz regularnie?</strong>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined due to a pseudo element

## Zaliczone reguły (na wszystkich stronach)

a11y-aria-allowed-attr, a11y-aria-command-name, a11y-aria-conditional-attr, a11y-aria-deprecated-role, a11y-aria-hidden-body, a11y-aria-hidden-focus, a11y-aria-prohibited-attr, a11y-aria-required-attr, a11y-aria-roles, a11y-aria-valid-attr, a11y-aria-valid-attr-value, a11y-autocomplete-valid, a11y-avoid-inline-spacing, a11y-button-name, a11y-bypass, a11y-document-title, a11y-duplicate-id-aria, a11y-form-field-multiple-labels, a11y-html-has-lang, a11y-html-lang-valid, a11y-image-alt, a11y-label, a11y-link-name, a11y-list, a11y-listitem, a11y-meta-viewport, a11y-nested-interactive, a11y-role-img-alt, a11y-summary-name, a11y-target-size, a11y-td-headers-attr, a11y-th-has-data-cells, a11y-video-caption, seo-canonical, seo-h1, seo-http-status, seo-https, seo-meta-description, seo-noindex, seo-open-graph, seo-robots-txt, seo-sitemap, seo-structured-data, seo-viewport

## Ponowny audyt

`npm run audit -- https://centrumrespo.pl/` w repozytorium web-audit.
