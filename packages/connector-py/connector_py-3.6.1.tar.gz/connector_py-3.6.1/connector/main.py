import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="(Lumos) Connectors CLI")
    parser.add_argument(
        "--version", "-v", help="Print the version of this library and exit", action="store_true"
    )

    subparsers = parser.add_subparsers(dest="command")

    scaffold_parser = subparsers.add_parser("scaffold", help="Create a new connector")
    scaffold_parser.add_argument("name", help="Name of the new connector")
    scaffold_parser.add_argument(
        "directory", type=Path, help="Directory to create the connector in"
    )
    scaffold_parser.add_argument("--force-overwrite", "-f", action="store_true")
    scaffold_parser.add_argument("--tests-only", "-t", action="store_true")

    args = parser.parse_args()

    if args.version:
        from connector.__about__ import __version__

        print(__version__)
        return
    elif args.command == "scaffold":
        from connector.scaffold.create import scaffold

        scaffold(args)


if __name__ == "__main__":
    main()
