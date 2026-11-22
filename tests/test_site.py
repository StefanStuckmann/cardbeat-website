"""Checks for the site's search and agent metadata. Run: python3 -m unittest discover tests"""
import glob
import html
import json
import os
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = "https://cardbeat.app/"
SM = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9", "xhtml": "http://www.w3.org/1999/xhtml"}


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def url_to_file(url):
    assert url.startswith(ORIGIN), url
    path = url[len(ORIGIN):].split("#")[0]
    if path == "" or path.endswith("/"):
        path += "index.html"
    return path


def html_files():
    return sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True))


def json_ld(path):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', read(path), re.S)
    return [json.loads(b) for b in blocks]


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def attr(path, pattern):
    return re.findall(pattern, read(path))


class StructuredData(unittest.TestCase):
    def test_json_ld_parses(self):
        for path in html_files():
            with self.subTest(path=path):
                json_ld(path)  # raises on invalid JSON

    def test_faq_html_matches_json_ld(self):
        for path in ["index.html", "de/index.html"]:
            with self.subTest(path=path):
                faq = next(d for d in json_ld(path) if d["@type"] == "FAQPage")
                ld = [(q["name"], q["acceptedAnswer"]["text"]) for q in faq["mainEntity"]]
                shown = [
                    (html.unescape(q), html.unescape(re.sub(r"<.*?>", "", a)))
                    for q, a in re.findall(r"<details><summary>(.*?)</summary><div><p>(.*?)</p>", read(path))
                ]
                self.assertEqual(ld, shown)

    def test_author_is_the_same_entity_everywhere(self):
        authors = []
        for path in html_files():
            for node in walk(json_ld(path)):
                if node.get("@type") == "Person" and node.get("name") == "Stefan Stuckmann":
                    authors.append((path, sorted(node.get("sameAs", []))))
        self.assertGreaterEqual(len({p for p, _ in authors}), 3, authors)
        self.assertEqual(len({tuple(s) for _, s in authors}), 1, authors)
        self.assertTrue(authors[0][1], "author has no sameAs links")


class Sitemap(unittest.TestCase):
    def setUp(self):
        self.urls = ET.fromstring(read("sitemap.xml")).findall("sm:url", SM)

    def test_every_entry_is_a_page_with_matching_canonical_and_lastmod(self):
        for url in self.urls:
            loc = url.find("sm:loc", SM).text
            with self.subTest(loc=loc):
                path = url_to_file(loc)
                self.assertIn(f'<link rel="canonical" href="{loc}">', read(path))
                lastmod = url.find("sm:lastmod", SM)
                self.assertIsNotNone(lastmod)
                self.assertRegex(lastmod.text, r"^\d{4}-\d{2}-\d{2}$")

    def test_every_indexable_page_is_listed(self):
        listed = {url_to_file(u.find("sm:loc", SM).text) for u in self.urls}
        for path in html_files():
            if 'name="robots" content="noindex"' not in read(path):
                with self.subTest(path=path):
                    self.assertIn(path, listed)

    def test_hreflang_matches_pages(self):
        for url in self.urls:
            loc = url.find("sm:loc", SM).text
            in_sitemap = sorted((l.get("hreflang"), l.get("href")) for l in url.findall("xhtml:link", SM))
            in_page = sorted(attr(url_to_file(loc), r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">'))
            with self.subTest(loc=loc):
                self.assertEqual(in_sitemap, in_page)


class LlmsTxt(unittest.TestCase):
    def test_links_point_to_existing_pages(self):
        text = read("llms.txt")
        self.assertTrue(text.startswith("# CardBeat\n"))
        links = re.findall(r"\]\((https://cardbeat\.app/[^)]*)\)", text)
        self.assertTrue(links)
        for link in links:
            with self.subTest(link=link):
                self.assertTrue(os.path.exists(os.path.join(ROOT, url_to_file(link))))


if __name__ == "__main__":
    unittest.main()
