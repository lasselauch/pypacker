#!/usr/bin/env python3
"""Command-line interface for Python Script Packer."""

import sys
from .pack import pack


def main():
    """Main entry point for the CLI."""
    # check arguments
    if len(sys.argv) < 6:
        print(f"Usage: {sys.argv[0]} <2.7|3.5> <output-path> <product-name> <module-name> <library-path> [...]")
        sys.exit(1)

    try:
        # extract arguments
        dialect = sys.argv[1]
        output_path = sys.argv[2]
        product_name = sys.argv[3]
        module_name = sys.argv[4]
        library_paths = sys.argv[5:]

        # pack
        packed = pack(dialect, product_name, module_name, library_paths)

        # write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(packed)

        sys.exit(0)

    except Exception as error:
        print(f"An error occurred: {error}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
