# Context Shape Task

This repository contains the PsychoPy implementation of the **ContextShape Task**, a multi-phase experiment examining bottom-up shape classification and top-down context incorporation.

## Acknowledgments

- **Shape generation**: Henderson et al. 2025
- **Context images**: THINGS dataset
- **Practice stimulus generation**: OpenAI
- **Coding**: Cursor
- **Idea development**: Claude

## Environment

- **Python**: Anaconda
- **PsychoPy**: v2025.1.1
- **Display**: Fullscreen with DPI scaling adjustments
- **Exit**: ESC at any time

## Repository Contents

### Core Task

- **`context_shape_task.py`** — Main PsychoPy script for the entire experiment

### Documentation

- **`csv_documentation.md`** — Column-by-column description of all CSV outputs
- **`script.md`** — All on-screen text, experimenter spoken instructions (including ELI5/simple versions for explaining to participants), and phase-by-phase script
- **`STIMULI/tutorial_video_spec.md`** — Production spec for tutorial video (content, timing, subtitles)

### Stimuli

- **`STIMULI/Shapes/`** — 16 shape PNGs (Shape_X_Y.png) + ShapeGrid_4x4.png
- **`STIMULI/Context_Images/`** — Context category folders (bark, cloud, coral, etc.) + practice1.png, practice2.png. Each category needs original (*_01b.jpg, *_01s.jpg) and control (*_02s.jpg) images—control = different image from same category, not the exact same context.
- **`STIMULI/tutorial_video.mp4`** — Optional. Video showing the click-to-place process (red square, red circle, green circle). See `STIMULI/tutorial_video_spec.md` for production spec (content, timing, subtitles). If missing, an animated fallback simulates the sequence.

## Data Output

All CSV data is written incrementally to `../LOG_FILES/` (relative to the task root). Participant name is appended to all filenames.

| File | Description |
|------|-------------|
| `phase1_{participant}_{datetime}.csv` | Per-shape: shape path, final (x,y), RT, TTL timestamps |
| `phase1_placements_{participant}_{datetime}.png` | Image of final shape placements at end of Phase 1 |
| `phase2_{participant}_{datetime}.csv` | Per-trial: shape, 2 contexts (original or control images), variant, response, RT, TTL timestamps |
| `phase3_{participant}_{datetime}.csv` | Same structure as phase1 |
| `phase3_placements_{participant}_{datetime}.png` | Image of final shape placements at end of Phase 3 |
| `debrief_{participant}_{datetime}.csv` | Post–Phase 3: 2 Yes/No questions, answers, RT, onset/response TTL |
| `summary_{participant}_{datetime}.csv` | Total task time, grid dimensions, ground-truth positions, Euclidean distances (how close shapes are categorically) |
| `ttl_log_{participant}_{datetime}.csv` | Every TTL trigger: timestamp, trigger code, event label, trial info |

*datetime* = `YYYYMMDD_HHMMSS` (e.g., 20250318_143022). **No files are written** if participant name contains "test" (case-insensitive).

**Phase 2 design:** Each shape is associated with exactly 2 context categories (A and B). Four trials per shape, e.g. for Shape 1 with categories A and B: (1) A then B, (2) B then A, (3) A-control then B-control, (4) B-control then A-control. Control = different image from same category. Different shapes can share the same context category (e.g. BARK with shape 1 and shape 5) but each context *pair* is unique to one shape.

## TTL Triggers

TTL triggers are sent via Blackrock parallel port (or Cedrus pyxid2 on macOS) for every screen change and response. Phase 1 & 3 placement uses `phase1_click_place` and `phase3_click_place` (click-to-place). See `csv_documentation.md` for the full TTL trigger mapping.

## Quick Start

1. Ensure PsychoPy and dependencies are installed (Anaconda environment)
2. Run: `python context_shape_task.py`
3. Enter participant name on fullscreen (like Social Recognition Task); press Enter when done
4. **ESC** exits at any time. **Click** to place shapes (Phase 1 & 3); **Enter** to continue through instructions
5. Optional: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise a timed fallback plays
6. For practice runs: use a name containing "test" to skip all file saving

**Experimenters:** Use `script.md` for the full run-through. It includes "Simple version" (ELI5) scripts for explaining the task in plain language to participants.

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
