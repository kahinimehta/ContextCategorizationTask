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
- **Display**: Fullscreen (or windowed via `PSYCHOPY_WINDOWED=1`)
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
| `phase1_{participant}_{datetime}.csv` | Per-shape: final (x,y), RT (to last click), all_click_ttl, submit_ttl |
| `phase1_placements_{participant}_{datetime}.png` | Image of final shape placements at end of Phase 1 |
| `phase2_{participant}_{datetime}.csv` | Per-trial: shape, 2 contexts, variant, response, RT, TTL timestamps |
| `phase3_{participant}_{datetime}.csv` | Same structure as phase1 |
| `phase3_placements_{participant}_{datetime}.png` | Image of final shape placements at end of Phase 3 |
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
4. **ESC** exits at any time. **Click** to move shapes, **Enter** to submit (Phase 1 & 3); **Enter** to continue through instructions
5. Optional: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise a timed fallback plays
6. For practice runs: use a name containing "test" to skip all file saving

**Experimenters:** See `script.md` for run-through and ELI5 scripts.

## Troubleshooting

- **`zsh: killed` (OOM):** If the process is killed during Phase 2 or 3, try running in windowed mode to reduce memory use: `PSYCHOPY_WINDOWED=1 python context_shape_task.py`
- **Mac:** Parallel port is not supported; TTL is logged only. Cedrus pyxid2 works if connected.

## Paths

All paths in the code are relative to the script location. Clone the repo and run from the task root; stimuli are included.
