from collections import Counter, deque


def parse_line(line):
    timestamp, ip, app, stream, event, status = line.split()
    return {
        "timestamp": timestamp,
        "ip": ip,
        "app": app,
        "stream": stream,
        "event": event,
        "status": int(status),
    }


errors = 0
ip_counts = Counter()
stream_counts = Counter()
setvlive_ips = set()
last_errors = deque(maxlen=10)
streams_by_app = {}

with open("data/sample.log") as f:
    for line in f:
        entry = parse_line(line)

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