import unittest

from dork_parser import parse_query


class ParserTests(unittest.TestCase):
    def test_operator_parsing(self):
        result = parse_query('site:example.com filetype:pdf annual report')
        self.assertEqual(result.operators["site"], ["example.com"])
        self.assertEqual(result.operators["filetype"], ["pdf"])
        self.assertEqual(result.plain_terms, ["annual", "report"])
        self.assertEqual(result.risk_score, 0)

    def test_risk_detection(self):
        result = parse_query('site:test.local "index of" .env password')
        self.assertIn("directory_listing", result.risk_signals)
        self.assertIn("sensitive_file", result.risk_signals)
        self.assertIn("credential_keyword", result.risk_signals)
        self.assertGreaterEqual(result.risk_score, 60)

    def test_unknown_operator(self):
        result = parse_query('foo:bar intitle:dashboard')
        self.assertIn("foo", result.unsupported_operators)
        self.assertIn("intitle", result.operators)


if __name__ == "__main__":
    unittest.main()
