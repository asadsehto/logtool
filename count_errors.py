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
with open("data/sample.log") as f:
    for line in f:
        entry = parse_line(line)
        if entry["status"] >= 400:
            errors += 1
            print(f"IP: {entry['ip']}, Code: {entry['status']}")
print(f"Total errors: {errors}")
