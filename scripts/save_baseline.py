"""Capture a discovery snapshot of a remote host as a JSON file.

Usage:  python -m scripts.save_baseline HOST [--user USER] [--output FILE]
"""

import argparse
import json
from pathlib import Path

from collector.discovery import Discovery


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("host", help="IP address or hostname of the target")
    parser.add_argument("--user", default="root", help="SSH user (default: root)")
    parser.add_argument("--output", default="baseline/client_baseline.json", help="where to write the snapshot")
    args = parser.parse_args()

    results = Discovery(args.host, args.user).collect()
    Path(args.output).write_text(json.dumps(results, indent=4), encoding="utf-8")
    print(f"Baseline written to {args.output}")


if __name__ == "__main__":
    main()
