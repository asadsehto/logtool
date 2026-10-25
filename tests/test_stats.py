from parser import parse_line
from stats import Report


def test_new_report_is_empty():
    report = Report()
    assert report.errors == 0
    assert len(report.ip_counts) == 0


def test_404_counts_as_one_error():
    report = Report()
    report.add(parse_line("2026-10-18T20:02:03Z 192.0.2.30 live sports play 404\n"))
    assert report.errors == 1


def test_200_is_not_an_error():
    report = Report()
    report.add(parse_line("2026-10-18T20:01:12Z 192.0.2.10 live setvlive play 200\n"))
    assert report.errors == 0


def test_same_ip_on_setvlive_is_counted_once():
    report = Report()
    report.add(parse_line("2026-10-18T20:01:12Z 192.0.2.10 live setvlive play 200\n"))
    report.add(parse_line("2026-10-18T20:02:40Z 192.0.2.10 live setvlive stop 200\n"))
    assert report.ip_counts["192.0.2.10"] == 2
    assert len(report.setvlive_ips) == 1