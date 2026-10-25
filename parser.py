class LogFormatError(Exception):
    pass

from dataclasses import dataclass

@dataclass
class LogEntry:
    timestamp: str
    ip: str
    app: str
    stream: str
    event: str
    status: int

def parse_line(line: str) -> LogEntry:
    if "\ufffd" in line:
        raise LogFormatError("contains characters that are not valid UTF-8")
    fields = line.split()
    if len(fields) != 6:
        raise LogFormatError(f"expected 6 fields, got {len(fields)}")
    timestamp, ip, app, stream, event, status = fields
    if not status.isdigit():
        raise LogFormatError(f"status is not a number: {status!r}")
    return LogEntry(timestamp, ip, app, stream, event, int(status))