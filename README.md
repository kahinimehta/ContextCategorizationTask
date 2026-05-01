# Context Shape Task

This repository contains the PsychoPy implementation of the **ContextShape Task**, a multi-phase experiment examining bottom-up object grouping and top-down context incorporation.

## Acknowledgments

- **`Current task objects:** `.bmp` files in **`STIMULI/shapes/`** from the Droodles task (psycho applies **near-white → transparent:** **`OBJECT_WHITE_BG_STRIP_THRESHOLD`** in **`context_shape_task.py`**).
- **Contexts & tutorial practice stimuli:** OpenAI image generation
- **Coding**: Cursor & Claude

## Environment

- **Python**: Anaconda
- **PsychoPy**: **`requirements.txt`** pins **`psychopy>=2025.2,<2027`** (Anaconda builds often ship **2025.1.x**; either works with this script — same API surface used here)
- **Display**: Fullscreen by default (windowed via `PSYCHOPY_WINDOWED=1` if needed)
- **Exit**: ESC during interactive screens only (no global escape; like Social Recognition Task)

## Repository Contents

### Core Task

- **`context_shape_task.py`** — Main PsychoPy script for the entire experiment
- **`phase2_trial_order.csv`** — Defines Phase 2 (**shipped:** **64** rows; **`stderr`** logs **`N`** on load). Columns, **`PHASE2_CSV_REQUIRED`**, path quirks: **`TASK_DESCRIPTION.md`**.

### Task design (summary)

- **Phase 1:** 16 `.bmp` objects (from `STIMULI/shapes/`), random order (alphabetically first task stimulus not first), full-screen grid preview then click-to-sort with a **miniature 4×4 grid** fixed in the **bottom-right** for every trial (1 s isolate + placement).
- **Phase 2:** Trial order from **`phase2_trial_order.csv`**; breaks every **16** trials. Sequence: context → object → **`PHASE2_OBJECT_QUESTION_TEXT`** (default **"What is the object?"**, spoken response), twice per trial before the choice screen; TTL **`phase2_object_question_*`** / **`phase2_object_question2_*`**, **`phase2_*.csv`** **`object_question_onset_ttl`** / **`object_question2_onset_ttl`**. Context layout and timings: **`TASK_DESCRIPTION.md`**; verbatim instructions: **`script.md`** (Phase 2).
- **Phase 3:** Same 16 objects as Phase 1, new random order (must differ from Phase 1); same **bottom-right miniature grid** behavior as Phase 1.

### Documentation

| File | Role |
|------|------|
| **`script.md`** | Verbatim screens, run order |
| **`TASK_DESCRIPTION.md`** | Timings, stimuli, trial CSV spec, troubleshooting |
| **`csv_documentation.md`** | **`ttl_log_*`** triggers + behavioral CSV columns |

### Stimuli

- **`STIMULI/shapes/`** — 16 task `.bmp` + **`ShapeGrid_4x4_bmp.png`** (**layout / matte strip:** **`TASK_DESCRIPTION.md`**).
- **`STIMULI/contexts/`** — **`{category}1.png` / `{category}.png`**. Tutorial: **`practice1.png`**, **`practice2.png`** in **`STIMULI/`** or **`contexts/`**.


## Data Output

Session outputs (CSV, placement PNGs, TTL log) are written incrementally to **`../LOG_FILES/`** (relative to the task folder). Filenames include **`{participant}`** and **`{YYYYMMDD_HHMMSS}`** (session start timestamp).

| File pattern | Description |
|------|-------------|
| `phase1_{participant}_{YYYYMMDD_HHMMSS}.csv`, `phase3_{participant}_{YYYYMMDD_HHMMSS}.csv` | Per-shape placement (**columns:** **`csv_documentation.md`**) |
| `phase1_placements_{participant}_{YYYYMMDD_HHMMSS}.png`, `phase3_placements_{participant}_{YYYYMMDD_HHMMSS}.png` | Incremental placement PNGs (Phase 1 / 3) |
| `phase2_{participant}_{YYYYMMDD_HHMMSS}.csv` | One row per Phase 2 trial (+ onset TTL columns + **`response_ttl`**) |
| `debrief_{participant}_{YYYYMMDD_HHMMSS}.csv`, `summary_{participant}_{YYYYMMDD_HHMMSS}.csv` | Post–Phase 3 questionnaire + session summary |
| `ttl_log_{participant}_{YYYYMMDD_HHMMSS}.csv` | All TTL rows (starts as `ttl_log_{YYYYMMDD_HHMMSS}.csv`, **renamed** at session end—**`csv_documentation.md`**) |

**No saves** if participant name contains **`test`** (TTL scratch file is removed).


## Quick Start

1. PsychoPy (Anaconda) environment
2. `python context_shape_task.py` from the task folder
3. Participant name → Enter (**`test`** in name → no CSV/PNG saves; TTL log removed)
4. Optional: **`STIMULI/tutorial_video.mp4`** — else scripted fallback (spread overview; anchors beat **before** placement halo/click; isolate **without** expanding ring; triangle + **narrow tail**; **`script.md`** / **`TASK_DESCRIPTION.md`**)

## Troubleshooting

**`TASK_DESCRIPTION.md`** only (ESC timing, **`PSYCHOPY_WINDOWED`**, **`PSYCHOPY_DUMMY_WINDOW`**, **`PSYCHOPY_CHECK_TIMING`**, macOS quirks).

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
