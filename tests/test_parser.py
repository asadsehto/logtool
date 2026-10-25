from parser import LogFormatError, parse_line, LogEntry
import pytest

def test_good_lines_become_logentry():
    entry = parse_line("2026-10-18T20:02:03Z 192.0.2.30 live sports play 404\n")
    assert entry.ip == "192.0.2.30"
    assert entry.stream == "sports"
    assert entry.status == 404


def test_missing_fields_raise_log_format_error():
    with pytest.raises(LogFormatError):
        parse_line("2026-10-18T20:02:03Z 192.0.2.30 live sports  404\n")


def test_status_that_is_not_a_number_is_rejected():
    with pytest.raises(LogFormatError):
        parse_line("2026-10-18T20:03:30Z 192.0.2.40 live sports play OK\n")


def test_empty_line_is_rejected():
    with pytest.raises(LogFormatError):
        parse_line("\n")


def test_bad_byte_is_rejected():
    with pytest.raises(LogFormatError):
        parse_line("2026-10-18T20:03:30Z 192.0.2.40 live sp\ufffdrts play 500\n")



@pytest.mark.parametrize("line", [
    "2026-10-18T20:02:03Z 192.0.2.30 live sports play 999\n",
    "2026-10-18T20:02:03Z 192.0.2.30 live sports play 99\n",
    "2026-10-18T20:02:03Z hello live sports play 404\n",
    "yesterday 192.0.2.30 live sports play 404\n",
])
def test_invalid_values_are_rejected(line):
    with pytest.raises(LogFormatError):
        parse_line(line)


def test_status_text_becomes_a_number():
    entry = parse_line("2026-10-18T20:02:03Z 192.0.2.30 live sports play 404\n")
    assert entry.status == 404
    assert isinstance(entry.status, int)