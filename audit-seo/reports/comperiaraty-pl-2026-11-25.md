# Audyt SEO i dostępności: https://comperiaraty.pl/

- Data: 2026-11-25
- Status: **FAIL** (problemy: błędy 5, ostrzeżenia 7, info 1, do ręcznej weryfikacji 1)
- Średnie wyniki Lighthouse (6 str.): SEO **91/100**, Accessibility **94/100**, Best Practices **96/100**
- Zakres: 6 stron (strona startowa + kolejne adresy z sitemapy), robots.txt, sitemap, linki wewnętrzne
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
| / | 200 | 85 | 86 | 96 | 4 | 5 |
| /polityka-prywatnosci/ | 200 | 92 | 100 | 96 | 1 | 3 |
| /regulamin/ | 200 | 92 | 100 | 96 | 0 | 4 |
| /wspolpraca/ | 200 | 92 | 90 | 96 | 3 | 5 |
| /test/ | 200 | 92 | 89 | 96 | 3 | 4 |
| /author/admin/ | 200 | 92 | 100 | 96 | 0 | 5 |
| **Średnia** | | 91 | 94 | 96 | | |

## Utracone punkty Lighthouse

| Kategoria | Audyt | Stron | Śr. utrata pkt | Zobacz |
|---|---|---|---|---|
| SEO | Document does not have a meta description | 6 | 7.8 | seo-meta-description |
| Best Practices | Serves images with low resolution | 6 | 3.8 | lh-image-size-responsive |
| Accessibility | Background and foreground colors do not have a sufficient contrast ratio. | 3 | 2.2 | a11y-color-contrast |
| Accessibility | Form elements do not have associated labels | 2 | 2 | a11y-label |
| SEO | Links are not crawlable | 1 | 1.3 | lh-crawlable-anchors |
| Accessibility | `[aria-*]` attributes do not match their roles | 1 | 0.9 | a11y-aria-allowed-attr |
| Accessibility | Links do not have a discernible name | 1 | 0.8 | a11y-link-name |
| Accessibility | Elements with `role="none"` or `role="presentation"` have conflicts | 1 | 0.1 | lh-presentation-role-conflict |

## SEO

### [error] seo-h1 — 4 z 6 stron

- Naprawa: Dodaj jeden H1 opisujący temat strony.
- Strona: /
  - Problem: Brak nagłówka H1.
- Strona: /polityka-prywatnosci/
  - Problem: Brak nagłówka H1.
- Strona: /test/
  - Problem: Brak nagłówka H1.
- Strona: /wspolpraca/
  - Problem: Brak nagłówka H1.

### [warning] lh-crawlable-anchors — 1 z 6 stron

- Naprawa: Search engines may use `href` attributes on links to crawl websites. Ensure that the `href` attribute of anchor elements links to an appropriate destination, so more pages of the site can be discovered. [Learn how to make links crawlable](https://support.google.com/webmasters/answer/9112205)
- Strona: /
  - Problem: Links are not crawlable (Lighthouse, -7.7 pkt w kategorii SEO).
  - Elementy (10 z 10):
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-6011 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-6012 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-6013 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-6014 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-6015 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-6016 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-9441 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-9442 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-9443 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`
    - Selektor: `div.elementor-accordion > div.elementor-accordion-item > div#elementor-tab-title-9444 > a.elementor-accordion-title`
      - HTML: `<a class="elementor-accordion-title" tabindex="0">`

### [warning] seo-canonical — 1 z 6 stron

- Naprawa: Dodaj <link rel="canonical"> wskazujący na adres tej strony.
- Strona: /author/admin/
  - Problem: Brak link rel=canonical.

### [warning] seo-meta-description — 6 z 6 stron

- Naprawa: Dodaj <meta name="description"> opisujący stronę w 70–160 znakach.
- Strona: /
  - Problem: Brak meta description.
- Strona: /author/admin/
  - Problem: Brak meta description.
- Strona: /polityka-prywatnosci/
  - Problem: Brak meta description.
- Strona: /regulamin/
  - Problem: Brak meta description.
- Strona: /test/
  - Problem: Brak meta description.
- Strona: /wspolpraca/
  - Problem: Brak meta description.

### [warning] seo-open-graph — 6 z 6 stron

- Naprawa: Uzupełnij brakujące tagi og:* w <head>.
- Strona: /
  - Problem: Brak tagów Open Graph: og:title, og:description, og:image.
- Strona: /author/admin/
  - Problem: Brak tagów Open Graph: og:title, og:description, og:image.
- Strona: /polityka-prywatnosci/
  - Problem: Brak tagów Open Graph: og:title, og:description, og:image.
- Strona: /regulamin/
  - Problem: Brak tagów Open Graph: og:title, og:description, og:image.
- Strona: /test/
  - Problem: Brak tagów Open Graph: og:title, og:description, og:image.
- Strona: /wspolpraca/
  - Problem: Brak tagów Open Graph: og:title, og:description, og:image.

### [warning] seo-title — 5 z 6 stron

- Naprawa: Skróć albo wydłuż tytuł tak, żeby główna fraza była na początku i nie był ucinany w wynikach Google.
- Strona: /
  - Problem: Tytuł ma 12 znaków (zalecane 30–60).
  - Szczegół: `ComperiaRaty`
- Strona: /author/admin/
  - Problem: Tytuł ma 20 znaków (zalecane 30–60).
  - Szczegół: `admin – ComperiaRaty`
- Strona: /regulamin/
  - Problem: Tytuł ma 24 znaków (zalecane 30–60).
  - Szczegół: `Regulamin – ComperiaRaty`
- Strona: /test/
  - Problem: Tytuł ma 19 znaków (zalecane 30–60).
  - Szczegół: `test – ComperiaRaty`
- Strona: /wspolpraca/
  - Problem: Tytuł ma 25 znaków (zalecane 30–60).
  - Szczegół: `Współpraca – ComperiaRaty`

### [info] seo-structured-data — 6 z 6 stron

- Naprawa: Rozważ schema.org (np. Organization, WebSite, Article).
- Strona: /
  - Problem: Brak danych strukturalnych JSON-LD.
- Strona: /author/admin/
  - Problem: Brak danych strukturalnych JSON-LD.
- Strona: /polityka-prywatnosci/
  - Problem: Brak danych strukturalnych JSON-LD.
- Strona: /regulamin/
  - Problem: Brak danych strukturalnych JSON-LD.
- Strona: /test/
  - Problem: Brak danych strukturalnych JSON-LD.
- Strona: /wspolpraca/
  - Problem: Brak danych strukturalnych JSON-LD.

## Dostępność (WCAG)

### [error] a11y-aria-allowed-attr — 1 z 6 stron

- Naprawa: Ensure an element's role supports its ARIA attributes Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/aria-allowed-attr?application=playwright
- Strona: /
  - Problem: Elements must only use supported ARIA attributes (1 elem., impact: critical).
  - Elementy (1 z 1):
    - Selektor: `#elementor-tab-title-9441`
      - HTML: `<div id="elementor-tab-title-9441" class="elementor-tab-title elementor-active" data-tab="1" role="button" aria-controls="elementor-tab-content-9441" aria-expanded="true" tabindex="0" aria-selected="true">`
      - Do zrobienia: Fix all of the following: ARIA attribute is not allowed: aria-selected="true"

### [error] a11y-color-contrast — 3 z 6 stron

- Naprawa: Ensure the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/color-contrast?application=playwright
- Strona: /
  - Problem: Elements must meet minimum color contrast ratio thresholds (4 elem., impact: serious).
  - Elementy (4 z 4):
    - Selektor: `.input-elements:nth-child(1) > .input-parametres > .extra-labels > .max`
      - HTML: `<div class="max">max. 100 000 zł</div>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 1.82 (foreground color: #4ba0d1, background color: #0770b3, font size: 9.0pt (12px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.input-elements:nth-child(1) > .input-parametres > .extra-labels > .min`
      - HTML: `<div class="min">min. 1000</div>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 1.82 (foreground color: #4ba0d1, background color: #0770b3, font size: 9.0pt (12px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.input-elements:nth-child(2) > .input-parametres > .extra-labels > .max`
      - HTML: `<div class="max">max. 84 mies.</div>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 1.82 (foreground color: #4ba0d1, background color: #0770b3, font size: 9.0pt (12px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.input-elements:nth-child(2) > .input-parametres > .extra-labels > .min`
      - HTML: `<div class="min">min. 10</div>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 1.82 (foreground color: #4ba0d1, background color: #0770b3, font size: 9.0pt (12px), font weight: normal). Expected contrast ratio of 4.5:1
- Strona: /test/
  - Problem: Elements must meet minimum color contrast ratio thresholds (4 elem., impact: serious).
  - Elementy: 4 — te same selektory co przy pierwszej stronie.
- Strona: /wspolpraca/
  - Problem: Elements must meet minimum color contrast ratio thresholds (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `.elementor-element-9f4b3dc > .elementor-widget-container > p[align="JUSTIFY"]:nth-child(1)`
      - HTML: `<p align="JUSTIFY">Masz pytania? Chcesz nawiązać współpracę? A może potrzebujesz dodatkowych informacji? Jesteśmy do Twojej dyspozycji!</p>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4.29 (foreground color: #7a7a7a, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.elementor-element-9f4b3dc > .elementor-widget-container > p[align="JUSTIFY"]:nth-child(2)`
      - HTML: `<p align="JUSTIFY">E-mail: akedrak@comperia.pl</p>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4.29 (foreground color: #7a7a7a, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.elementor-element-9f4b3dc > .elementor-widget-container > p[align="JUSTIFY"]:nth-child(3)`
      - HTML: `<p align="JUSTIFY">Telefon: 605 031 083</p>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4.29 (foreground color: #7a7a7a, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.elementor-element-c9324a2 > .elementor-widget-container > p[align="JUSTIFY"]:nth-child(1)`
      - HTML: `<p align="JUSTIFY">`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4.29 (foreground color: #7a7a7a, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.elementor-element-c9324a2 > .elementor-widget-container > p[align="JUSTIFY"]:nth-child(2)`
      - HTML: `<p align="JUSTIFY">Dzięki ComperiaRaty użytkownicy mogą w łatwy sposób znaleźć finansowanie idealnie dopasowane do swoich potrzeb, a pośrednicy zyskują skuteczne narzędzie, które zwiększa konwersję i upraszcza sprzedaż produktów finansowych.</p>`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4.29 (foreground color: #7a7a7a, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1
    - Selektor: `.elementor-element-c9324a2 > .elementor-widget-container > p[align="JUSTIFY"]:nth-child(3)`
      - HTML: `<p align="JUSTIFY">`
      - Do zrobienia: Fix any of the following: Element has insufficient color contrast of 4.29 (foreground color: #7a7a7a, background color: #ffffff, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1

### [error] a11y-label — 2 z 6 stron

- Naprawa: Ensure every form element has a label Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/label?application=playwright
- Strona: /
  - Problem: Form elements must have labels (2 elem., impact: critical).
  - Elementy (2 z 2):
    - Selektor: `#ilosc-rat_val`
      - HTML: `<input id="ilosc-rat_val" maxlength="3" type="tel">`
      - Do zrobienia: Fix any of the following: Element does not have an implicit (wrapped) <label>; Element does not have an explicit <label>; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute; Element has no placeholder attribute; Element's default semantics were not overridden with role="none" or role="presentation"
    - Selektor: `#pozyczka_val`
      - HTML: `<input id="pozyczka_val" maxlength="7" type="tel">`
      - Do zrobienia: Fix any of the following: Element does not have an implicit (wrapped) <label>; Element does not have an explicit <label>; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute; Element has no placeholder attribute; Element's default semantics were not overridden with role="none" or role="presentation"
- Strona: /test/
  - Problem: Form elements must have labels (2 elem., impact: critical).
  - Elementy: 2 — te same selektory co przy pierwszej stronie.

### [error] a11y-link-name — 1 z 6 stron

- Naprawa: Ensure links have discernible text Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/link-name?application=playwright
- Strona: /wspolpraca/
  - Problem: Links must have discernible text (6 elem., impact: serious).
  - Elementy (6 z 6):
    - Selektor: `a[data-elementor-lightbox-title="comperiaraty_ico_-01"]`
      - HTML: `<a data-elementor-open-...="yes" data-elementor-light...="2ee375e" data-elementor-light...="comperiaraty_ico_-01" data-e-action-hash="#elementor-action%3A..." href="https://comperiaraty...">`
      - Do zrobienia: Fix all of the following: Element is in tab order and does not have accessible text; Fix any of the following:; Element does not have text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute
    - Selektor: `a[data-elementor-lightbox-title="comperiaraty_ico_-02"]`
      - HTML: `<a data-elementor-open-...="yes" data-elementor-light...="2ee375e" data-elementor-light...="comperiaraty_ico_-02" data-e-action-hash="#elementor-action%3A..." href="https://comperiaraty...">`
      - Do zrobienia: Fix all of the following: Element is in tab order and does not have accessible text; Fix any of the following:; Element does not have text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute
    - Selektor: `a[data-elementor-lightbox-title="comperiaraty_ico_-03"]`
      - HTML: `<a data-elementor-open-...="yes" data-elementor-light...="2ee375e" data-elementor-light...="comperiaraty_ico_-03" data-e-action-hash="#elementor-action%3A..." href="https://comperiaraty...">`
      - Do zrobienia: Fix all of the following: Element is in tab order and does not have accessible text; Fix any of the following:; Element does not have text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute
    - Selektor: `a[data-elementor-lightbox-title="comperiaraty_ico_-04"]`
      - HTML: `<a data-elementor-open-...="yes" data-elementor-light...="2ee375e" data-elementor-light...="comperiaraty_ico_-04" data-e-action-hash="#elementor-action%3A..." href="https://comperiaraty...">`
      - Do zrobienia: Fix all of the following: Element is in tab order and does not have accessible text; Fix any of the following:; Element does not have text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute
    - Selektor: `a[data-elementor-lightbox-title="comperiaraty_ico_-05"]`
      - HTML: `<a data-elementor-open-...="yes" data-elementor-light...="2ee375e" data-elementor-light...="comperiaraty_ico_-05" data-e-action-hash="#elementor-action%3A..." href="https://comperiaraty...">`
      - Do zrobienia: Fix all of the following: Element is in tab order and does not have accessible text; Fix any of the following:; Element does not have text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute
    - Selektor: `a[data-elementor-lightbox-title="comperiaraty_ico_-06"]`
      - HTML: `<a data-elementor-open-...="yes" data-elementor-light...="2ee375e" data-elementor-light...="comperiaraty_ico_-06" data-e-action-hash="#elementor-action%3A..." href="https://comperiaraty...">`
      - Do zrobienia: Fix all of the following: Element is in tab order and does not have accessible text; Fix any of the following:; Element does not have text that is visible to screen readers; aria-label attribute does not exist or is empty; aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty; Element has no title attribute

### [warning] lh-presentation-role-conflict — 1 z 6 stron

- Naprawa: There are certain cases where the semantic role of an element with `role="none"` or `role="presentation"` does not resolve to none or presentation. To ensure the element remains removed from the accessibility tree, you should not add any global ARIA attributes to the element or make it focusable. [Learn more about presentation role conflict](https://dequeuniversity.com/rules/axe/4.14/presentation-role-conflict).
- Strona: /wspolpraca/
  - Problem: Elements with `role="none"` or `role="presentation"` have conflicts (Lighthouse, -0.7 pkt w kategorii Accessibility).
  - Elementy (6 z 6):
    - Selektor: `figure.gallery-item > div.gallery-icon > a > img.attachment-thumbnail`
      - HTML: `<img loading="lazy" decoding="async" width="150" height="150" src="https://comperiaraty.pl/wp-content/uploads/2025/05/comperiaraty_ico_-04.svg" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-971">`
      - Do zrobienia: Fix all of the following: Element does not have global ARIA attribute
    - Selektor: `figure.gallery-item > div.gallery-icon > a > img.attachment-thumbnail`
      - HTML: `<img loading="lazy" decoding="async" width="150" height="150" src="https://comperiaraty.pl/wp-content/uploads/2025/05/comperiaraty_ico_-01.svg" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-972">`
      - Do zrobienia: Fix all of the following: Element does not have global ARIA attribute
    - Selektor: `figure.gallery-item > div.gallery-icon > a > img.attachment-thumbnail`
      - HTML: `<img loading="lazy" decoding="async" width="150" height="150" src="https://comperiaraty.pl/wp-content/uploads/2025/05/comperiaraty_ico_-03.svg" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-973">`
      - Do zrobienia: Fix all of the following: Element does not have global ARIA attribute
    - Selektor: `figure.gallery-item > div.gallery-icon > a > img.attachment-thumbnail`
      - HTML: `<img loading="lazy" decoding="async" width="150" height="150" src="https://comperiaraty.pl/wp-content/uploads/2025/05/comperiaraty_ico_-05.svg" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-974">`
      - Do zrobienia: Fix all of the following: Element does not have global ARIA attribute
    - Selektor: `figure.gallery-item > div.gallery-icon > a > img.attachment-thumbnail`
      - HTML: `<img loading="lazy" decoding="async" width="150" height="150" src="https://comperiaraty.pl/wp-content/uploads/2025/05/comperiaraty_ico_-02.svg" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-975">`
      - Do zrobienia: Fix all of the following: Element does not have global ARIA attribute
    - Selektor: `figure.gallery-item > div.gallery-icon > a > img.attachment-thumbnail`
      - HTML: `<img loading="lazy" decoding="async" width="150" height="150" src="https://comperiaraty.pl/wp-content/uploads/2025/05/comperiaraty_ico_-06.svg" class="attachment-thumbnail size-thumbnail" alt="" aria-describedby="gallery-1-976">`
      - Do zrobienia: Fix all of the following: Element does not have global ARIA attribute

## Dobre praktyki (Lighthouse)

### [warning] lh-image-size-responsive — 6 z 6 stron

- Naprawa: Image natural dimensions should be proportional to the display size and the pixel ratio to maximize image clarity. [Learn how to provide responsive images](https://web.dev/articles/serve-responsive-images).
- Strona: /
  - Problem: Serves images with low resolution (Lighthouse, -3.8 pkt w kategorii Best Practices).
  - Elementy (1 z 1):
    - Selektor: `div.site-branding > span.site-logo-img > a.custom-logo-link > img.custom-logo`
      - HTML: `<img width="248" height="51" src="https://comperiaraty.pl/wp-content/uploads/2023/08/comperiaraty-logo.png" class="custom-logo" alt="Logo ComperiaRaty" decoding="async">`
- Strona: /author/admin/
  - Problem: Serves images with low resolution (Lighthouse, -3.8 pkt w kategorii Best Practices).
  - Elementy: 1 — te same selektory co przy pierwszej stronie.
- Strona: /polityka-prywatnosci/
  - Problem: Serves images with low resolution (Lighthouse, -3.8 pkt w kategorii Best Practices).
  - Elementy: 1 — te same selektory co przy pierwszej stronie.
- Strona: /regulamin/
  - Problem: Serves images with low resolution (Lighthouse, -3.8 pkt w kategorii Best Practices).
  - Elementy: 1 — te same selektory co przy pierwszej stronie.
- Strona: /test/
  - Problem: Serves images with low resolution (Lighthouse, -3.8 pkt w kategorii Best Practices).
  - Elementy: 1 — te same selektory co przy pierwszej stronie.
- Strona: /wspolpraca/
  - Problem: Serves images with low resolution (Lighthouse, -3.8 pkt w kategorii Best Practices).
  - Elementy: 1 — te same selektory co przy pierwszej stronie.

## Do ręcznej weryfikacji (axe incomplete)

### [info] a11y-color-contrast — 2 z 6 stron

- Naprawa: Ensure the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds Dokumentacja: https://dequeuniversity.com/rules/axe/4.14/color-contrast?application=playwright
- Strona: /
  - Problem: Elements must meet minimum color contrast ratio thresholds (10 elem., impact: serious).
  - Elementy (10 z 10):
    - Selektor: `.elementor-element-2c18e77 > .elementor-widget-container > p`
      - HTML: `<p>szybko i bezpiecznie!</p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.elementor-widget-container > h2`
      - HTML: `<h2 class="elementor-heading-title elementor-size-default">Weź pożyczkę</h2>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.info-box`
      - HTML: `<div class="info-box">`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.info-box > p:nth-child(1)`
      - HTML: `<p>Rata już od: <span><span id="rata">402 zł</span> </span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.info-box > p:nth-child(2)`
      - HTML: `<p>Termin spłaty: <span class="full-date"><span id="day">25</span>.<span class="span" id="month">11</span>.<span class="span" id="year">2031</span></span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `.open-modal`
      - HTML: `<a href="#" class="open-modal">Warunki pożyczki</a>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `#day`
      - HTML: `<span id="day">25</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `#month`
      - HTML: `<span class="span" id="month">11</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `#rata`
      - HTML: `<span id="rata">402 zł</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
    - Selektor: `#year`
      - HTML: `<span class="span" id="year">2031</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because element contains an image node
- Strona: /test/
  - Problem: Elements must meet minimum color contrast ratio thresholds (9 elem., impact: serious).
  - Elementy (9 z 9):
    - Selektor: `.elementor-heading-title`
      - HTML: `<h2 class="elementor-heading-title elementor-size-default">Test</h2>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it is overlapped by another element
    - Selektor: `.info-box`
      - HTML: `<div class="info-box">`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element
    - Selektor: `.info-box > p:nth-child(1)`
      - HTML: `<p>Rata już od: <span><span id="rata">402 zł</span> </span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element
    - Selektor: `.open-modal`
      - HTML: `<a href="#" class="open-modal">Warunki pożyczki</a>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element
    - Selektor: `#day`
      - HTML: `<span id="day">25</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element
    - Selektor: `#month`
      - HTML: `<span class="span" id="month">11</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element
    - Selektor: `#rata`
      - HTML: `<span id="rata">402 zł</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it partially overlaps other elements
    - Selektor: `#year`
      - HTML: `<span class="span" id="year">2031</span>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element
    - Selektor: `p:nth-child(2)`
      - HTML: `<p>Termin spłaty: <span class="full-date"><span id="day">25</span>.<span class="span" id="month">11</span>.<span class="span" id="year">2031</span></span></p>`
      - Do zrobienia: Fix any of the following: Element's background color could not be determined because it's partially obscured by another element

## Zaliczone reguły (na wszystkich stronach)

a11y-aria-command-name, a11y-aria-conditional-attr, a11y-aria-deprecated-role, a11y-aria-hidden-body, a11y-aria-hidden-focus, a11y-aria-prohibited-attr, a11y-aria-required-attr, a11y-aria-roles, a11y-aria-valid-attr, a11y-aria-valid-attr-value, a11y-avoid-inline-spacing, a11y-bypass, a11y-document-title, a11y-duplicate-id-aria, a11y-form-field-multiple-labels, a11y-html-has-lang, a11y-html-lang-valid, a11y-image-alt, a11y-input-button-name, a11y-link-in-text-block, a11y-list, a11y-listitem, a11y-meta-viewport, a11y-nested-interactive, a11y-scrollable-region-focusable, a11y-target-size, seo-broken-links, seo-duplicate-description, seo-duplicate-title, seo-http-status, seo-https, seo-noindex, seo-page-error, seo-redirects, seo-robots-txt, seo-sitemap, seo-viewport

## Ponowny audyt

`npm --prefix audit-seo run audit -- https://comperiaraty.pl/` w katalogu głównym repozytorium web-audit.
