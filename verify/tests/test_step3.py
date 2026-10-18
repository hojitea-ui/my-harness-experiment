import unittest

from stats import price_histogram, price_stats


def rows(*prices):
    return [{"name": str(i), "price": p, "combo_type": "단독", "review_count": 0} for i, p in enumerate(prices)]


class Step3(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            price_stats([]), {"count": 0, "min": None, "max": None, "mean": None, "median": None}
        )

    def test_odd_count(self):
        self.assertEqual(
            price_stats(rows(12900, 19900, 39000, 9900, 24500)),
            {"count": 5, "min": 9900, "max": 39000, "mean": 21240, "median": 19900},
        )

    def test_even_count_median_and_floor(self):
        s = price_stats(rows(1000, 1001, 2000, 2001))
        self.assertEqual(s["median"], 1500)  # (1001+2000)//2
        self.assertEqual(s["mean"], 1500)  # 6002//4

    def test_mean_floors(self):
        self.assertEqual(price_stats(rows(1, 2))["mean"], 1)

    def test_histogram_includes_empty_bins(self):
        self.assertEqual(
            price_histogram(rows(1500, 2500, 12000), 5000),
            [(0, 2), (5000, 0), (10000, 1)],
        )

    def test_histogram_edges(self):
        self.assertEqual(price_histogram(rows(10000), 10000), [(10000, 1)])
        self.assertEqual(price_histogram(rows(9999, 10000), 10000), [(0, 1), (10000, 1)])

    def test_histogram_empty_and_bad_bin(self):
        self.assertEqual(price_histogram([], 1000), [])
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                price_histogram(rows(1000), bad)


if __name__ == "__main__":
    unittest.main()
