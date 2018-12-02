import unittest

from . import Page


class TestPage(unittest.TestCase):
    "Tests for Page class"

    def setUp(self):
        pass

    def test(self):
        url = "http://fake.dev"
        text = "Text."
        imgs = ["a", "b"]
        p = Page(url, text, imgs)
