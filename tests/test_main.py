import pytest

from main import main


def test_main_prints_hello(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that main() prints the expected greeting."""
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello from mfsignal!\n"
