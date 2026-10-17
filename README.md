# imgprep

[![CI](https://github.com/yosefther/imgprep/actions/workflows/ci.yml/badge.svg)](https://github.com/yosefther/imgprep/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**A fast command-line toolkit for cleaning and preparing image datasets before training computer vision models.**

imgprep finds duplicate and near-duplicate images, splits datasets into stratified train/val/test sets, and reports dataset health issues like class imbalance and corrupted files.

---

## Why

Real-world image datasets are messy, and the mess silently damages models:

- **Duplicates cause data leakage.** When copies of the same image (resized, recompressed, or slightly cropped) end up in both training and test sets, the model has effectively seen the test data, and reported accuracy is inflated.
- **Careless splits distort evaluation.** A random split can leave rare classes missing from the validation or test set entirely.
- **Hidden problems crash training.** Corrupted files and extreme class imbalance are better found before a long training run than halfway through it.

imgprep handles all three with one command each.

---

## Features

- `dedup`: detects exact and near-duplicate images using perceptual hashing, with a BK-tree index for sub-quadratic search
- `split`: stratified train/val/test splitting with reproducible seeds
- `stats`: per-class counts, imbalance warnings, resolution and format distribution, corrupted-file detection
- Rich terminal output and machine-readable JSON reports
- Fully typed, tested, and checked in CI

---

## Installation

Requires Python 3.12+.

```bash
git clone https://github.com/yosefther/imgprep.git
cd imgprep
uv sync          # or: pip install -e .
```

---

## Usage

imgprep expects a class-per-folder dataset:

```
dataset/
├── cats/
├── dogs/
└── rabbits/
```

### Inspect a dataset

```bash
imgprep stats ./dataset
```

```
Class        Images   Share
cats          1,204   48.2%
dogs          1,150   46.0%
rabbits         145    5.8%   ⚠ underrepresented
Corrupted files: 3
Resolutions: 640x480 (61%), 1024x768 (22%), other (17%)
```

### Find duplicates

```bash
imgprep dedup ./dataset --threshold 5
imgprep dedup ./dataset --threshold 5 --move ./duplicates --report dupes.json
```

| Option | Description | Default |
| --- | --- | --- |
| `--threshold` | Max Hamming distance to count as a duplicate (0 = exact match) | `5` |
| `--hash` | Hash algorithm: `phash`, `dhash`, `ahash` | `phash` |
| `--move` | Move duplicates (keeping one per group) into this folder | off |
| `--report` | Write duplicate groups to a JSON file | off |

### Split a dataset

```bash
imgprep split ./dataset --out ./splits --ratios 0.7 0.15 0.15 --seed 42
```

Produces `splits/train/`, `splits/val/`, and `splits/test/`, each preserving the original class proportions. The same seed always produces the same split. Use `--dry-run` to preview without copying files.

---

## How it works

### Perceptual hashing

Pixel-by-pixel comparison fails for near-duplicates, since a resized or recompressed copy has entirely different pixel values. imgprep instead computes a 64-bit perceptual hash for each image: the image is shrunk to a tiny grayscale version, and each bit encodes its brightness structure. Visually similar images produce nearly identical hashes.

Two hashes are compared by **Hamming distance** (the number of differing bits). A distance of 0 indicates an exact or near-exact duplicate; small distances indicate edited copies.

### BK-tree search

Comparing every pair of images is O(n²): about 1.25 billion comparisons for 50,000 images. imgprep indexes hashes in a **BK-tree**, a metric tree that uses the triangle inequality to skip most comparisons when searching for all hashes within a distance threshold.

### Benchmark

<!-- Replace with your measured results -->

| Images | Naive pairwise | BK-tree | Speedup |
| --- | --- | --- | --- |
| 1,000 | _TBD_ s | _TBD_ s | _TBD_× |
| 10,000 | _TBD_ s | _TBD_ s | _TBD_× |
| 50,000 | _TBD_ s | _TBD_ s | _TBD_× |

_Measured on: CPU model, RAM, threshold = 5._

### Stratified splitting

Images are grouped by class, shuffled with a seeded random generator, and sliced per class according to the requested ratios, so every split keeps the dataset's class balance. Classes too small to populate every split produce a warning rather than a silent gap.

---

## Project structure

```
imgprep/
├── src/imgprep/
│   ├── cli.py       # Typer commands (thin layer, no logic)
│   ├── dedup.py     # hashing, BK-tree, duplicate grouping
│   ├── split.py     # stratified splitting
│   ├── stats.py     # dataset statistics
│   └── io.py        # image discovery and corrupt-file handling
└── tests/
```

---

## Development

```bash
uv sync --dev
uv run pytest            # tests
uv run ruff check .      # linting
uv run mypy src          # type checking
```

CI runs all three on every push via GitHub Actions.

---

## Design decisions

- **Logic separated from the CLI** so every function can be unit-tested directly.
- **BK-tree implemented from scratch** rather than using a library, to control performance and keep dependencies minimal.
- **Corrupted files are reported, not fatal**, so one bad file never stops a scan of a large dataset.
- **Deterministic by default**: seeded splits make experiments reproducible.

---

## Roadmap

- [ ] Parallel hashing with multiprocessing
- [ ] Support for YOLO and COCO annotation formats in `split`
- [ ] HTML report with duplicate thumbnails
- [ ] Publish to PyPI

---

## License

MIT