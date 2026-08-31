#!/usr/bin/env python3
"""Compare scientific markers, numeric bindings, and protected quotes.

This is an alarm, not semantic validation. Reports require manual review and
may include harmless changes.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys


NUMBER_RE = re.compile(
    r"(?<![\w])(?:[+−-]?\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|[+−-]?\d+(?:[.,]\d+)?)(?:[eE][+−-]?\d+)?%?"
)
OPERATOR_RE = re.compile(r"≤|≥|≠|≈|[<>]=?|=")
UNIT_RE = re.compile(
    r"(?<![\w])(?:°\s?[CF]|°Brix|mg/L|g/L|µg/L|ug/L|mL|µL|uL|kg|mg|µg|ug|mmol/L|mol/L|ppm|ppb|kPa|MPa|h|min|s|days?|weeks?|months?|years?)(?![\w])",
    re.IGNORECASE,
)
STAT_RE = re.compile(
    r"(?<![\w])(?:p|q|n|N|SD|SE|CI|OR|RR|HR|df|R²|R2|r|β|beta)(?=\s*(?:[=<>≤≥:]|\d))"
)
QUOTE_RE = re.compile(r'"([^"\n]+)"|“([^”\n]+)”')
CLAUSE_SPLIT_RE = re.compile(
    r"(?<=[.!?])\s+|;\s*|,\s+(?:whereas|while|but|and|where|pero|mientras|aunque|y)\s+",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)?")
STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "had", "has", "in", "is",
    "it", "of", "on", "or", "the", "this", "to", "was", "were", "with",
    "al", "con", "de", "del", "el", "en", "es", "la", "las", "los", "o", "para",
    "por", "se", "un", "una", "y",
}


def inventory(text: str) -> dict[str, Counter[str]]:
    return {
        "numbers": Counter(NUMBER_RE.findall(text)),
        "operators": Counter(OPERATOR_RE.findall(text)),
        "units": Counter(match.group(0) for match in UNIT_RE.finditer(text)),
        "statistics": Counter(match.group(0) for match in STAT_RE.finditer(text)),
    }


def compare(source: str, rewrite: str) -> dict[str, dict[str, dict[str, int]]]:
    left = inventory(source)
    right = inventory(rewrite)
    mismatches: dict[str, dict[str, dict[str, int]]] = {}
    for category in left:
        missing = left[category] - right[category]
        added = right[category] - left[category]
        if missing or added:
            mismatches[category] = {
                "missing_from_rewrite": dict(missing),
                "added_in_rewrite": dict(added),
            }
    return mismatches


def quoted_spans(text: str) -> list[str]:
    """Return straight- or curly-quoted single-line spans without delimiters."""
    return [next(group for group in match.groups() if group is not None) for match in QUOTE_RE.finditer(text)]


def quote_mismatches(source: str, rewrite: str) -> dict[str, object]:
    """Report quote inventory changes when wording is expected to remain exact."""
    left = Counter(quoted_spans(source))
    right = Counter(quoted_spans(rewrite))
    missing = left - right
    added = right - left
    return {
        "changed": bool(missing or added),
        "missing_from_rewrite": dict(missing),
        "added_in_rewrite": dict(added),
    }


def _marker_contexts(text: str) -> dict[str, list[str]]:
    contexts: dict[str, list[str]] = {}
    for clause in CLAUSE_SPLIT_RE.split(text):
        clean = " ".join(clause.split())
        if not clean:
            continue
        for marker in NUMBER_RE.findall(clean):
            contexts.setdefault(marker, []).append(clean)
    return contexts


def _keywords(context: str) -> set[str]:
    return {
        word.lower()
        for word in WORD_RE.findall(context)
        if word.lower() not in STOPWORDS
    }


def _similarity(left: str, right: str) -> float:
    left_words = _keywords(left)
    right_words = _keywords(right)
    if not left_words and not right_words:
        return 1.0
    union = left_words | right_words
    return len(left_words & right_words) / len(union) if union else 1.0


def binding_changes(source: str, rewrite: str, threshold: float = 0.6) -> list[dict[str, object]]:
    """Flag values whose nearby subject or comparison may have changed.

    This heuristic is intentionally conservative. It compares the nearest
    clause around each literal value and must be reviewed by a person or model.
    """
    left = _marker_contexts(source)
    right = _marker_contexts(rewrite)
    changes: list[dict[str, object]] = []
    for marker in sorted(set(left) & set(right)):
        if len(left[marker]) != len(right[marker]):
            continue
        unmatched = list(right[marker])
        for source_context in left[marker]:
            scored = [(_similarity(source_context, candidate), candidate) for candidate in unmatched]
            score, rewrite_context = max(scored, key=lambda item: item[0])
            unmatched.remove(rewrite_context)
            if score < threshold:
                changes.append(
                    {
                        "marker": marker,
                        "source_context": source_context,
                        "rewrite_context": rewrite_context,
                        "similarity": round(score, 3),
                    }
                )
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare numbers, operators, units and statistical labels."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("rewrite", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--bindings",
        action="store_true",
        help="Flag values whose nearby subject or comparison may have changed.",
    )
    parser.add_argument(
        "--protect-quotes",
        action="store_true",
        help="Require quoted spans to remain literal.",
    )
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    rewrite = args.rewrite.read_text(encoding="utf-8")
    mismatches = compare(source, rewrite)
    bindings = binding_changes(source, rewrite) if args.bindings else []
    quotes = quote_mismatches(source, rewrite) if args.protect_quotes else {"changed": False}
    ok = not mismatches and not bindings and not quotes["changed"]

    if args.as_json:
        print(
            json.dumps(
                {
                    "match": ok,
                    "literal_mismatches": mismatches,
                    "potential_binding_changes": bindings,
                    "quote_mismatches": quotes,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    elif ok:
        print("OK: controlled literal markers match.")
        print("Manual semantic review is still required.")
    else:
        print("ALERT: the rewrite may have changed protected scientific content.")
        for category, details in mismatches.items():
            print(f"- {category}: {details}")
        for change in bindings:
            print(f"- possible binding change: {change}")
        if quotes["changed"]:
            print(f"- quoted wording changed: {quotes}")
        print("Also review direction, certainty, scope, limitations, and interpretation.")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
