import pytest

from parser import parse_line
from stats import Report


@pytest.fixture
def report():
    return Report()


def make_line(status):
    return f"2026-10-18T20:02:03Z 192.0.2.30 live sports play {status}\n"


def test_new_report_is_empty(report):
    assert report.errors == 0
    assert len(report.ip_counts) == 0


@pytest.mark.parametrize("status", [400, 401, 403, 404, 500, 503])
def test_4xx_and_5xx_are_errors(report, status):
    report.add(parse_line(make_line(status)))
    assert report.errors == 1


@pytest.mark.parametrize("status", [200, 204, 301, 399])
def test_below_400_is_not_an_error(report, status):
    report.add(parse_line(make_line(status)))
    assert report.errors == 0


def test_same_ip_on_setvlive_is_counted_once(report):
    report.add(parse_line("2026-10-18T20:01:12Z 192.0.2.10 live setvlive play 200\n"))
    report.add(parse_line("2026-10-18T20:02:40Z 192.0.2.10 live setvlive stop 200\n"))
    assert report.ip_counts["192.0.2.10"] == 2
    assert len(report.setvlive_ips) == 1