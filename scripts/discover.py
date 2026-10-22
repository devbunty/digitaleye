"""Print what Digital Eye can discover on a remote host over SSH.

Usage:  python -m scripts.discover HOST [--user USER]
"""

import argparse

from collector.discovery import Discovery


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("host", help="IP address or hostname of the target")
    parser.add_argument("--user", default="root", help="SSH user (default: root)")
    args = parser.parse_args()

    for section, output in Discovery(args.host, args.user).collect().items():
        print("=" * 70)
        print(section.upper())
        print("=" * 70)
        print(output)


if __name__ == "__main__":
    main()
