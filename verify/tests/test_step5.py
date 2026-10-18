import unittest

from parse_file import parse_csv
from report import build_report

SAMPLE = (
    "name,price,combo_type,review_count\n"
    "용돈박스 클래식,12900,단독,34\n"
    '"용돈박스, 핸드크림 세트","19,900",화장품,120\n'
    "용돈박스+홍삼스틱,39000,건강식품,58\n"
    "용돈박스 미니,9900,단독,\n"
    "용돈박스+립밤,24500,화장품,17\n"
)

EXPECTED = (
    "분석 대상 5건, 오류 0건\n"
    "가격 최소 9,900원 / 최대 39,000원 / 평균 21,240원 / 중앙값 19,900원\n"
    "결합유형별 상품 수\n"
    "- 단독: 2\n"
    "- 화장품: 2\n"
    "- 건강식품: 1"
)


class Step5(unittest.TestCase):
    def test_sample_report(self):
        rows, errors = parse_csv(SAMPLE)
        self.assertEqual(build_report(rows, errors), EXPECTED)

    def test_report_with_errors(self):
        rows, errors = parse_csv(SAMPLE + "bad,-1,단독,1\nbad2,x,단독,1\n")
        out = build_report(rows, errors)
        self.assertEqual(out, EXPECTED.replace("오류 0건", "오류 2건") + "\n오류 줄: 7, 8")

    def test_no_rows_no_errors(self):
        self.assertEqual(build_report([], []), "분석 대상 0건, 오류 0건")

    def test_no_rows_with_errors(self):
        self.assertEqual(build_report([], [(2, "x"), (5, "y")]), "분석 대상 0건, 오류 2건\n오류 줄: 2, 5")

    def test_no_trailing_newline(self):
        rows, errors = parse_csv(SAMPLE)
        self.assertFalse(build_report(rows, errors).endswith("\n"))


if __name__ == "__main__":
    unittest.main()
