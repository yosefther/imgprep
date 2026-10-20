"""Dataset health stats.

Per-class counts, imbalance warnings, resolution/format distribution, corrupted files.
"""

from collections import Counter

from imgprep.io import ScanResult


def class_counts(result: ScanResult) -> Counter[str]:
    """Count valid images per class."""
    return Counter(cls for _, cls in result.valid)
