import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.language import TITLES, sphinx_lang


class TestLanguage(ExtTestCase):
    def test_titles_en_keys(self):
        self.assertIn("en", TITLES)
        self.assertIn("author", TITLES["en"])
        self.assertIn("book", TITLES["en"])
        self.assertIn("FAQ", TITLES["en"])

    def test_titles_fr_keys(self):
        self.assertIn("fr", TITLES)
        self.assertIn("author", TITLES["fr"])
        self.assertIn("book", TITLES["fr"])
        self.assertIn("FAQ", TITLES["fr"])

    def test_sphinx_lang_no_settings(self):
        class FakeEnv:
            pass

        lang = sphinx_lang(FakeEnv())
        self.assertEqual(lang, "en")

    def test_sphinx_lang_settings_no_language_code(self):
        class FakeSettings:
            pass

        class FakeEnv:
            settings = FakeSettings()

        lang = sphinx_lang(FakeEnv())
        self.assertEqual(lang, "en")

    def test_sphinx_lang_settings_with_language_code(self):
        class FakeSettings:
            language_code = "fr"

        class FakeEnv:
            settings = FakeSettings()

        lang = sphinx_lang(FakeEnv())
        self.assertEqual(lang, "fr")

    def test_sphinx_lang_default_value(self):
        class FakeEnv:
            pass

        lang = sphinx_lang(FakeEnv(), default_value="de")
        self.assertEqual(lang, "en")


if __name__ == "__main__":
    unittest.main(verbosity=2)
