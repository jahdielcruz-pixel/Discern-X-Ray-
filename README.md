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

Run the CLI:

```bash
discernx
```

Analyze text for risk signals:

```bash
discernx --text "Your text here"
```

Example output (JSON):

```json
{
  "input_text": "This is shocking news! They don't want you to know this secret.",
  "overall_risk": 25,
  "notes": [...],
  "claims": [...]
}
```

Check version:

```bash
discernx --version
```
