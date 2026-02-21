from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from discernx.core.analyzer import analyze_text, to_dict
from discernx.core.report import to_markdown


def read_input_text(args) -> str:
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    # If neither provided, read stdin (supports piping)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("No input provided. Use --text, --file, or pipe via stdin.")


def cmd_analyze(args) -> int:
    text = read_input_text(args)
    result = analyze_text(text, max_claims=args.max_claims)
    data = to_dict(result)

    if args.format == "json":
        out = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        out = to_markdown(data)

    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"Wrote: {args.out}")
    else:
        print(out)

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="discernx", description="Discern-X-Ray CLI (MVP)")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("analyze", help="Analyze input text for manipulation-style signals")
    a.add_argument("--text", type=str, help="Text to analyze")
    a.add_argument("--file", type=str, help="Path to a text file to analyze")
    a.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    a.add_argument("--out", type=str, help="Write output to a file instead of stdout")
    a.add_argument("--max-claims", type=int, default=12, help="Max number of claims to score")
    a.set_defaults(func=cmd_analyze)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    rc = args.func(args)
    raise SystemExit(rc)