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
- **`script.md`** — All on-screen text and suggested experimenter spoken instructions for each phase

### Stimuli

- **`STIMULI/Shapes/`** — 16 shape PNGs (Shape_X_Y.png) + ShapeGrid_4x4.png
- **`STIMULI/Context_Images/`** — Context category folders (bark, cloud, coral, etc.) + practice1.png, practice2.png
- **`STIMULI/tutorial_video.mp4`** — Optional. Video showing the dragging process (red square, red circle, green circle). Subtitles describe what's on screen; include "There were alternative ways of grouping, but this is what we went with." If missing, an animated fallback simulates the sequence.

## Data Output

All CSV data is written incrementally to `../LOG_FILES/` (relative to the task root). Participant name is appended to all filenames.

| File | Description |
|------|-------------|
| `phase1_{participant}.csv` | Per-shape: shape path, final (x,y), RT, TTL timestamps |
| `phase2_{participant}.csv` | Per-trial: shape, contexts, variant, response, RT, TTL timestamps |
| `phase3_{participant}.csv` | Same structure as phase1 |
| `debrief_{participant}.csv` | Post–Phase 3: 2 Yes/No questions, answers, RT, onset/response TTL |
| `summary_{participant}.csv` | Total task time, grid dimensions, ground-truth positions |
| `ttl_log_{participant}.csv` | Every TTL trigger: timestamp, trigger code, event label, trial info |

## TTL Triggers

TTL triggers are sent via Blackrock parallel port (or Cedrus pyxid2 on macOS) for every screen change and response. See `csv_documentation.md` for event mapping.

## Quick Start

1. Ensure PsychoPy and dependencies are installed (Anaconda environment)
2. Run: `python context_shape_task.py`
3. Enter participant name on fullscreen (like Social Recognition Task); press Enter when done
4. **ESC** exits at any time. **Enter** submits/continues (no buttons)
5. Optional: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise a timed fallback plays

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
