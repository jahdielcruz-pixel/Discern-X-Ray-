import argparse

def main():
    parser = argparse.ArgumentParser(description="Discern-X-Ray CLI proof of concept")
    parser.add_argument('--version', action='version', version='discernx 0.1.0')
    args = parser.parse_args()
    print("Welcome to Discern-X-Ray CLI!")