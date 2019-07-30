# Very basic unit tests for helper functions.
import unittest

from helpers import is_valid_url, to_emoji_slug


class UrlValidationTest(unittest.TestCase):
    def test_valid_urls(self):
        valid_urls = [
            'https://mishnit.github.io/',
            'https://github.com/mishnit',
            'https://www.getdoozy.com/',
        ]

        self.assertTrue(all([is_valid_url(url) for url in valid_urls]))

    def test_invalid_urls(self):
        invalid_urls = [
            'htp://mishnit.com',
            'mishnit.com',
            'www.mishnit.co',
            'http://subdomain',
        ]

        self.assertFalse(all([is_valid_url(url) for url in invalid_urls]))


class BaseConverterTest(unittest.TestCase):
    def test_valid_urls(self):
        self.assertEqual(to_emoji_slug(0), "😆")
        self.assertEqual(to_emoji_slug(1), "😂")
        self.assertEqual(to_emoji_slug(29), "😩")
        self.assertEqual(to_emoji_slug(30), "😂😆")
        self.assertEqual(to_emoji_slug(31), "😂😂")
        self.assertEqual(to_emoji_slug(299), "😐😩")
        self.assertEqual(to_emoji_slug(300), "😑😆")
        self.assertEqual(to_emoji_slug(301), "😑😂")
        self.assertEqual(to_emoji_slug(4234353453423245324524323452345), "😏🤭😐😎🤫😳😎🙄🤨🤑🤨😶😑🤫😓😭🤗🤭😬😓🤫")


if __name__ == '__main__':
    unittest.main(verbosity=2)
