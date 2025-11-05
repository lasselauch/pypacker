# Simple Plugin Example

This example demonstrates how to use pypacker to bundle a simple plugin.

## Project Structure

```
simple_plugin/
├── myplugin/
│   ├── __init__.py
│   ├── __main__.py        # Entry point
│   ├── pack.list          # Defines what to pack
│   ├── core.py            # Core functionality
│   └── utils/
│       ├── __init__.py
│       └── helper.py      # Helper utilities
└── README.md
```

## Building

Run the packer from the `simple_plugin` directory:

```bash
pypacker 3.5 output.pyp my_product myplugin .
```

This will create `output.pyp` containing all modules bundled together.

## Testing

You can test the packed output:

```bash
python output.pyp
```

You should see:
```
Simple Plugin v1.0
Core function executed!
Helper function result: HELLO FROM HELPER
```
