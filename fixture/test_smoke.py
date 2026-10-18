"""시작 상태부터 통과해야 하고, 어느 단계를 구현해도 계속 통과해야 하는 최소 점검."""
import unittest
from pathlib import Path

import parse_file
import schema
import stats


class Smoke(unittest.TestCase):
    def test_modules_expose_entry_points(self):
        self.assertEqual(schema.FIELDS, ("name", "price", "combo_type", "review_count"))
        self.assertTrue(callable(schema.validate_row))
        self.assertTrue(callable(parse_file.parse_csv))
        self.assertTrue(callable(stats.price_stats))
        self.assertTrue(callable(stats.price_histogram))

    def test_sample_csv_header(self):
        first = (Path(__file__).parent / "sample.csv").read_text(encoding="utf-8").splitlines()[0]
        self.assertEqual(first, "name,price,combo_type,review_count")


if __name__ == "__main__":
    unittest.main()
