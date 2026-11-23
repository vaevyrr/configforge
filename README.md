# ConfigForge

A command-line tool for checking and comparing JSON or YAML configuration files. It is aimed at small projects where a quick, readable validation report is more useful than a full schema platform.

## Features

- Validate JSON with line and column errors
- Validate YAML when PyYAML is installed
- Compare two files recursively and show added, removed and changed keys
- Optional required-key checks using dotted paths
- Exit codes suitable for CI scripts

## Install

Python 3.10+. JSON support uses only the standard library. For YAML:

```bash
python -m pip install PyYAML
```

## Examples

```bash
python configforge.py check config.json
python configforge.py check settings.yaml --require app.name --require database.host
python configforge.py diff config.example.json config.json
```

ConfigForge does not modify source files. Keep secrets out of committed configuration files.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT
