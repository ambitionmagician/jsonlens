# JsonLens

by Dr. Brent Allen Jensen

Inspect and pick apart JSON from the command line — pretty-print it,
validate it, pull one value out by path, list keys, or flatten the
whole document into dotted-path lines you can grep.

## Quickstart

```bash
python3 jsonlens.py data.json                      # pretty-print
python3 jsonlens.py data.json --sort-keys --indent 4
python3 jsonlens.py data.json --validate           # exit 0/1
python3 jsonlens.py data.json --get user.name
python3 jsonlens.py data.json --get items.0.price
python3 jsonlens.py data.json --keys               # top-level keys
python3 jsonlens.py data.json --get user --keys    # keys under a path
python3 jsonlens.py data.json --flatten            # path <TAB> value lines
cat data.json | python3 jsonlens.py - --get version
```

Paths are dotted; numeric segments index into arrays (`a.b.0.c`).
Modes are exclusive, except `--get` and `--keys`, which combine.

## Requirements

- Python 3.10+, standard library only

## Notes

- Invalid JSON is reported with the parser's position message and a
  nonzero exit code — useful in shell scripts and CI.
- `--flatten` emits scalar leaves only; empty objects and arrays
  produce no lines.

## Support this work

If this tool saved you time or taught you something, donations keep the work going:

- BTC: 15McijPo79Zx58NGyEf2PvaPtGqGmpztWn
- ETH: 0x8C25164E9234E6A30b8E44485B79c5cE8419cF2B

## License

MIT — see [LICENSE](LICENSE).
