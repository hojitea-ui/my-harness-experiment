from crosstab import combo_counts
from stats import price_stats


def build_report(rows, errors):
    s = price_stats(rows)
    lines = [f"분석 대상 {s['count']}건, 오류 {len(errors)}건"]
    if s["count"]:
        lines.append(
            f"가격 최소 {s['min']:,}원 / 최대 {s['max']:,}원 / 평균 {s['mean']:,}원 / 중앙값 {s['median']:,}원"
        )
        lines.append("결합유형별 상품 수")
        lines += [f"- {t}: {c}" for t, c in combo_counts(rows)]
    if errors:
        lines.append("오류 줄: " + ", ".join(str(n) for n, _ in errors))
    return "\n".join(lines)
