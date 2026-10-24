from collections import Counter, deque


def new_stats():
    return {
        "errors": 0,
        "ip_counts": Counter(),
        "stream_counts": Counter(),
        "setvlive_ips": set(),
        "last_errors": deque(maxlen=10),
        "streams_by_app": {},
    }


def add_entry(stats, entry):
    stats["ip_counts"][entry.ip] += 1
    stats["stream_counts"][entry.stream] += 1

    if entry.stream == "setvlive":
        stats["setvlive_ips"].add(entry.ip)

    if entry.status >= 400:
        stats["errors"] += 1
        stats["last_errors"].append(entry)

    if entry.app not in stats["streams_by_app"]:
        stats["streams_by_app"][entry.app] = Counter()
    stats["streams_by_app"][entry.app][entry.stream] += 1