import csv
import io

from schema import FIELDS, validate_row


def parse_csv(text):
    reader = csv.reader(io.StringIO(text.lstrip("﻿")))
    header = [h.strip() for h in next(reader, [])]
    missing = [f for f in FIELDS if f not in header]
    if missing:
        raise ValueError("missing column: " + ", ".join(missing))
    index = {name: header.index(name) for name in FIELDS}
    rows, errors = [], []
    for row in reader:
        if not row:
            continue
        if len(row) != len(header):
            errors.append((reader.line_num, "column count mismatch"))
            continue
        try:
            rows.append(validate_row({name: row[i] for name, i in index.items()}))
        except ValueError as exc:
            errors.append((reader.line_num, str(exc)))
    return rows, errors
