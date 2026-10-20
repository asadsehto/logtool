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
ip_counts = {}

with open("data/sample.log") as f:
    for line in f:
        entry = parse_line(line)

        # result 1: errors
        if entry["status"] >= 400:
            errors += 1
            print(f"IP: {entry['ip']}, Code: {entry['status']}")

        # result 2: requests per IP
        if entry["ip"] not in ip_counts:
            ip_counts[entry["ip"]] = 1
        else:
            ip_counts[entry["ip"]] += 1

print(f"Total errors: {errors}")
print()
print("Requests per IP:")
for ip, requests in ip_counts.items():
    print(f"  {ip}: {requests}")