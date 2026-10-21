from collections import Counter, deque
import sys
import os
import logging
from parser import parse_line , LogFormatError

logger = logging.getLogger("logtool")

def main():
    logging.basicConfig(level = os.environ.get("LOGLEVEL", "WARNING").upper(),
                    format = "%(asctime)s - %(levelname)s - %(message)s")


    logpath = "data/sample.log"
    errors = 0
    ip_counts = Counter()
    stream_counts = Counter()
    setvlive_ips = set()
    last_errors = deque(maxlen=10)
    streams_by_app = {}
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
            ip_counts[entry["ip"]] += 1
            stream_counts[entry["stream"]] += 1
    
            if entry["stream"] == "setvlive":
                setvlive_ips.add(entry["ip"])
    
            if entry["status"] >= 400:
                errors += 1
                last_errors.append(entry)
    
            if entry["app"] not in streams_by_app:
                streams_by_app[entry["app"]] = Counter()
            streams_by_app[entry["app"]][entry["stream"]] += 1
    
    
    print(f"Total errors: {errors}")
    print(f"Total bad lines: {badline}")
    print()
    print("Top 3 IPs:")
    for ip, requests in ip_counts.most_common(3):
        print(f"  {ip}: {requests}")
    print()
    print("Requests per stream:")
    for stream, requests in stream_counts.most_common():
        print(f"  {stream}: {requests}")
    print()
    print(f"Different IPs on setvlive: {len(setvlive_ips)}")
    print()
    print("Last errors (oldest first):")
    for error in last_errors:
        print(f"  {error['timestamp']}  {error['ip']}  {error['status']}")
    print()
    print("Streams per app:")
    for app, streams in streams_by_app.items():
        print(f"  {app}:")
        for stream, requests in streams.items():
            print(f"    {stream}: {requests}")


if __name__ == "__main__":
    main()