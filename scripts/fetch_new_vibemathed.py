#!/usr/bin/env python3
"""Fetch new, significant VibeMathed achievements.

The output is a JSON array containing the original problem objects returned by
the VibeMathed API. An achievement is included when its significance is at
least the requested threshold and its solveDate is later than the latest date
already present in achievements.json. A month-only solveDate is also included
when it falls in the same month as that latest achievement, because its exact
ordering cannot be determined.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://vibemathed.com/api/dataset"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACHIEVEMENTS_PATH = ROOT / "achievements.json"
DEFAULT_OUTPUT_PATH = ROOT / "vibemathed_new.json"


def parse_date(value: str) -> date:
    """Parse a YYYY-MM, ISO date, or ISO datetime as a calendar date."""
    if len(value) == 7:
        value = f"{value}-01"

    try:
        return date.fromisoformat(value)
    except ValueError:
        # datetime.fromisoformat accepts offsets but uses +00:00 rather than Z.
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()


def is_possibly_newer(solve_date: str, latest_date: date) -> bool:
    """Return whether solve_date is newer or cannot be ordered precisely.

    VibeMathed occasionally reports dates at month resolution (YYYY-MM). If
    that month is the latest achievement's month, include the record because
    it may have been solved after the latest precisely dated achievement.
    """
    if len(solve_date) == 7:
        solve_month = parse_date(solve_date)
        latest_month = latest_date.replace(day=1)
        return solve_month >= latest_month

    return parse_date(solve_date) > latest_date


def most_recent_achievement_date(path: Path) -> date:
    with path.open(encoding="utf-8") as file:
        achievements = json.load(file)

    if not isinstance(achievements, list) or not achievements:
        raise ValueError(f"{path} must contain a non-empty JSON array")

    try:
        return max(parse_date(item["date"]) for item in achievements)
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            f"Every achievement in {path} must have a valid 'date'"
        ) from error


def fetch_dataset(url: str, timeout: float = 30.0) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "AI-Mathematics-Timeline/1.0",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.load(response)

    if not isinstance(payload, dict) or not isinstance(payload.get("problems"), list):
        raise ValueError("VibeMathed response does not contain a 'problems' array")
    return payload


def filter_problems(
    problems: list[dict[str, Any]],
    after: date,
    minimum_significance: float = 40,
) -> list[dict[str, Any]]:
    filtered = []
    for problem in problems:
        significance = problem.get("significance")
        solve_date = problem.get("solveDate")

        # bool is a subclass of int, but it is not a meaningful score here.
        if (
            isinstance(significance, bool)
            or not isinstance(significance, (int, float))
            or significance < minimum_significance
            or not isinstance(solve_date, str)
        ):
            continue

        try:
            is_new = is_possibly_newer(solve_date, after)
        except ValueError:
            continue

        if is_new:
            filtered.append(problem)

    return sorted(filtered, key=lambda problem: parse_date(problem["solveDate"]))


def write_json(problems: list[dict[str, Any]], output: Path | None) -> None:
    if output is None:
        json.dump(problems, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return

    with output.open("w", encoding="utf-8") as file:
        json.dump(problems, file, indent=2, ensure_ascii=False)
        file.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--achievements",
        type=Path,
        default=DEFAULT_ACHIEVEMENTS_PATH,
        help=f"existing achievements file (default: {DEFAULT_ACHIEVEMENTS_PATH})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"output JSON file; use - for stdout (default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "--minimum-significance",
        type=float,
        default=40,
        help="minimum significance score, inclusive (default: 40)",
    )
    parser.add_argument("--url", default=API_URL, help=argparse.SUPPRESS)
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = None if str(args.output) == "-" else args.output

    try:
        latest_date = most_recent_achievement_date(args.achievements)
        dataset = fetch_dataset(args.url, args.timeout)
        problems = filter_problems(
            dataset["problems"], latest_date, args.minimum_significance
        )
        write_json(problems, output)
    except (OSError, HTTPError, URLError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    destination = "stdout" if output is None else str(output)
    print(
        f"Wrote {len(problems)} achievement(s) solved after {latest_date} "
        f"to {destination}.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
