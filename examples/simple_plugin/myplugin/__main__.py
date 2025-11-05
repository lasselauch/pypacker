"""Main entry point for the simple plugin."""

import sys

# !!! PACK HERE !!!

import myplugin

def main():
    """Main plugin function."""
    print(f"Simple Plugin v{__version__}")

    # Call core functionality
    myplugin.core.do_something()

    # Use helper utilities
    result = myplugin.utils.helper.process_text("hello from helper")
    print(f"Helper function result: {result}")

if __name__ == "__main__":
    # Plugin metadata
    __version__ = "1.0"
    __plugin_name__ = "Simple Plugin"

    main()
