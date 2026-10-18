from bisect import bisect_left
from collections import Counter


def combo_counts(rows):
    counts = Counter(r["combo_type"] for r in rows)
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def combo_by_price_band(rows, bands):
    ok = (
        isinstance(bands, (list, tuple))
        and len(bands) > 0
        and all(isinstance(b, int) and not isinstance(b, bool) for b in bands)
        and all(a < b for a, b in zip(bands, bands[1:]))
    )
    if not ok:
        raise ValueError("bands must be a non-empty, strictly ascending list of ints")
    labels = [f"~{bands[0]}"]
    labels += [f"{bands[i - 1] + 1}~{bands[i]}" for i in range(1, len(bands))]
    labels.append(f"{bands[-1] + 1}~")
    table = {}
    for r in rows:
        label = labels[bisect_left(bands, r["price"])]
        table.setdefault(r["combo_type"], {l: 0 for l in labels})[label] += 1
    return table
