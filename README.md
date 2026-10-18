
# logtool

A Python tool for analyzing streaming-server logs.

Current feature: counts error lines (HTTP status 4xx and 5xx) and prints the IP and status of each one.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Run

```bash
uv run python count_errors.py
```

## Sample data

`data/sample.log` is **synthetic** (made for testing). Format, one event per line:

```
<timestamp UTC> <ip> <app> <stream> <event> <status>
```
