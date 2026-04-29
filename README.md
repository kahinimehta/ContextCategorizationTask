# Context Shape Task

This repository contains the PsychoPy implementation of the **ContextShape Task**, a multi-phase experiment examining bottom-up object grouping and top-down context incorporation.

## Acknowledgments

- **`Current task objects:** `.bmp` files in **`STIMULI/shapes/`** (psycho applies **near-white → transparent:** **`OBJECT_WHITE_BG_STRIP_THRESHOLD`** in **`context_shape_task.py`**).
- **Contexts & tutorial practice stimuli:** OpenAI image generation
- **Coding**: Cursor & Claude

## Environment

- **Python**: Anaconda
- **PsychoPy**: v2025.1.1
- **Display**: Fullscreen by default (windowed via `PSYCHOPY_WINDOWED=1` if needed)
- **Exit**: ESC during interactive screens only (no global escape; like Social Recognition Task)

## Repository Contents

### Core Task

- **`context_shape_task.py`** — Main PsychoPy script for the entire experiment
- **`phase2_trial_order.csv`** — Defines Phase 2 (**shipped:** **64** rows; **`stderr`** logs **`N`** on load). Columns, **`PHASE2_CSV_REQUIRED`**, path quirks: **`TASK_DESCRIPTION.md`**.

### Task design (summary)

- **Phase 1:** 16 `.bmp` objects (from `STIMULI/shapes/`), random order (alphabetically first task stimulus not first), full-screen grid preview then click-to-sort with a **miniature 4×4 grid** fixed in the **bottom-right** for every trial (1 s isolate + placement).
- **Phase 2:** Trial order from **`phase2_trial_order.csv`**; breaks every **16** trials. Context layout (**center square**, cover crop): constants in **`context_shape_task.py`** — details **`TASK_DESCRIPTION.md`**.
- **Phase 3:** Same 16 objects as Phase 1, new random order (must differ from Phase 1); same **bottom-right miniature grid** behavior as Phase 1.

### Documentation

| File | Contents |
|------|----------|
| **`script.md`** | Verbatim screens, run order, example TTL names |
| **`TASK_DESCRIPTION.md`** | Timing constants (`*_SEC`), stimuli paths, **Phase 2 context framing**, **`phase2_trial_order.csv`** spec, troubleshooting |
| **`csv_documentation.md`** | Full **`ttl_log_*`** trigger table (includes **legacy** rows for old instruction screens) plus **`*.csv`** column definitions |

### Stimuli

- **`STIMULI/shapes/`** — 16 task `.bmp` files plus `ShapeGrid_4x4_bmp.png` composite (ordering: **`TASK_DESCRIPTION.md`**). Task `.bmp` files are shown with **white matte stripped at load** (see **`OBJECT_WHITE_BG_STRIP_THRESHOLD`**). Rebuild composite: **`python scripts/generate_shape_grid.py`** (needs **Pillow**) if you change which assets are in the grid.
- **`STIMULI/contexts/`** — Category pairs `{category}1.png` / `{category}.png`. Tutorial practice assets: **`practice1.png`**, **`practice2.png`** (**space** / **circus**) in **`STIMULI/`** or **`contexts/`**.


## Data Output

All CSV data is written incrementally to `../LOG_FILES/` (relative to the task root). Participant name is appended to all filenames.

| File | Description |
|------|-------------|
| `phase1_*.csv`, `phase1_placements_*.png` | Per-shape placement + incremental PNG (**columns:** **`csv_documentation.md`**) |
| `phase2_*.csv` | One row per trial (includes onset TTL copies + **`response_ttl`**) |
| `phase3_*.csv`, `phase3_placements_*.png` | Same role as Phase 1 |
| `debrief_*.csv`, `summary_*.csv`, `ttl_log_*.csv` | Debrief, session summary, all TTL events (**schema:** **`csv_documentation.md`**) |

*datetime* = `YYYYMMDD_HHMMSS` in filenames. **No output files** if participant name contains **`test`**.

### Example output

Example files in the task root show a full non-test run (participant `kini`, timestamp `20260324_140014`):

| Files |
|-------|
| `phase1_kini_20260324_140014.csv`, `phase2_kini_20260324_140014.csv`, `phase3_kini_20260324_140014.csv` |
| `debrief_kini_20260324_140014.csv`, `summary_kini_20260324_140014.csv`, `ttl_log_kini_20260324_140014.csv` |
| `phase1_placements_kini_20260324_140014.png`, `phase3_placements_kini_20260324_140014.png` |

Live runs write the same filenames under `../LOG_FILES/`.

## Quick Start

1. PsychoPy (Anaconda) environment
2. `python context_shape_task.py` from the task folder
3. Participant name → Enter (**`test`** in name → no CSV/PNG saves; TTL log removed)
4. Optional: **`STIMULI/tutorial_video.mp4`** — else scripted fallback (color-sort demo; subtitles match **`script.md`** / timing **`TASK_DESCRIPTION.md`**)

## Troubleshooting

**`TASK_DESCRIPTION.md`** only (ESC timing, **`PSYCHOPY_WINDOWED`**, **`PSYCHOPY_DUMMY_WINDOW`**, **`PSYCHOPY_CHECK_TIMING`**, macOS quirks).

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
