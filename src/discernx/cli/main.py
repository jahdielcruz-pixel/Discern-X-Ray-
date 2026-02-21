import argparse
import json
from discernx.analysis import analyze_text, to_dict

def main():
    parser = argparse.ArgumentParser(description="Discern-X-Ray CLI proof of concept")
    parser.add_argument('--version', action='version', version='discernx 0.1.0')
    parser.add_argument('--text', type=str, help='Text to analyze for risk signals')
    args = parser.parse_args()

    if args.text:
        result = analyze_text(args.text)
        print(json.dumps(to_dict(result), indent=2))
    else:
        print("Welcome to Discern-X-Ray CLI! Use --text to analyze some text.")