#!/usr/bin/env python3
"""Validate NoolNest bilingual Current Affairs JSON before publication."""
import json
import re
import sys
from pathlib import Path

def validate(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    records = data.get("records") if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise ValueError("Feed must contain a records array")
    dates = set()
    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            raise ValueError(f"records[{i}] must be an object")
        date = rec.get("date", "")
        if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            raise ValueError(f"records[{i}].date must be YYYY-MM-DD")
        if date in dates:
            raise ValueError(f"duplicate date: {date}")
        dates.add(date)
        for exam in ("upsc", "tnpsc"):
            lesson = rec.get(exam)
            if not isinstance(lesson, dict):
                raise ValueError(f"{date}.{exam} required")
            for field in ("title", "summary", "background", "conclusion", "modelEssay"):
                val = lesson.get(field)
                if not isinstance(val, dict) or any(not isinstance(val.get(lang), str) or not val[lang].strip() for lang in ("en", "ta")):
                    raise ValueError(f"{date}.{exam}.{field} requires nonempty en and ta")
            for source in lesson.get("sources", []):
                if not isinstance(source, dict) or not isinstance(source.get("url"), str) or not source["url"].startswith("https://"):
                    raise ValueError(f"{date}.{exam}.sources must use HTTPS URLs")
    print(f"Validated {len(records)} dated records")
if __name__ == "__main__":
    validate(sys.argv[1] if len(sys.argv) > 1 else "current-affairs.json")
