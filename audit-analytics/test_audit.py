"""Testy parserów audit.py (bez przeglądarki): uv run python -m unittest test_audit.py"""
import json
import tempfile
import unittest
from pathlib import Path

from audit import (EMAIL_RE, check_privacy, find_consent_buttons, find_secrets, ga4_hits, har_entries, leak_hits,
                   load_passes, make_masker, validate_ecommerce, classify_consent)
from evidence import _snippets

JWT = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4In0.c2lnbmF0dXJl"


class AuditParsers(unittest.TestCase):
    def test_find_secrets_takes_token_not_slug(self):
        self.assertEqual(find_secrets("https://x.pl/psychometry-test/7ea9b4c53c?lang=pl", []), ["7ea9b4c53c"])

    def test_mask_token_email_jwt(self):
        mask = make_masker(["7ea9b4c53c"])
        self.assertEqual(mask("/t/7ea9b4c53c jan@example.com " + JWT), "/t/7ea9… ja…@example.com eyJ…(JWT)")

    def test_ga4_batch_post_splits_events(self):
        req = {"t": 1, "phase": "przed", "host": "region1.google-analytics.com",
               "url": "https://region1.google-analytics.com/g/collect?v=2&tid=G-TEST&dl=https%3A%2F%2Fx.pl%2F",
               "post_body": "en=scroll&epn.percent_scrolled=90\r\nen=page_view&dr=https%3A%2F%2Fx.pl%2Fa"}
        hits = ga4_hits([req])
        self.assertEqual([h["params"]["en"] for h in hits], ["scroll", "page_view"])
        self.assertEqual(hits[1]["params"]["tid"], "G-TEST")

    def test_leak_detects_token_and_jwt_only_on_third_party(self):
        reqs = [
            {"t": 1, "phase": "przed", "host": "api.x.pl", "url": "https://api.x.pl/t/7ea9b4c53c", "referer": None, "post_body": None},
            {"t": 2, "phase": "przed", "host": "intake.dd.eu", "url": "https://intake.dd.eu/rum", "referer": None,
             "post_body": '{"url":"https://x.pl/t/7ea9b4c53c","referrer":"https://api.x.pl/' + JWT + '"}'},
        ]
        leaks = leak_hits(reqs, "www.x.pl", ["7ea9b4c53c"])
        self.assertEqual(len(leaks), 1)
        self.assertIn("token 7ea9… (pola: url)", leaks[0]["what"])
        self.assertTrue(any(w.startswith("JWT") for w in leaks[0]["what"]))

    def test_mask_percent_encoded_email(self):
        self.assertEqual(make_masker([])("x?email=jan%40example.com"), "x?email=ja…@example.com")

    def test_snippets_never_cut_token_open(self):
        # JWT tuż przed tokenem: okno fragmentu zaczyna się w środku JWT — nie może zostać jawny
        body = '{"url":"https://x.pl/t/' + JWT + '/pl","referrer":"https://x.pl/t/7ea9b4c53c"}'
        frags = _snippets(body, make_masker(["7ea9b4c53c"]))
        self.assertTrue(frags)
        self.assertFalse(any("eyJzdWIi" in f or "c2lnbmF0dXJl" in f for f in frags))

    def test_har_numbering_from_one_and_load_skips_files(self):
        with tempfile.TemporaryDirectory() as d:
            har = Path(d) / "network.har"
            har.write_text(json.dumps({"log": {"entries": [
                {"request": {"url": "https://a"}, "startedDateTime": "2026-01-01T00:00:00Z", "response": {"status": 200}}]}}))
            idx, start = har_entries(har)
            self.assertEqual((idx["https://a"][0]["n"], start), (1, "2026-01-01T00:00:00Z"))
            (Path(d) / "raw").mkdir()
            (Path(d) / "raw" / ".DS_Store").write_text("")
            self.assertEqual(load_passes(Path(d)), {})

    def test_validate_ecommerce_rules(self):
        dl = [
            {"ecommerce": None},
            {"event": "view_item", "ecommerce": {"value": "10", "items": [{"item_id": "A", "price": "10"}]}},
            {"event": "view_item_list", "ecommerce": {"currency": "PLN", "items": [{"price": 5}]}},
            {"event": "productImpression", "ecommerce": {"impressions": [{"id": "A"}]}},
        ]
        ga4 = [{"params": {"en": "view_item", "pr1": "idA"}}]
        rows, seen = validate_ecommerce([{"url": "https://x.pl/p", "datalayer": dl}], ga4)
        problems = {(r[1], r[2].split(" (")[0]) for r in rows}
        self.assertIn(("view_item", "`value` bez `currency`"), problems)
        self.assertIn(("view_item", "`items[].price` nie jest liczbą"), problems)
        self.assertIn(("view_item_list", "1 z 1 produktów bez `item_id` i `item_name`"), problems)
        self.assertIn(("view_item_list", "brak `dataLayer.push({ecommerce: null})` przed zdarzeniem — dziedziczy poprzedni obiekt"), problems)
        self.assertIn(("view_item_list", "zdarzenie w dataLayer, ale brak żądania GA4 z tym `en`"), problems)
        self.assertTrue(any(r[1] == "productImpression" and "Universal Analytics" in r[2] for r in rows))
        # null wcześniej + push bez klucza `ecommerce` pomiędzy = model czysty, bez zgłoszenia
        rows2, _ = validate_ecommerce([{"url": "u", "datalayer": [{"ecommerce": None}, {"event": "pageview"},
                                        {"event": "view_item_list", "ecommerce": {"items": [{"item_id": "A"}]}}]}], [])
        self.assertFalse(any("ecommerce: null" in r[2] for r in rows2))
        self.assertEqual(seen["view_item"], 1)

    def test_secrets_fragment_base64_and_slug(self):
        self.assertEqual(find_secrets("https://app.x.pl/#/test/7ea9b4c53c11", []), ["7ea9b4c53c11"])
        self.assertEqual(find_secrets("https://x.pl/t?k=ab12+cd/ef==", []), ["ab12+cd/ef=="])
        self.assertEqual(find_secrets("https://shop.pl/p/buty-nike-air-max-90-123456", []), [])

    def test_mask_name_variants_and_bare_phone(self):
        mask = make_masker(["Jan Kowalski"])
        self.assertEqual(mask("q=Jan+Kowalski&n=JAN KOWALSKI"), "q=JanK…&n=JanK…")
        self.assertEqual(mask("tel=+48500600700"), "tel=+48…")

    def test_email_regex_skips_versions_and_images(self):
        self.assertEqual(EMAIL_RE.findall("rum@5.23.3 logo@2x.webp jan@example.com"), ["jan@example.com"])

    def test_ecommerce_gtag_refund_and_value_events(self):
        dl = [["event", "view_item", {"items": [{"item_id": "A"}]}],
              {"ecommerce": None}, {"event": "refund", "ecommerce": {"transaction_id": "T1", "value": 5, "currency": "PLN"}},
              {"ecommerce": None}, {"event": "begin_checkout", "ecommerce": {"items": [{"item_id": "A"}]}}]
        rows, seen = validate_ecommerce([{"url": "u", "datalayer": dl}], [])
        problems = {(r[1], r[2]) for r in rows}
        self.assertEqual(seen["view_item"], 1)  # gtag() też jest walidowany
        self.assertIn(("view_item", "brak `value` (zalecane do raportowania)"), problems)
        self.assertIn(("begin_checkout", "brak `value` (zalecane do raportowania)"), problems)
        self.assertFalse(any(r[1] == "refund" and "items" in r[2] for r in rows))
        self.assertFalse(any(r[1] == "view_item" and "ecommerce: null" in r[2] for r in rows))


    def test_classify_consent_modes(self):
        v2 = {"ad_storage": "denied", "analytics_storage": "denied", "ad_user_data": "denied", "ad_personalization": "denied"}
        def p(cmds=(), **hits):  # hits: przed=[gcs…], po=[gcs…]; None = żądanie bez gcs
            return {"datalayer": [{"datalayer": [list(c) for c in cmds]}],
                    "ga4": [{"phase": ph, "params": {} if g is None else {"gcs": g}} for ph, gs in hits.items() for g in gs]}
        grant = ["consent", "update", {k: "granted" for k in v2}]
        # Zaawansowany i poprawny: pingi denied przed zgodą, granted po akceptacji.
        mode, rows = classify_consent({"A": p([["consent", "default", v2]], przed=["G100"]),
                                       "B": p([["consent", "default", v2]], przed=["G100"], po=["G100"]),
                                       "C": p([["consent", "default", v2], grant], przed=["G100"], po=["G111"])})
        self.assertEqual(mode, "zaawansowany")
        self.assertEqual([r[2] for r in rows], ["info"])
        # Podstawowy: zero GA4 przed zgodą; odpalenie po odrzuceniu = błąd.
        mode, rows = classify_consent({"A": p(), "B": p(po=["G100"]), "C": p([grant], po=["G111"])})
        self.assertEqual(mode, "podstawowy")
        self.assertTrue(any("mimo odmowy" in r[1] for r in rows))
        # Default bez parametrów v2 i z granted; brak CM w ogóle.
        mode, rows = classify_consent({"A": p([["consent", "default", {"ad_storage": "denied", "analytics_storage": "granted"}]], przed=["G101"])})
        self.assertEqual(mode, "zaawansowany z błędem stanu domyślnego")
        self.assertTrue(any("ad_user_data" in r[1] for r in rows) and any("granted" in r[1] for r in rows))
        self.assertEqual(classify_consent({"A": p(przed=[None])})[0], "brak Consent Mode")


class BrowserSafety(unittest.TestCase):
    """Lokalny HTML (set_content), bez ruchu sieciowego poza 127.0.0.1:9 (odrzucane połączenie)."""

    HTML = """
    <form action="/start-test"><p>Wyrażam zgodę na przetwarzanie danych (RODO).</p>
      <button type="submit">Zgadzam się</button></form>
    <div style="position:fixed;bottom:0">Ta strona używa plików cookie.
      <button>Akceptuję wszystkie</button><button>Odrzuć</button></div>
    <a href="http://127.0.0.1:9/polityka-prywatnosci">Polityka prywatności</a>
    <a href="http://127.0.0.1:9/rodo/withdraw/abc">Polityka — wycofaj zgodę</a>
    <a href="http://127.0.0.1:9/polityka/7ea9b4c53c">Polityka z tokenem</a>"""

    def test_clicks_only_cookie_banner_and_skips_unsafe_links(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.set_content(self.HTML)
            buttons = find_consent_buttons(page)
            self.assertEqual(buttons["accept"]["text"], "Akceptuję wszystkie")
            self.assertEqual(buttons["reject"]["text"], "Odrzuć")
            page.set_content(self.HTML.replace("<div style=\"position:fixed;bottom:0\">", "<div>"))
            self.assertIsNone(find_consent_buttons(page)["accept"])  # sam formularz RODO → brak kliknięcia
            checked = check_privacy(page, context, ["7ea9b4c53c"])["checked"]
            self.assertEqual([c["href"] for c in checked], ["http://127.0.0.1:9/polityka-prywatnosci"])
            browser.close()


if __name__ == "__main__":
    unittest.main()
