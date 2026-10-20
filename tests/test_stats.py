"""Tests for stats: class counts, imbalance detection, and resolution/format summaries."""

from pathlib import Path

from imgprep.io import scan_dataset
from imgprep.stats import class_counts


def test_class_counts_ignores_corrupt(sample_dataset: Path) -> None:
    assert class_counts(scan_dataset(sample_dataset)) == {"cats": 2, "dogs": 1}
