"""Dataset health stats.

Per-class counts, imbalance warnings, resolution/format distribution, corrupted files.
"""

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from imgprep.io import ScanResult, scan_dataset


@dataclass
class DatasetStats:
    class_counts: dict[str, int] = field(default_factory=dict)  # class name -> count
    corrupted: list[tuple[Path, str]] = field(default_factory=list)  # path ,reason
    resolutions: Counter[tuple[int, int]] = field(default_factory=Counter)


def compute_stats(root: Path) -> DatasetStats:
    """Scan root once and collect class counts, corrupt files and resolutions"""
    result = scan_dataset(root)
    resolutions: Counter[tuple[int, int]] = Counter()
    for path, _ in result.valid:
        with Image.open(path) as img:
            resolutions[img.size] += 1

    return DatasetStats(
        class_counts=class_counts(result),
        corrupted=result.corrupt,
        resolutions=resolutions,
    )


def class_counts(result: ScanResult) -> Counter[str]:
    """Count valid images per class."""
    return Counter(cls for _, cls in result.valid)
