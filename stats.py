from collections import Counter, deque

from parser import LogEntry


class Report:
    def __init__(self) -> None:
        self.errors = 0
        self.ip_counts: Counter[str] = Counter()
        self.stream_counts: Counter[str] = Counter()
        self.setvlive_ips: set[str] = set()
        self.last_errors: deque[LogEntry] = deque(maxlen=10)
        self.streams_by_app: dict[str, Counter[str]] = {}

    def add(self, entry: LogEntry) -> None:
        self.ip_counts[entry.ip] += 1
        self.stream_counts[entry.stream] += 1

        if entry.stream == "setvlive":
            self.setvlive_ips.add(entry.ip)

        if entry.status >= 400:
            self.errors += 1
            self.last_errors.append(entry)

        if entry.app not in self.streams_by_app:
            self.streams_by_app[entry.app] = Counter()
        self.streams_by_app[entry.app][entry.stream] += 1
