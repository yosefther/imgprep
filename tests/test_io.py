"""Tests for io: image discovery, class detection, and corrupted-file handling."""

from pathlib import Path

import pytest

from imgprep.io import UNLABELED, class_of, find_images, scan_dataset


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


def test_class_of_uses_folder_name(tmp_path: Path) -> None:
    assert class_of(tmp_path / "cats" / "x.jpg", tmp_path) == "cats"


def test_class_of_image_in_root_is_unlabeled(tmp_path: Path) -> None:
    assert class_of(tmp_path / "x.jpg", tmp_path) == UNLABELED


def test_class_of_nested_uses_top_folder(tmp_path: Path) -> None:
    assert class_of(tmp_path / "cats" / "indoor" / "x.jpg", tmp_path) == "cats"


def test_scan_dataset_sorts_valid_and_corrupt(sample_dataset: Path) -> None:
    result = scan_dataset(sample_dataset)
    valid = [(p.relative_to(sample_dataset).as_posix(), cls) for p, cls in result.valid]
    corrupt = [p.relative_to(sample_dataset).as_posix() for p, _ in result.corrupt]
    assert valid == [
        ("cats/cat1.jpg", "cats"),
        ("cats/cat2.PNG", "cats"),
        ("dogs/dog1.jpg", "dogs"),
    ]
    assert corrupt == ["dogs/fake.jpg", "dogs/truncated.jpg"]


def test_scan_dataset_gives_reason_for_corrupt(sample_dataset: Path) -> None:
    for _, reason in scan_dataset(sample_dataset).corrupt:
        assert reason
