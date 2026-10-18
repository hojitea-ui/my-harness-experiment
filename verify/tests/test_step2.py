import unittest

from parse_file import parse_csv

HEADER = "name,price,combo_type,review_count\n"


class Step2(unittest.TestCase):
    def test_basic(self):
        rows, errors = parse_csv(HEADER + "a,1000,단독,5\nb,\"2,000\",화장품,\n")
        self.assertEqual(errors, [])
        self.assertEqual(
            rows,
            [
                {"name": "a", "price": 1000, "combo_type": "단독", "review_count": 5},
                {"name": "b", "price": 2000, "combo_type": "화장품", "review_count": 0},
            ],
        )

    def test_quoted_comma_in_name(self):
        rows, errors = parse_csv(HEADER + '"박스, 세트",5000,단독,1\n')
        self.assertEqual(errors, [])
        self.assertEqual(rows[0]["name"], "박스, 세트")

    def test_bom_and_column_order_and_extra_columns(self):
        text = "﻿ combo_type ,extra,price,name,review_count\n단독,x,3000,a,2\n"
        rows, errors = parse_csv(text)
        self.assertEqual(errors, [])
        self.assertEqual(rows, [{"name": "a", "price": 3000, "combo_type": "단독", "review_count": 2}])

    def test_missing_header_column_raises(self):
        with self.assertRaises(ValueError):
            parse_csv("name,price,combo_type\na,1,단독\n")
        with self.assertRaises(ValueError):
            parse_csv("")

    def test_errors_carry_file_line_numbers_and_continue(self):
        text = HEADER + "a,1000,단독,1\n\nb,-5,단독,1\nc,2000,화장품,1\nd,10,단독\n"
        rows, errors = parse_csv(text)
        self.assertEqual([r["name"] for r in rows], ["a", "c"])
        self.assertEqual([line for line, _ in errors], [4, 6])
        for _, msg in errors:
            self.assertIsInstance(msg, str)

    def test_blank_lines_skipped(self):
        rows, errors = parse_csv(HEADER + "\n\na,1000,단독,1\n\n")
        self.assertEqual(len(rows), 1)
        self.assertEqual(errors, [])

    def test_header_only(self):
        self.assertEqual(parse_csv(HEADER), ([], []))


if __name__ == "__main__":
    unittest.main()
