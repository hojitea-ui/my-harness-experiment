FIELDS = ("name", "price", "combo_type", "review_count")


def _text(raw, key):
    value = raw.get(key)
    return "" if value is None else str(value).strip()


def validate_row(raw):
    name = _text(raw, "name")
    if not name:
        raise ValueError("name is required")
    try:
        price = int(_text(raw, "price").replace(",", ""))
    except ValueError:
        raise ValueError("price must be an integer")
    if price <= 0:
        raise ValueError("price must be positive")
    combo_type = _text(raw, "combo_type")
    if not combo_type:
        raise ValueError("combo_type is required")
    review = _text(raw, "review_count")
    if review == "":
        review_count = 0
    else:
        try:
            review_count = int(review)
        except ValueError:
            raise ValueError("review_count must be an integer")
        if review_count < 0:
            raise ValueError("review_count must not be negative")
    return {"name": name, "price": price, "combo_type": combo_type, "review_count": review_count}
