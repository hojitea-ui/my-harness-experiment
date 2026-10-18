import unittest

from schema import validate_row


def raw(**kw):
    base = {"name": "박스", "price": "12900", "combo_type": "단독", "review_count": "3"}
    base.update(kw)
    return base


class Step1(unittest.TestCase):
    def test_valid_row_is_typed(self):
        self.assertEqual(
            validate_row(raw()),
            {"name": "박스", "price": 12900, "combo_type": "단독", "review_count": 3},
        )

    def test_strips_and_removes_commas(self):
        out = validate_row(raw(name="  박스 ", price=" 12,900 ", combo_type=" 화장품 "))
        self.assertEqual((out["name"], out["price"], out["combo_type"]), ("박스", 12900, "화장품"))

    def test_blank_or_missing_review_count_is_zero(self):
        self.assertEqual(validate_row(raw(review_count=""))["review_count"], 0)
        self.assertEqual(validate_row(raw(review_count="  "))["review_count"], 0)
        r = raw()
        del r["review_count"]
        self.assertEqual(validate_row(r)["review_count"], 0)
        self.assertEqual(validate_row(raw(review_count=None))["review_count"], 0)

    def test_bad_name(self):
        for bad in ("", "   ", None):
            with self.assertRaises(ValueError):
                validate_row(raw(name=bad))

    def test_bad_price(self):
        for bad in ("", "abc", "12.5", "0", "-100", None):
            with self.assertRaises(ValueError):
                validate_row(raw(price=bad))

    def test_bad_combo_type(self):
        for bad in ("", "  ", None):
            with self.assertRaises(ValueError):
                validate_row(raw(combo_type=bad))

    def test_bad_review_count(self):
        for bad in ("x", "-1", "2.5"):
            with self.assertRaises(ValueError):
                validate_row(raw(review_count=bad))

    def test_missing_keys_are_errors(self):
        for key in ("name", "price", "combo_type"):
            r = raw()
            del r[key]
            with self.assertRaises(ValueError):
                validate_row(r)


if __name__ == "__main__":
    unittest.main()
