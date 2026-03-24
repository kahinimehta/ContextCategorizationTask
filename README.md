# Context Shape Task

This repository contains the PsychoPy implementation of the **ContextShape Task**, a multi-phase experiment examining bottom-up shape classification and top-down context incorporation.

## Acknowledgments

- **Shape generation**: Bunny anchor from Henderson et al. 2025; OpenAI used to create duck, bird, and squirrel anchors; contour interpolation (OpenCV, scipy) to morph the four anchors into a 4×4 grid. See `STIMULI/shape_generation.md` for the full pipeline and morphing script.
- **Context images**: OpenAI
- **Practice stimulus generation**: OpenAI
- **Coding**: Cursor & Claude

## Environment

- **Python**: Anaconda
- **PsychoPy**: v2025.1.1
- **Display**: Fullscreen by default (windowed via `PSYCHOPY_WINDOWED=1` if needed)
- **Exit**: ESC during interactive screens only (no global escape; like Social Recognition Task)

## Repository Contents

### Core Task

- **`context_shape_task.py`** — Main PsychoPy script for the entire experiment
- **`phase2_trial_order.csv`** — Phase 2 trial template: **64** trials (one row per trial after the header). Columns: `trial_number`, `shape`, `shape_path`, `strong_context`, `neutral_context`, `context1`, `context1_image`, `context2`, `context2_image`, `variant`. Image paths may be absolute or relative to `STIMULI/`. Same row order for every participant; logged `phase2_*.csv` matches this order (`trial` 1…64). Details: **TASK_DESCRIPTION.md** (Phase 2 trial template).

### Task design (summary)

- **Phase 1:** 16 shapes, random order (with `Shape_0_0` not first), click-to-place after grid preview.
- **Phase 2:** **64** context trials in **fixed** order from `phase2_trial_order.csv` (no randomization).
- **Phase 3:** Same 16 shapes as Phase 1, new random order (must differ from Phase 1).

### Documentation

| File | Purpose |
|------|---------|
| **`script.md`** | Experimenter script: on-screen text, phase-by-phase flow, TTL summary, ELI5 tips |
| **`TASK_DESCRIPTION.md`** | Technical spec: timing, trial selection, Phase 2 template CSV, troubleshooting |
| **`csv_documentation.md`** | CSV columns and complete TTL trigger mapping |
| **`STIMULI/shape_generation.md`** | Shape creation pipeline (morphing, anchors) |

### Stimuli

- **`STIMULI/Shapes/`** — 16 shape PNGs (Shape_0_0.png … Shape_3_3.png) + ShapeGrid_4x4.png, ShapeGrid_4x4_scrambled.png. Phase 1 and Phase 3 each show the **scrambled** grid (5 s), then shapes one-by-one in random order (Phase 3 uses a different order than Phase 1). See `STIMULI/shape_generation.md`.
- **`STIMULI/Context_Images/`** — Flat folder of context PNGs named by category and variant: `{category}1.png`/`{category}2.png` or `{category}_1.png`/`{category}_2.png` (e.g., bedroom1.png, bedroom2.png; bookstore_1.png, bookstore_2.png). The number denotes the variation (1 = original, 2 = control). Practice images: practice1.png, practice2.png.


## Data Output

All CSV data is written incrementally to `../LOG_FILES/` (relative to the task root). Participant name is appended to all filenames.

| File | Description |
|------|-------------|
| `phase1_{participant}_{datetime}.csv` | Per-shape: final (x,y), RT (to last click), click_ttl (last click), all_click_ttl, submit_ttl |
| `phase1_placements_{participant}_{datetime}.png` | Image of shape placements (saved incrementally after each shape) |
| `phase2_{participant}_{datetime}.csv` | **64** trials; order matches `phase2_trial_order.csv`. Per-trial: shape, contexts, variant, response, RT (TTL columns: csv_documentation.md) |
| `phase3_{participant}_{datetime}.csv` | Same structure as phase1 |
| `phase3_placements_{participant}_{datetime}.png` | Image of shape placements (saved incrementally after each shape) |
| `debrief_{participant}_{datetime}.csv` | Post–Phase 3: 3 Yes/No questions, answers, RT, onset/response TTL |
| `summary_{participant}_{datetime}.csv` | Total task time, grid dimensions, ground-truth positions, Euclidean distances (how close shapes are categorically) |
| `ttl_log_{participant}_{datetime}.csv` | Every TTL trigger: timestamp, trigger code, event label, trial info |

*datetime* = `YYYYMMDD_HHMMSS`. **No files** if name contains "test".

**Only `ttl_log` has real timing data; the other CSVs keep timing column headers empty on purpose so files stay small and merge cleanly.** 

### Example output

Example files in the task root show a full non-test run (participant `kini`, timestamp `20260324_140014`):

| Files |
|-------|
| `phase1_kini_20260324_140014.csv`, `phase2_kini_20260324_140014.csv`, `phase3_kini_20260324_140014.csv` |
| `debrief_kini_20260324_140014.csv`, `summary_kini_20260324_140014.csv`, `ttl_log_kini_20260324_140014.csv` |
| `phase1_placements_kini_20260324_140014.png`, `phase3_placements_kini_20260324_140014.png` |

Live runs write the same filenames under `../LOG_FILES/`. **Columns and TTL:** `csv_documentation.md` (trigger codes, trial_info, which CSV fields are populated).

## Quick Start

1. Ensure PsychoPy and dependencies are installed (Anaconda environment)
2. Run: `python context_shape_task.py`
3. Enter participant name on fullscreen (like Social Recognition Task); press Enter when done
4. **ESC** exits during interactive screens (instructions, name entry, shape placement, etc.). Not during timed displays (grid, fixation). Like Social Recognition Task, no global escape—reduces accidental quits.
5. Optional: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise a timed fallback plays
6. For practice runs: use a name containing "test" to skip all file saving

**Experimenters:** See `script.md`. **Technical specs:** See `TASK_DESCRIPTION.md`.

## Troubleshooting

See **`TASK_DESCRIPTION.md`** for the full troubleshooting section (ESC behavior, OOM, dummy window, Mac TTL/ObjC/Enter issues).

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
