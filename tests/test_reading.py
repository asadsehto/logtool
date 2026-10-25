import pytest

from cli import analyse_file


def test_counts_good_and_bad_lines(tmp_path):
    log = tmp_path / "test.log"
    log.write_text(
        "2026-10-18T20:01:12Z 192.0.2.10 live setvlive play 200\n"
        "this line is broken\n"
        "2026-10-18T20:02:03Z 192.0.2.30 live sports play 404\n"
    )
    stats, badline = analyse_file(str(log))
    assert stats.errors == 1
    assert badline == 1


def test_empty_file(tmp_path):
    log = tmp_path / "empty.log"
    log.write_text("")
    stats, badline = analyse_file(str(log))
    assert stats.errors == 0
    assert badline == 0


def test_bad_byte_line_is_skipped(tmp_path):
    log = tmp_path / "bad_bytes.log"
    log.write_bytes(b"2026-10-18T20:03:30Z 192.0.2.40 live sp\xffrts play 500\n")
    stats, badline = analyse_file(str(log))
    assert stats.errors == 0
    assert badline == 1


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        analyse_file(str(tmp_path / "does_not_exist.log"))


def test_bad_line_is_logged(tmp_path, caplog):
    log = tmp_path / "test.log"
    log.write_text("2026-10-18T20:01:12Z 192.0.2.10 live setvlive play 200\nbroken\n")
    analyse_file(str(log))
    assert "Error parsing line 2" in caplog.text


def test_real_broken_log():
    stats, badline = analyse_file("data/broken.log")
    assert stats.errors == 2
    assert badline == 3