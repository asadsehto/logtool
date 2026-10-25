import ipaddress
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError, field_validator


class LogFormatError(Exception):
    pass


class LogEntry(BaseModel):
    timestamp: datetime
    ip: str
    app: str
    stream: str
    event: str
    status: int = Field(ge=100, le=599)

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        ipaddress.ip_address(v)
        return v


def parse_line(line: str) -> LogEntry:
    if "\ufffd" in line:
        raise LogFormatError("contains characters that are not valid UTF-8")
    fields = line.split()
    if len(fields) != 6:
        raise LogFormatError(f"expected 6 fields, got {len(fields)}")
    timestamp, ip, app, stream, event, status = fields
    try:
        return LogEntry.model_validate(
            {
                "timestamp": timestamp,
                "ip": ip,
                "app": app,
                "stream": stream,
                "event": event,
                "status": status,
            }
        )
    except ValidationError as e:
        problems = "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in e.errors())
        raise LogFormatError(problems) from e
