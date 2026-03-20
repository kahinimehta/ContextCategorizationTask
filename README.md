# Context Shape Task

This repository contains the PsychoPy implementation of the **ContextShape Task**, a multi-phase experiment examining bottom-up shape classification and top-down context incorporation.

## Acknowledgments

- **Shape generation**: Bunny anchor from Henderson et al. 2025; OpenAI used to create duck, bird, and squirrel anchors; contour interpolation (OpenCV, scipy) to morph the four anchors into a 4×4 grid. See `STIMULI/shape_generation.md` for the full pipeline and morphing script.
- **Context images**: THINGS dataset
- **Practice stimulus generation**: OpenAI
- **Coding**: Cursor
- **Idea development**: Claude

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

## TTL Triggers

TTL via Blackrock parallel port or Cedrus pyxid2. Every screen change and response is logged (onset/offset for instructions, stimulus/click/submit for tasks). See `csv_documentation.md` for full mapping.

## Quick Start

1. Ensure PsychoPy and dependencies are installed (Anaconda environment)
2. Run: `python context_shape_task.py`
3. Enter participant name on fullscreen (like Social Recognition Task); press Enter when done
4. **ESC** exits during interactive screens (instructions, name entry, shape placement, etc.). Not during timed displays (grid, fixation). Like Social Recognition Task, no global escape—reduces accidental quits.
5. Optional: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise a timed fallback plays
6. For practice runs: use a name containing "test" to skip all file saving

**Experimenters:** See `script.md` for run-through.

## Troubleshooting

- **Random/accidental quits:** ESC is not a global key (like Social Recognition Task). It only works during interactive screens (instructions, name entry, shape placement, Phase 2 questions, debrief). During timed displays (grid, fixation, stimulus), ESC does nothing—reduces accidental quits from key repeat or stray keypresses.
- **`zsh: killed` (OOM, often during Phase 3):** Use windowed mode to reduce memory: `PSYCHOPY_WINDOWED=1` (1280×720). Default is fullscreen. The task also runs periodic garbage collection between phases and trials.
- **Dummy window:** A small 100×100 window is kept open (like Social Recognition Task) to improve stability. Disable with `PSYCHOPY_DUMMY_WINDOW=0`.
- **Mac:** Parallel port is not supported; TTL is logged only. Cedrus pyxid2 works if connected.

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
