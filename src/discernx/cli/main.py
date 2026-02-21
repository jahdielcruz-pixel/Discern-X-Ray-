import argparse
import json
from discernx.analysis import analyze_text, to_dict, to_markdown

def main():
    parser = argparse.ArgumentParser(description="Discern-X-Ray CLI proof of concept")
    parser.add_argument('--version', action='version', version='discernx 0.1.0')
    parser.add_argument('--text', type=str, help='Text to analyze for risk signals')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json', help='Output format (default: json)')
    args = parser.parse_args()

    if args.text:
        result = analyze_text(args.text)
        data = to_dict(result)
        if args.format == 'markdown':
            print(to_markdown(data))
        else:
            print(json.dumps(data, indent=2))
    else:
        print("Welcome to Discern-X-Ray CLI! Use --text to analyze some text.")