from collections import Counter, deque
from parser import parse_line , LogFormatError
from typing import Annotated
import typer
from stats import Report
import argparse
import logging
import sys
import os

logger = logging.getLogger("logtool")

def main(
            logfile: Annotated[str, typer.Argument(help="Path to the log file")],
            top: Annotated[int, typer.Option(help="Number of top IPs to display")] = 3
)-> None:
    

    
    logging.basicConfig(level = os.environ.get("LOGLEVEL", "WARNING").upper(),
                    format = "%(asctime)s - %(levelname)s - %(message)s")

   
    logpath = logfile
    stats = Report()
    badline = 0
    
    try:
        f = open(logpath, encoding="utf-8", errors="replace")
    except FileNotFoundError as e:
        logger.error("Error opening log file: %s - %s", logpath, e)
        sys.exit(1)
    logger.info("Processing log file: %s", logpath)
    with f:
         for linenumber, line in enumerate(f, start=1):
            try:
                entry = parse_line(line)
            except LogFormatError as e:
                badline += 1
                logger.error("Error parsing line %d : %r - %s", linenumber, line.rstrip(), e)
                continue
            logger.debug("Parsed line %d: %s", linenumber, entry)
            stats.add(entry)

    print_reporrt(stats, badline, top)


def print_reporrt(stats: Report, badline: int, top: int) -> None:
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
        print(f"  {error.timestamp}  {error.ip}  {error.status}  {error.app}  {error.stream}  {error.event}")
    print()
    print("Streams per app:")
    for app, streams in stats.streams_by_app.items():
        print(f"  {app}:")
        for stream, requests in streams.items():
            print(f"    {stream}: {requests}")
    

if __name__ == "__main__":
    
  typer.run(main)