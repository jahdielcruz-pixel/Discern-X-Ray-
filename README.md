# Discern-X-Ray

Discern-X-Ray CLI proof of concept

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/jahdielcruz-pixel/Discern-X-Ray-.git
cd Discern-X-Ray-
pip install -e .
```

## Usage

Analyze text for risk signals:

```bash
discernx analyze --text "Your text here"
```

Read from a file:

```bash
discernx analyze --file path/to/file.txt
```

Pipe from stdin:

```bash
echo "Some text" | discernx analyze
```

Specify output format (md or json, default md):

```bash
discernx analyze --text "Text" --format json
```

Write output to a file:

```bash
discernx analyze --text "Text" --out report.md
```

Options:
- `--max-claims`: Limit the number of claims to analyze (default 12)

Example markdown output:

# Discern-X-Ray Report

**Overall Risk Score:** 30/100

## Claims

### Claim 1 — Risk 35/100
> This is shocking news!

Signals: `sensational_language`, `very_short`

## Notes
- MVP heuristics only (not fact-checking).
- ...
