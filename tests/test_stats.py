"""Tests for stats: class counts, imbalance detection, and resolution/format summaries."""

from pathlib import Path

from PIL import Image

from imgprep.io import UNLABELED, scan_dataset
from imgprep.stats import class_counts, compute_stats


def test_class_counts_ignores_corrupt(sample_dataset: Path) -> None:
    assert class_counts(scan_dataset(sample_dataset)) == {"cats": 2, "dogs": 1}


def test_compute_stats_counts_classes(sample_dataset: Path) -> None:
    assert compute_stats(sample_dataset).class_counts == {"cats": 2, "dogs": 1}


def test_compute_stats_keeps_corrupt_with_reason(sample_dataset: Path) -> None:
    corrupted = compute_stats(sample_dataset).corrupted
    assert [p.relative_to(sample_dataset).as_posix() for p, _ in corrupted] == [
        "dogs/fake.jpg",
        "dogs/truncated.jpg",
    ]
    for _, reason in corrupted:
        assert reason


def test_compute_stats_counts_resolutions(sample_dataset: Path) -> None:
    assert compute_stats(sample_dataset).resolutions == {(32, 32): 3}


def test_compute_stats_mixed_resolutions(tmp_path: Path) -> None:
    (tmp_path / "cats").mkdir()
    Image.new("RGB", (32, 32)).save(tmp_path / "cats" / "a.jpg")
    Image.new("RGB", (32, 32)).save(tmp_path / "cats" / "b.jpg")
    Image.new("RGB", (64, 48)).save(tmp_path / "cats" / "c.jpg")
    assert compute_stats(tmp_path).resolutions == {(32, 32): 2, (64, 48): 1}


def test_compute_stats_empty_folder(tmp_path: Path) -> None:
    stats = compute_stats(tmp_path)
    assert stats.class_counts == {}
    assert stats.corrupted == []
    assert stats.resolutions == {}


def test_compute_stats_image_in_root_is_unlabeled(tmp_path: Path) -> None:
    Image.new("RGB", (32, 32)).save(tmp_path / "x.jpg")
    assert compute_stats(tmp_path).class_counts == {UNLABELED: 1}
