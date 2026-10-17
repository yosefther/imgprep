import pytest

from imgprep import main


def test_main_runs(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    assert "imgprep" in capsys.readouterr().out
