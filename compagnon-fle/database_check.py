#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from database import database_health_report


def main() -> int:
    report = database_health_report()
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
