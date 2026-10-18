import unittest

from crosstab import combo_by_price_band, combo_counts


def rows(*pairs):
    return [{"name": str(i), "price": p, "combo_type": t, "review_count": 0} for i, (t, p) in enumerate(pairs)]


class Step4(unittest.TestCase):
    def test_counts_order(self):
        data = rows(("화장품", 1), ("단독", 2), ("화장품", 3), ("단독", 4), ("건강식품", 5))
        self.assertEqual(combo_counts(data), [("단독", 2), ("화장품", 2), ("건강식품", 1)])

    def test_counts_empty(self):
        self.assertEqual(combo_counts([]), [])

    def test_band_table(self):
        data = rows(("단독", 10000), ("단독", 10001), ("화장품", 20000), ("화장품", 20001), ("화장품", 5))
        self.assertEqual(
            combo_by_price_band(data, [10000, 20000]),
            {
                "단독": {"~10000": 1, "10001~20000": 1, "20001~": 0},
                "화장품": {"~10000": 1, "10001~20000": 1, "20001~": 1},
            },
        )

    def test_single_band(self):
        self.assertEqual(
            combo_by_price_band(rows(("단독", 50), ("단독", 150)), [100]),
            {"단독": {"~100": 1, "101~": 1}},
        )

    def test_empty_rows(self):
        self.assertEqual(combo_by_price_band([], [100]), {})

    def test_bad_bands(self):
        for bad in ([], [200, 100], [100, 100], [1.5], ["a"], None):
            with self.assertRaises(ValueError):
                combo_by_price_band(rows(("단독", 1)), bad)


if __name__ == "__main__":
    unittest.main()
