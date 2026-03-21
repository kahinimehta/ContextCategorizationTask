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
- **`phase2_trial_order.csv`** — Fixed trial order for Phase 2 (same for all participants)

### Documentation

- **`csv_documentation.md`** — CSV columns and complete TTL trigger mapping
- **`script.md`** — Experimenter script: on-screen text, phase-by-phase flow, TTL summary, ELI5 tips
- **`STIMULI/tutorial_video_spec.md`** — Production spec for tutorial video (content, timing, subtitles)
- **`STIMULI/shape_generation.md`** — Shape creation pipeline (Henderson bunny anchor → OpenAI anchors → morphing script)

### Stimuli

- **`STIMULI/Shapes/`** — 16 shape PNGs (Shape_0_0.png … Shape_3_3.png) + ShapeGrid_4x4.png, ShapeGrid_4x4_scrambled.png. Phase 1 shows the **scrambled** grid (5 s), then shapes one-by-one in random order. Phase 3: same task, no grid preview, different random order. See `STIMULI/shape_generation.md`.
- **`STIMULI/Context_Images/`** — Flat folder of context PNGs named by category and variant: `{category}1.png`/`{category}2.png` or `{category}_1.png`/`{category}_2.png` (e.g., bedroom1.png, bedroom2.png; bookstore_1.png, bookstore_2.png). The number denotes the variation (1 = original, 2 = control). Practice images: practice1.png, practice2.png.
- **`STIMULI/tutorial_video.mp4`** — Optional. Video showing the click-to-place process (red square, red circle, green circle). See `STIMULI/tutorial_video_spec.md` for production spec (content, timing, subtitles). If missing, an animated fallback simulates the sequence.


## Data Output

All CSV data is written incrementally to `../LOG_FILES/` (relative to the task root). Participant name is appended to all filenames.

| File | Description |
|------|-------------|
| `phase1_{participant}_{datetime}.csv` | Per-shape: final (x,y), RT (to last click), all_click_ttl, submit_ttl |
| `phase1_placements_{participant}_{datetime}.png` | Image of shape placements (saved incrementally after each shape) |
| `phase2_{participant}_{datetime}.csv` | Per-trial: shape, 2 contexts, variant, response, RT, TTL timestamps (order from phase2_trial_order.csv) |
| `phase3_{participant}_{datetime}.csv` | Same structure as phase1 |
| `phase3_placements_{participant}_{datetime}.png` | Image of shape placements (saved incrementally after each shape) |
| `debrief_{participant}_{datetime}.csv` | Post–Phase 3: 3 Yes/No questions, answers, RT, onset/response TTL |
| `summary_{participant}_{datetime}.csv` | Total task time, grid dimensions, ground-truth positions, Euclidean distances (how close shapes are categorically) |
| `ttl_log_{participant}_{datetime}.csv` | Every TTL trigger: timestamp, trigger code, event label, trial info |

*datetime* = `YYYYMMDD_HHMMSS`. **No files** if name contains "test".


### Demonstration of task 

**`demo.mp4`** — Demonstration of task. 

Example output files in the task root illustrate the expected format:

| File | Description |
|------|-------------|
| `phase1_kahini_20260320_175811.csv` | Phase 1 output: one row per shape with `shape_path` (full path), `final_x`, `final_y`, `rt`, `click_ttl`, `submit_ttl`, etc. |
| `phase2_kahini_20260320_175811.csv` | Phase 2 output: one row per trial with `shape_path`, `context_1_path`, `context_2_path`, `trial_variant`, `response`, `rt`, and TTL timestamps. |
| `ttl_log_20260320_175811.csv` | TTL log: every event with `timestamp`, `trigger_code`, `event_label`, `trial_info`. Use for EEG/fMRI alignment. |


See `csv_documentation.md` for full column definitions and TTL trigger mapping.

## TTL Triggers

TTL via Blackrock parallel port or Cedrus pyxid2. Every screen change and response is logged (onset/offset for instructions, stimulus/click/submit for tasks, phase completion markers, debrief onset/response/offset, escape_pressed on quit). See `csv_documentation.md` for full mapping.

## Quick Start

1. Ensure PsychoPy and dependencies are installed (Anaconda environment)
2. Run: `python context_shape_task.py`
3. Enter participant name on fullscreen (like Social Recognition Task); press Enter when done
4. **ESC** exits during interactive screens (instructions, name entry, shape placement, etc.). Not during timed displays (grid, fixation). Like Social Recognition Task, no global escape—reduces accidental quits.
5. Optional: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise a timed fallback plays
6. For practice runs: use a name containing "test" to skip all file saving

**Experimenters:** See `script.md` for run-through.

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
