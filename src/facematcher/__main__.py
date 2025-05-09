"""Main entry point for the facematcher package."""

import logging
import sys
from typing import List

from facematcher.cli.commands import cmd_detect, cmd_compare
from facematcher.cli.parser import parse_args


def main(argv: List[str] | None = None) -> None:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args(argv)
    try:
        if args.func == "detect":
            cmd_detect(args)
        elif args.func == "compare":
            cmd_compare(args)
    except Exception as exc:  # noqa: BLE001
        logging.error("%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main() 