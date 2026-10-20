"""Tests for io: image discovery, class detection, and corrupted-file handling."""

from pathlib import Path

import pytest

from imgprep.io import find_images


def test_find_images_returns_sorted_images(sample_dataset: Path) -> None:
    found = [p.relative_to(sample_dataset).as_posix() for p in find_images(sample_dataset)]
    assert found == [
        "cats/cat1.jpg",
        "cats/cat2.PNG",
        "dogs/dog1.jpg",
        "dogs/fake.jpg",
        "dogs/truncated.jpg",
    ]


def test_find_images_skips_junk(sample_dataset: Path) -> None:
    names = {p.name for p in find_images(sample_dataset)}
    assert ".DS_Store" not in names
    assert "._cat1.jpg" not in names
    assert "notes.txt" not in names


def test_find_images_missing_folder_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        find_images(tmp_path / "nope")


def test_find_images_file_instead_of_folder_raises(sample_dataset: Path) -> None:
    with pytest.raises(NotADirectoryError):
        find_images(sample_dataset / "notes.txt")


def test_find_images_empty_folder(tmp_path: Path) -> None:
    assert find_images(tmp_path) == []
