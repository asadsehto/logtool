class LogFormatError(Exception):
    pass

def parse_line(line):
    if "\ufffd" in line:
        raise LogFormatError("contains characters that are not valid UTF-8")
    fields = line.split()
    if len(fields) != 6:
        raise LogFormatError(f"expected 6 fields, got {len(fields)}")
    timestamp, ip, app, stream, event, status = fields
    if not status.isdigit():
        raise LogFormatError(f"status is not a number: {status!r}")
    return {
        "timestamp": timestamp,
        "ip": ip,
        "app": app,
        "stream": stream,
        "event": event,
        "status": int(status),
    }

