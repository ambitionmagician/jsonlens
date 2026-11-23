#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Union

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="JSON Lens: A command-line tool for inspecting and manipulating JSON data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsonlens.py data.json                    Pretty-print JSON
  jsonlens.py data.json --validate         Validate JSON
  jsonlens.py data.json --get user.name    Extract nested value
  jsonlens.py data.json --keys             List top-level keys
  jsonlens.py data.json --flatten          Flatten to dotted paths
  jsonlens.py - < data.json                Read from stdin
"""
    )
    parser.add_argument(
        "input",
        help="Input JSON file path, or '-' for stdin"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Number of spaces for indentation (default: 2, use 0 for compact)"
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort object keys in output"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate JSON and exit with status 0 if valid, 1 if invalid"
    )
    parser.add_argument(
        "--get",
        metavar="PATH",
        help="Extract value at dotted path (e.g., 'a.b.0.c')"
    )
    parser.add_argument(
        "--keys",
        action="store_true",
        help="List top-level keys, or keys at --get path if combined"
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Output flat dotted-path -> value lines for scalar leaves"
    )
    return parser.parse_args()

def read_json(input_path: str) -> Any:
    try:
        if input_path == "-":
            data = sys.stdin.read()
        else:
            with open(input_path, "r") as f:
                data = f.read()
        return json.loads(data)
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def get_nested_value(data: Any, path: str) -> Any:
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict):
            if key not in current:
                print(f"Error: Key '{key}' not found", file=sys.stderr)
                sys.exit(1)
            current = current[key]
        elif isinstance(current, list):
            try:
                idx = int(key)
                if idx < 0 or idx >= len(current):
                    print(f"Error: Index {idx} out of range", file=sys.stderr)
                    sys.exit(1)
                current = current[idx]
            except ValueError:
                print(f"Error: Invalid list index '{key}'", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: Cannot traverse non-container at '{key}'", file=sys.stderr)
            sys.exit(1)
    return current

def list_keys(data: Any, path: Optional[str] = None) -> List[str]:
    if path:
        data = get_nested_value(data, path)
    if isinstance(data, dict):
        return list(data.keys())
    elif isinstance(data, list):
        return [str(i) for i in range(len(data))]
    else:
        return []

def flatten_json(data: Any, prefix: str = "") -> List[tuple]:
    items = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            items.extend(flatten_json(value, new_prefix))
    elif isinstance(data, list):
        for idx, value in enumerate(data):
            new_prefix = f"{prefix}.{idx}" if prefix else str(idx)
            items.extend(flatten_json(value, new_prefix))
    else:
        items.append((prefix, data))
    return items

def main():
    args = parse_args()
    
    # --get and --keys may be combined (keys at the --get path); every
    # other mode is exclusive.
    mode_count = sum([
        args.validate,
        bool(args.get) or args.keys,
        args.flatten
    ])
    
    if mode_count > 1:
        print("Error: Only one mode can be used at a time", file=sys.stderr)
        sys.exit(1)
    
    data = read_json(args.input)
    
    if args.validate:
        print("Valid JSON", file=sys.stderr)
        sys.exit(0)
    
    if args.keys:
        keys = list_keys(data, args.get)
        for key in keys:
            print(key)
        sys.exit(0)

    if args.get:
        value = get_nested_value(data, args.get)
        print(json.dumps(value, indent=args.indent if args.indent else None, sort_keys=args.sort_keys))
        sys.exit(0)
    
    if args.flatten:
        items = flatten_json(data)
        for path, value in items:
            print(f"{path}\t{json.dumps(value)}")
        sys.exit(0)
    
    # Default: pretty-print
    print(json.dumps(data, indent=args.indent, sort_keys=args.sort_keys))

if __name__ == "__main__":
    main()
