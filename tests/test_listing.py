import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import check  # noqa: E402
import listing  # noqa: E402

GOOD = {
    "name": "thing",
    "url": "https://github.com/someone/thing",
    "description": "Does a thing.",
    "category": "tooling",
}


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        shutil.copytree(ROOT / "schema", self.root / "schema")
        shutil.copy(ROOT / "categories.json", self.root / "categories.json")
        shutil.copy(ROOT / "template.md", self.root / "template.md")
        (self.root / "entries").mkdir()

    def entry(self, name, doc):
        text = doc if isinstance(doc, str) else json.dumps(doc)
        (self.root / "entries" / name).write_text(text)

    def problems(self):
        return listing.load(self.root)[2]


class LoadTest(Fixture):
    def test_good_entry(self):
        self.entry("thing.json", GOOD)
        cats, entries, problems = listing.load(self.root)
        self.assertEqual(problems, [])
        self.assertEqual(entries, [{"id": "thing", **GOOD}])

    def test_rejects_missing_field(self):
        self.entry("thing.json", {k: v for k, v in GOOD.items() if k != "url"})
        self.assertIn("'url' is a required property", self.problems()[0])

    def test_rejects_extra_field(self):
        self.entry("thing.json", {**GOOD, "stars": 3})
        self.assertIn("Additional properties", self.problems()[0])

    def test_rejects_description_without_period(self):
        self.entry("thing.json", {**GOOD, "description": "Does a thing"})
        self.assertEqual(len(self.problems()), 1)

    def test_rejects_plain_http(self):
        self.entry("thing.json", {**GOOD, "url": "http://example.com"})
        self.assertEqual(len(self.problems()), 1)

    def test_rejects_archived_false(self):
        self.entry("thing.json", {**GOOD, "archived": False})
        self.assertEqual(len(self.problems()), 1)

    def test_rejects_unknown_category(self):
        self.entry("thing.json", {**GOOD, "category": "nope"})
        self.assertIn("unknown category 'nope'", self.problems()[0])

    def test_rejects_bad_file_name(self):
        self.entry("Thing.json", GOOD)
        self.assertIn("file name", self.problems()[0])

    def test_rejects_invalid_json(self):
        self.entry("thing.json", "{")
        self.assertIn("invalid json", self.problems()[0])


class BuildTest(Fixture):
    def test_orders_by_category_then_name(self):
        self.entry("b.json", {**GOOD, "name": "b", "category": "web"})
        self.entry("a.json", {**GOOD, "name": "a", "category": "web"})
        self.entry("z.json", {**GOOD, "name": "z", "category": "core"})
        out = self.root / "out"
        out.mkdir()
        self.assertEqual(build.build(self.root, out), 3)
        data = json.loads((out / "entries.json").read_text())
        self.assertEqual([e["id"] for e in data["entries"]], ["z", "a", "b"])
        readme = (out / "README.md").read_text()
        self.assertIn("- [Language](#language)", readme)
        self.assertNotIn("#tooling", readme)
        self.assertIn("- [a](https://github.com/someone/thing) - Does a thing.", readme)
        self.assertNotIn("{{", readme)

    def test_lists_archived_entries_in_their_own_section(self):
        self.entry("a.json", {**GOOD, "name": "a", "category": "web"})
        self.entry("old.json", {**GOOD, "name": "old", "category": "web", "archived": True})
        out = self.root / "out"
        out.mkdir()
        self.assertEqual(build.build(self.root, out), 2)
        readme = (out / "README.md").read_text()
        self.assertIn("- [Archived](#archived)", readme)
        web, archived = readme.split("## Web")[1].split("## Archived")
        self.assertIn("- [a]", web)
        self.assertNotIn("- [old]", web)
        self.assertIn("- [old]", archived)
        data = json.loads((out / "entries.json").read_text())
        self.assertTrue(next(e for e in data["entries"] if e["id"] == "old")["archived"])

    def test_refuses_to_build_with_problems(self):
        self.entry("thing.json", {**GOOD, "category": "nope"})
        with self.assertRaises(SystemExit):
            build.build(self.root, self.root)


class UrlTest(unittest.TestCase):
    def meta(self, **fields):
        res = mock.MagicMock()
        res.__enter__.return_value.read.return_value = json.dumps(fields).encode()
        return res

    def test_github_archived_unmarked(self):
        with mock.patch.object(check, "request", return_value=self.meta(private=False, archived=True)):
            self.assertEqual(
                check.url_problem("https://github.com/a/b", None),
                'repository is archived, mark the entry "archived": true',
            )

    def test_github_archived_marked(self):
        with mock.patch.object(check, "request", return_value=self.meta(private=False, archived=True)):
            self.assertIsNone(check.url_problem("https://github.com/a/b", None, archived=True))

    def test_github_marked_but_live(self):
        with mock.patch.object(check, "request", return_value=self.meta(private=False, archived=False)):
            self.assertEqual(
                check.url_problem("https://github.com/a/b", None, archived=True),
                "entry is marked archived but the repository is not",
            )

    def test_github_private(self):
        with mock.patch.object(check, "request", return_value=self.meta(private=True, archived=False)):
            self.assertEqual(check.url_problem("https://github.com/a/b/", None), "repository is private")

    def test_github_live(self):
        with mock.patch.object(check, "request", return_value=self.meta(private=False, archived=False)):
            self.assertIsNone(check.url_problem("https://github.com/a/b", None))

    def test_github_missing(self):
        err = check.urllib.error.HTTPError("u", 404, "nf", {}, None)
        with mock.patch.object(check, "request", side_effect=err):
            self.assertEqual(check.url_problem("https://github.com/a/b", None), "repository not found or not public")

    def test_non_github_dead(self):
        err = check.urllib.error.HTTPError("u", 410, "gone", {}, None)
        with mock.patch.object(check, "request", side_effect=err):
            self.assertEqual(check.url_problem("https://example.com/x", None), "returned 410")

    def test_non_github_falls_back_to_get(self):
        err = check.urllib.error.HTTPError("u", 405, "no head", {}, None)
        with mock.patch.object(check, "request", side_effect=[err, mock.MagicMock()]):
            self.assertIsNone(check.url_problem("https://example.com/x", None))


if __name__ == "__main__":
    unittest.main()
