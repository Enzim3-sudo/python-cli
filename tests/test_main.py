import pytest
from python_cli import main


def test_default_greeting(capsys):
    main([])
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"


def test_long_name_option(capsys):
    main(["--name", "Alice"])
    captured = capsys.readouterr()
    assert captured.out == "Hello, Alice!\n"


def test_short_name_option(capsys):
    main(["-n", "Alice"])
    captured = capsys.readouterr()
    assert captured.out == "Hello, Alice!\n"


def test_empty_name(capsys):
    main(["--name", ""])
    captured = capsys.readouterr()
    assert captured.out == "Hello, !\n"


def test_unicode_name(capsys):
    main(["--name", "जयेश"])
    captured = capsys.readouterr()
    assert captured.out == "Hello, जयेश!\n"


def test_help_exits_successfully(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower()