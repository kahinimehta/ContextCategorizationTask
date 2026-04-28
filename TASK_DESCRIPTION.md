# Context Shape Task — Technical Description

Canonical copy for **`context_shape_task.py`** timing constants (**`*_SEC`**), stimulus paths, **`phase2_trial_order.csv`**, trials→grid mapping, and troubleshooting. Narrative experiment flow (**Welcome**, instruction strings, TTL **names**) lives in **`script.md`**.

---

## Code overview

PsychoPy (v2025.1.1), Python 3. Main module: **`context_shape_task.py`**.

**Sequence:** Participant id → welcome + (**`tutorial_video.mp4`** or fallback) → **Phase 1** (full-screen grid/fixation → per-trial: isolated shape + **bottom-right miniature** **`ShapeGrid_4x4_bmp.png`** through preview and placement) → **Phase 2** (instructions → practice **`practice1`**/**`practice2`** demo → **`phase2_trial_order.csv`**) → **Phase 3** (same inset behavior as Phase 1 → debrief) → thanks (**`THANKS_SCREEN_SEC`**). Verbatim wording: **`script.md`**.

**Writes:** **`../LOG_FILES/`** — skipped entirely if **`test`** occurs in participant name (**`ttl_log_*`** likewise removed).

---

## Specifications

### Stimulus Paths

- **Shapes:** `STIMULI/shapes/*.bmp` — 16 task shapes are the first 16 files by sorted name (excludes `ShapeGrid*`); each maps to a 4×4 cell by that order (row-major)
- **Context images:** `STIMULI/contexts/{category}1.png` and `STIMULI/contexts/{category}.png` (two variants per category; e.g. `sky1` / `sky`). **Phase 2 tutorial only:** dedicated `practice1.png` / `practice2.png` (**space** / **circus**) in `STIMULI/` or `contexts/`.
- **Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png` — full-screen 5 s preview in Phase 1/3, then a **miniature** copy in the **bottom-right** for every shape trial (**`SHAPE_STATIC_PREVIEW_SEC`** + click-to-place) until that phase ends (rebuild with `scripts/generate_shape_grid.py` so cell order matches sorted `*.bmp` order)

### Phase 2 trial template (`phase2_trial_order.csv`)

- **Location:** Task root (next to `context_shape_task.py`).
- **Size:** Header row plus **N** trial rows (row order = run order for every participant). The shipped template defines **64** trials; replacing the file updates N automatically (`stderr` prints the loaded count at run time).
- **Columns** (exact header order in the repo template): `trial_number`, `shape`, `shape_path`, `primary_context`, `secondary_context`, `context1`, `context1_image`, `context2`, `context2_image`, `variant`. **`primary_context` / `secondary_context`** design labels may also appear under legacy names `strong_context` / `neutral_context`.
- **Paths:** `shape_path`, `context1_image`, and `context2_image` may be absolute or relative to `STIMULI/`. The script normalizes `Shapes`/`Contexts` in absolute paths to on-disk `shapes`/`contexts`.
- **What the code reads:** stimulus paths and `context1`/`context2` (A/B); `variant` plus primary/secondary labels are **logged only**. Presentation follows **`context*_image`** paths and button labels—not `variant`-driven branching.
- **Output alignment:** `phase2_*.csv` rows match template rows in order (trial 1…N).

### TTL

Incremental logging (**Cedrus pyxid2** or TTL parallel port — **Darwin:** timestamps only unless hardware attached). Timing semantics preamble + exhaustive **`ttl_log_*`** event table (**`csv_documentation.md`**).

---

## Timing (Stimulus Durations)

**Source of truth:** `context_shape_task.py` module constants (names ending in `_SEC`; e.g. `PHASE2_REDDOT_DURATION_SEC`, `PHASE_GRID_PREVIEW_SEC`). The tables below mirror those values.

### Tutorial (fallback)

| Step | Duration | Content |
|------|----------|---------|
| 1 | 2.5 s | Three shapes overview |
| 2 | 3 s | Red square: 1 s center, 2 s at target |
| 3 | 3 s | Red circle: 1 s center, 2 s at target |
| 4 | 3 s | Green circle: 1 s center, 2 s at target |
| 5a | 3 s | Groups explained |
| 5b | 4 s | "Not a line/spectrum" |
| 6 | 7 s | "Objects in a group can be farther apart..." + "We click to place each shape and press Enter to submit each shape's position." |

### Phase 1

| Event | Duration |
|-------|----------|
| Grid (`ShapeGrid_4x4_bmp.png`) | `PHASE_GRID_PREVIEW_SEC` (5 s) |
| Fixation (cross) | `PHASE_FIXATION_CROSS_SEC` (1 s) |
| Shape display (before clickable) | `SHAPE_STATIC_PREVIEW_SEC` (1 s); **miniature** `ShapeGrid_4x4_bmp.png` bottom-right (same as placement) |
| Click-to-place | Participant-paced; at least one click required, then Enter to submit. Miniature full grid in bottom-right for entire sorting block (same inset as preview) |

### Phase 2 Tutorial

| Event | Duration |
|-------|----------|
| Fixation | `PHASE2_FIXATION_PRE_TRIAL_SEC` |
| Context 1 (**`practice1.png`**, SPACE) | `PHASE2_SEGMENT_SEC` |
| Shape (blue circle) | `PHASE2_SEGMENT_SEC` |
| Blank | `PHASE2_SEGMENT_SEC` |
| Red dot + label (PLANET) | `PHASE2_REDDOT_DURATION_SEC` |
| Context 2 (**`practice2.png`**, CIRCUS) | `PHASE2_SEGMENT_SEC` |
| Shape 2 | `PHASE2_SEGMENT_SEC` |
| Blank 2 | `PHASE2_SEGMENT_SEC` |
| Red dot 2 + label (BALL) | `PHASE2_REDDOT_DURATION_SEC` |
| Question (SPACE \| CIRCUS static) | 1.5 s (`PHASE2_TUTORIAL_QUESTION_PREVIEW_SEC`) |
| Highlight + "You might select CIRCUS" | 1 s (`PHASE2_TUTORIAL_HIGHLIGHT_FEEDBACK_SEC`) |
| Post-blank | 3 s (`PHASE2_TUTORIAL_POST_BLANK_SEC`) |

### Phase 2 Trials (per trial)

| Event | Duration |
|-------|----------|
| Fixation | `PHASE2_FIXATION_PRE_TRIAL_SEC` (0.5 s) |
| Context 1 | 1 s (`PHASE2_SEGMENT_SEC`) |
| Shape | 1 s (`PHASE2_SEGMENT_SEC`) |
| Blank 1 | 1 s (`PHASE2_SEGMENT_SEC`) |
| Red dot | `PHASE2_REDDOT_DURATION_SEC` (2 s) |
| Context 2 | 1 s (`PHASE2_SEGMENT_SEC`) |
| Shape 2 | 1 s (`PHASE2_SEGMENT_SEC`) |
| Blank 2 | 1 s (`PHASE2_SEGMENT_SEC`) |
| Red dot 2 | `PHASE2_REDDOT_DURATION_SEC` (2 s) |
| Question (**Which context fits the object better?**; click A or B) | Participant-paced |
| ITI (blank) | `PHASE2_TRIAL_ITI_SEC` (0.5 s) |

### Phase 3

| Event | Duration |
|-------|----------|
| Grid (`ShapeGrid_4x4_bmp.png`) | `PHASE_GRID_PREVIEW_SEC` |
| Fixation (cross) | `PHASE_FIXATION_CROSS_SEC` |
| Shape display (before clickable) | `SHAPE_STATIC_PREVIEW_SEC` (1 s); miniature grid bottom-right (same as Phase 1) |
| Click-to-place | Participant-paced; at least one click required, then Enter to submit. Miniature full grid in bottom-right for entire sorting block |

### Other

| Event | Duration |
|-------|----------|
| Thank-you screen | `THANKS_SCREEN_SEC` (2 s) |
| Break (every 16 Phase 2 trials) | Participant-paced |
| Instruction screens | Participant-paced (Enter to continue); **phase2_instr5** minimum `PHASE2_INSTR5_MIN_SEC` |
| Phase 2 before trials | "Ask the experimenter now if you have any questions. Press Enter when you're ready to begin." |

---

## Trial order, mapping, randomization

| Phase | Selection | Ground truth / mapping |
|-------|-----------|------------------------|
| **1** | `random.shuffle(get_shape_paths())`; if first item is alphabetically first task shape (`ball_slope.bmp` default), rotate it to end | Clicks → `(x,y)`; row/col from index in sorted 4×4 list ( **`ShapeGrid_4x4_bmp.png`** order via `scripts/generate_shape_grid.py`). |
| **2** | Fixed **`phase2_trial_order.csv`** order (**N** trial rows) | Paths from **`context*_image`**; **`context1`/`context2`** → buttons. **`variant`**: logged only (see **Phase 2 trial template**). |
| **3** | `random.shuffle` until sequence ≠ Phase 1 order | Same (x,y)→cell mapping as Phase 1; Euclidean distances in **`summary`** CSV |

Phase 2 **tutorial** (not from CSV): `practice1.png`/`practice2.png`, circle demo, scripted SPACE \| CIRCUS.

---

## Troubleshooting

- **Random/accidental quits:** ESC is not a global key (like Social Recognition Task). It only works during interactive screens (instructions, name entry, shape placement, Phase 2 questions, debrief). During timed displays (grid, fixation, stimulus), ESC does nothing—reduces accidental quits from key repeat or stray keypresses. Command + Q will always kill the tasks. 
- **`zsh: killed` (OOM, often during Phase 3):** Use windowed mode to reduce memory: `PSYCHOPY_WINDOWED=1` (1280×720). Default is fullscreen. The task also runs periodic garbage collection between phases and trials.
- **Dummy window:** A small 100×100 window is kept open (like Social Recognition Task) to improve stability. Disable with `PSYCHOPY_DUMMY_WINDOW=0`.
- **Mac:** Parallel port is not supported; TTL is logged only. Cedrus pyxid2 works if connected.
- **Mac `ObjCInstance` / NSTrackingArea crash:** If `visual.Window(...)` crashes at startup (`NSTrackingArea` has no attribute `type`), PsychoPy’s initial **`getActualFrameRate()`** path calls `flip()` and triggers a known pyglet/Cocoa interaction. The script passes **`checkTiming=False`** by default on macOS so startup frame calibration is skipped. Enable calibration with **`PSYCHOPY_CHECK_TIMING=1`** only if needed and stable. Separately during trials the script uses `time.sleep` instead of `core.wait` on macOS where the same ObjC bug can occur.
- **Mac Enter/keys not working:** On macOS, the script disables PsychoPy's hardware keyboard backend (known to freeze or ignore keys) and uses `event.getKeys` only. If keys still don't register, ensure the PsychoPy window has focus.
