from collections import Counter


def price_stats(rows):
    prices = sorted(r["price"] for r in rows)
    n = len(prices)
    if n == 0:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    if n % 2:
        median = prices[n // 2]
    else:
        median = (prices[n // 2 - 1] + prices[n // 2]) // 2
    return {"count": n, "min": prices[0], "max": prices[-1], "mean": sum(prices) // n, "median": median}


def price_histogram(rows, bin_size):
    if bin_size <= 0:
        raise ValueError("bin_size must be positive")
    if not rows:
        return []
    counts = Counter((r["price"] // bin_size) * bin_size for r in rows)
    lo, hi = min(counts), max(counts)
    return [(start, counts.get(start, 0)) for start in range(lo, hi + 1, bin_size)]
