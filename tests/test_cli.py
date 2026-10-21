"""Tests for the CLI: commands run end to end and print the expected output."""

from pathlib import Path

from typer.testing import CliRunner

from imgprep.cli import app

runner = CliRunner()


def test_stats_prints_class_counts(sample_dataset: Path) -> None:
    result = runner.invoke(app, ["stats", str(sample_dataset)])
    assert result.exit_code == 0
    assert "cats: 2" in result.output
    assert "dogs: 1" in result.output
    assert "total: 3 valid, 2 corrupt" in result.output


def test_stats_lists_corrupt_files(sample_dataset: Path) -> None:
    result = runner.invoke(app, ["stats", str(sample_dataset)])
    assert "corrupt: dogs/fake.jpg" in result.output
    assert "corrupt: dogs/truncated.jpg" in result.output


def test_stats_missing_folder_fails(tmp_path: Path) -> None:
    result = runner.invoke(app, ["stats", str(tmp_path / "nope")])
    assert result.exit_code != 0


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "imgprep" in result.output
