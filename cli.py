import logging
import os
import sys
from typing import Annotated

import typer

from parser import LogFormatError, parse_line
from stats import Report

logger = logging.getLogger("logtool")


def main(
    logfile: Annotated[str, typer.Argument(help="Path to the log file")],
    top: Annotated[int, typer.Option(help="Number of top IPs to display")] = 3,
) -> None:

    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "WARNING").upper(),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logpath = logfile

    try:
        stats, badline = analyse_file(logpath)
    except OSError as e:
        logger.error("Error processing log file: %s - %s", logpath, e)
        sys.exit(1)

    print_report(stats, badline, top)


def analyse_file(logpath: str) -> tuple[Report, int]:
    stats = Report()
    badline = 0


    with open(logpath, encoding="utf-8", errors="replace") as f:
        logger.info("Processing log file: %s", logpath)
        for linenumber, line in enumerate(f, start=1):
            try:
                entry = parse_line(line)
            except LogFormatError as e:
                badline += 1
                logger.error(
                    "Error parsing line %d : %r - %s", linenumber, line.rstrip(), e
                )
                continue
            logger.debug("Parsed line %d: %s", linenumber, entry)
            stats.add(entry)
    return stats, badline


def print_report(stats: Report, badline: int, top: int) -> None:
    print(f"Total errors: {stats.errors}")
    print(f"Total bad lines: {badline}")
    print()
    print(f"Top {top} IPs:")
    for ip, requests in stats.ip_counts.most_common(top):
        print(f"  {ip}: {requests}")
    print()
    print("Requests per stream:")
    for stream, requests in stats.stream_counts.most_common():
        print(f"  {stream}: {requests}")
    print()
    print(f"Different IPs on setvlive: {len(stats.setvlive_ips)}")
    print()
    print("Last errors (oldest first):")
    for error in stats.last_errors:
        print(
            f"  {error.timestamp}  {error.ip}  {error.status}  {error.app}  {error.stream}  {error.event}"
        )
    print()
    print("Streams per app:")
    for app, streams in stats.streams_by_app.items():
        print(f"  {app}:")
        for stream, requests in streams.items():
            print(f"    {stream}: {requests}")


if __name__ == "__main__":
    typer.run(main)
