# Context Shape Task — Technical Description

Canonical **`context_shape_task.py`** reference for **`*_SEC` timings**, stimulus paths, **`phase2_trial_order.csv`**, grid mapping, and **troubleshooting**. **On-screen wording** and step-by-step flow: **`script.md`**. **TTL / CSV columns:** **`csv_documentation.md`**.

---

## Code overview

PsychoPy (v2025.1.1), Python 3. Main module: **`context_shape_task.py`**.

**Writes:** **`../LOG_FILES/`** — skipped if participant name contains **`test`** (including **`ttl_log_*`**).

---

## Specifications

### Stimulus Paths

- **Task objects (.bmp):** `STIMULI/shapes/*.bmp` — 16 stimuli are the first 16 files by sorted name (excludes `ShapeGrid*`); each maps to a 4×4 cell by that order (row-major). At load, each **task** `.bmp` (not `ShapeGrid*` composites) has **near-white matte pixels** (R, G, B ≥ **`OBJECT_WHITE_BG_STRIP_THRESHOLD`**, default **247**) **set to transparent** in PsychoPy; context PNGs and the grid composite are unchanged.
- **Contexts:** `STIMULI/contexts/{category}1.png` and `STIMULI/contexts/{category}.png` (two variants per category; e.g. `sky1` / `sky`). **Phase 2 tutorial only:** dedicated `practice1.png` / `practice2.png` (**space** / **circus**) in `STIMULI/` or `contexts/`.
- **Phase 2 context on-screen framing:** Every context image (tutorial + main trials) is drawn in a **fixed square** centered on screen in PsychoPy `units='height'`: side length **`PHASE2_CONTEXT_MAX_EXTENT`** (default **1.0**), with **`PHASE2_CONTEXT_FRAME_ASPECT_W_OVER_H`** default **1.0** (square). Source PNGs are **uniformly scaled** and **center-cropped** (object-fit **cover**) in Pillow so pixels keep aspect ratio inside that box — see **`_phase2_context_frame_size_height_units`** / **`_phase2_context_image_cropped_pil`** in **`context_shape_task.py`**.
- **Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png` — Phase 1/3: fullscreen preview + bottom-right miniature through fixation, then instruction screens and sorting (**TTL labels:** **`script.md`** / **`csv_documentation.md`**). Rebuild composite: **`scripts/generate_shape_grid.py`** (cell order = sorted `*.bmp` order).

### Phase 2 trial template (`phase2_trial_order.csv`)

- **Location:** Task root (next to `context_shape_task.py`).
- **Size:** Header row plus **N** trial rows (row order = run order for every participant). The shipped template defines **64** trials; replacing the file updates N automatically (`stderr` prints the loaded count at run time).
- **Columns** (exact header order in the repo template): `trial_number`, `shape`, `shape_path`, `primary_context`, `secondary_context`, `context1`, `context1_image`, `context2`, `context2_image`, `variant`. **`primary_context` / `secondary_context`** design labels may also appear under legacy names `strong_context` / `neutral_context`.
- **Paths:** `shape_path`, `context1_image`, and `context2_image` may be absolute or relative to `STIMULI/`. The script normalizes `Shapes`/`Contexts` in absolute paths to on-disk `shapes`/`contexts`.
- **What the code reads:** stimulus paths and `context1`/`context2` (A/B); `variant` plus primary/secondary labels are **logged only**. Presentation follows **`context*_image`** paths and button labels—not `variant`-driven branching.
- **Output alignment:** `phase2_*.csv` rows match template rows in order (trial 1…N). **`fixation_onset_ttl` … `question_onset_ttl`** cells duplicate the **Unix onset times** logged in **`ttl_log_*`** (see **`csv_documentation.md`**).

### TTL

Hardware (**Cedrus** / parallel); **Darwin:** often log-only. **`reddot`** labels = black cue-dot epochs. **Video vs fallback** tutorial streams are mutually exclusive — event list: **`csv_documentation.md`**.

---

## Timing (Stimulus Durations)

**Source of truth:** `context_shape_task.py` module constants (names ending in `_SEC`; e.g. `PHASE2_REDDOT_DURATION_SEC`, `PHASE_GRID_PREVIEW_SEC`, `TRAINING_DEMO_SCREEN_EXTRA_SEC` adds time on scripted training-demo screens only — real Phase 2 trials still use `PHASE2_SEGMENT_SEC` / `PHASE2_REDDOT_DURATION_SEC`). Phase 2 transitions from each **task object** epoch to the following **black cue dot** with **no** intervening blank (`PHASE2_SEGMENT_SEC` still controls context/object display length only). **`PHASE2_REDDOT_*`** names are historical; the on-screen dot is **black**.

### Tutorial (fallback)

Durations below; **verbatim subtitles and transition:** **`script.md`** (Tutorial). Steps 2–4 each use center then target epochs (`TUTORIAL_FB_CLICK_CENTER_SEC` + `TUTORIAL_FB_CLICK_TARGET_SEC`); **`tutorial_fallback_step{n}_*`** TTLs: **`csv_documentation.md`**.

| Step | Duration | Content (summary) |
|------|----------|-------------------|
| 1 | **4** s (`TUTORIAL_FB_OVERVIEW_SEC`) | Three-shape overview + intro subtitle |
| 2 | **6** s total | Red square click-to-place |
| 3 | **6** s total | Red circle joins cluster |
| 4 | **6** s total | Green circle to right group |
| 5a | **4.5** s | Color-group summary (circled reds vs green) |
| 5b | **5.5** s | Spectrum / proximity subtitle |
| 6 | **8.5** s | Enter-reminder subtitle only *(optional “large spread” line commented out in code)* |

### Phase 1

| Event | Duration |
|-------|----------|
| Grid (`ShapeGrid_4x4_bmp.png`) | `PHASE_GRID_PREVIEW_SEC` (5 s); large centered grid + **miniature** same PNG bottom-right |
| Fixation (cross) | `PHASE_FIXATION_CROSS_SEC` (1 s); cross + **miniature** grid bottom-right |
| Task object display (before clickable) | `SHAPE_STATIC_PREVIEW_SEC` (1 s); **miniature** `ShapeGrid_4x4_bmp.png` bottom-right (same as placement) |
| Click-to-place | Participant-paced; at least one click required, then Enter to submit. Miniature full grid in bottom-right for entire sorting block (same inset as preview) |

### Phase 2 Tutorial

| Event | Duration |
|-------|----------|
| Intro (`phase2_tutorial_intro`) | Min **`PHASE2_INSTR5_MIN_SEC`** before Enter; copy **`script.md`** |
| Fixation | `PHASE2_TUTORIAL_FIXATION_SEC` (2 s); main trials remain `PHASE2_FIXATION_PRE_TRIAL_SEC` |
| Context 1 (**`practice1.png`**, SPACE) | `PHASE2_TUTORIAL_SEGMENT_SEC` (2.5 s); main trials: `PHASE2_SEGMENT_SEC`; **same square framing as trials** (center cover crop) |
| Task object (blue circle) | `PHASE2_TUTORIAL_SEGMENT_SEC` |
| Black dot + label (PLANET) | `PHASE2_TUTORIAL_REDDOT_SEC` (3.5 s); main trials: `PHASE2_REDDOT_DURATION_SEC` (**immediately** after circle) |
| Context 2 (**`practice2.png`**, CIRCUS) | `PHASE2_TUTORIAL_SEGMENT_SEC` |
| Task object 2 | `PHASE2_TUTORIAL_SEGMENT_SEC` |
| Black dot 2 + label (BALL) | `PHASE2_TUTORIAL_REDDOT_SEC` |
| Choice preview + highlight | **3** s + **2.5** s (`PHASE2_TUTORIAL_QUESTION_PREVIEW_SEC`, `PHASE2_TUTORIAL_HIGHLIGHT_FEEDBACK_SEC`); UI details **`csv_documentation.md`** (`phase2_tutorial_question_*`, `phase2_tutorial_demo_select_*`) |
| Post-blank | **4.5** s (`PHASE2_TUTORIAL_POST_BLANK_SEC`) |

### Phase 2 Trials (per trial)

| Event | Duration |
|-------|----------|
| Fixation | `PHASE2_FIXATION_PRE_TRIAL_SEC` (0.5 s) |
| Context 1 | 1 s (`PHASE2_SEGMENT_SEC`); **centered square**, center **cover** crop (same size all trials) |
| Task object | 1 s (`PHASE2_SEGMENT_SEC`); cue dot follows **without** intervening blank |
| Cue dot (black) | `PHASE2_REDDOT_DURATION_SEC` (2 s) |
| Context 2 | 1 s (`PHASE2_SEGMENT_SEC`); same square as context 1 |
| Task object 2 | 1 s (`PHASE2_SEGMENT_SEC`); cue dot 2 follows **without** intervening blank |
| Cue dot 2 (black) | `PHASE2_REDDOT_DURATION_SEC` (2 s) |
| Question | Participant-paced; main prompt **"Which context fits best? Use the left/right keys to choose."** and **← / →** mapping as **`script.md`** / **`csv_documentation.md`** (no separate gray arrow subtitle). |
| ITI (blank) | `PHASE2_TRIAL_ITI_SEC` (0.5 s) |

### Phase 3

| Event | Duration |
|-------|----------|
| Grid (`ShapeGrid_4x4_bmp.png`) | `PHASE_GRID_PREVIEW_SEC`; large + miniature bottom-right (same as Phase 1) |
| Fixation (cross) | `PHASE_FIXATION_CROSS_SEC`; cross + miniature bottom-right |
| Task object display (before clickable) | `SHAPE_STATIC_PREVIEW_SEC` (1 s); miniature grid bottom-right (same as Phase 1) |
| Click-to-place | Participant-paced; at least one click required, then Enter to submit. Miniature full grid in bottom-right for entire sorting block |
| Debrief (3 questions, after Phase 3) | Participant-paced; **←** = Yes, **→** = No; on-screen **`USE THE ARROW KEYS TO ANSWER`**. See **`script.md`** / **`csv_documentation.md`**. |

### Other

| Event | Duration |
|-------|----------|
| Thank-you screen | `THANKS_SCREEN_SEC` (2 s) |
| Break (every 16 Phase 2 trials) | Participant-paced |
| Enter-to-continue instruction screens | Participant-paced; copy **`script.md`**, event labels **`csv_documentation.md`** |

---

## Trial order, mapping, randomization

| Phase | Selection | Ground truth / mapping |
|-------|-----------|------------------------|
| **1** | `random.shuffle(get_shape_paths())`; if first item is alphabetically first task shape (`ball_slope.bmp` default), rotate it to end | Clicks → `(x,y)`; row/col from index in sorted 4×4 list ( **`ShapeGrid_4x4_bmp.png`** order via `scripts/generate_shape_grid.py`). |
| **2** | Fixed **`phase2_trial_order.csv`** order (**N** trial rows) | Paths from **`context*_image`**; **`context1`/`context2`** → buttons. **`variant`**: logged only (see **Phase 2 trial template**). |
| **3** | `random.shuffle` until sequence ≠ Phase 1 order | Same (x,y)→cell mapping as Phase 1; Euclidean distances in **`summary`** CSV |

Phase 2 practice demo uses **`practice1.png`** / **`practice2.png`** (not CSV); **`phase2_ready`** then **`phase2_before_trials`** precede main trials.

---

## Troubleshooting

- **Random/accidental quits:** ESC is not a global key (like Social Recognition Task). It only works during interactive screens (instructions, name entry, object placement, Phase 2 questions, debrief). During timed displays (grid, fixation, stimulus), ESC does nothing—reduces accidental quits from key repeat or stray keypresses. Command + Q will always kill the tasks. 
- **`zsh: killed` (OOM, often during Phase 3):** Use windowed mode to reduce memory: `PSYCHOPY_WINDOWED=1` (1280×720). Default is fullscreen. The task also runs periodic garbage collection between phases and trials.
- **Dummy window:** A small 100×100 window is kept open (like Social Recognition Task) to improve stability. Disable with `PSYCHOPY_DUMMY_WINDOW=0`.
- **Mac:** Parallel port is not supported; TTL is logged only. Cedrus pyxid2 works if connected.
- **Mac `ObjCInstance` / `.type()` crash (pyglet Cocoa):** AppKit can return an **`__NSSingleObjectArrayI`** wrapper instead of a bare **NSEvent** from `nextEventMatchingMask`; pyglet then calls **`event.type()`** and crashes (`ObjCInstance … has no attribute 'type'`). This can hit **`flip()`** during **Phase 2** (not only startup). The script installs a small **unwrap** patch for **`CocoaWindow.dispatch_events`** by default on macOS (mirror of pyglet’s loop, first element taken when the dequeue result is array-like). Disable with **`PSYCHOPY_COCOA_EVENT_PATCH=0`** if you need the stock pyglet path. If **`Window(...)`** crashes at startup (`NSTrackingArea` has no attribute `type`), that is PsychoPy’s **`getActualFrameRate()`** path; the script uses **`checkTiming=False`** by default on macOS unless **`PSYCHOPY_CHECK_TIMING=1`**. Timed waits use **`time.sleep`** instead of **`core.wait`** on macOS where **`core.wait`** can worsen event-dispatch issues.
- **Mac Enter/keys not working:** On macOS, the script disables PsychoPy's hardware keyboard backend for **Enter-to-continue** screens (known to freeze); those use `event.getKeys` with normalization. **Participant id** uses **unrestricted** **`event.getKeys()`** then filters keys in code (see **`get_participant_name`**). Ensure the PsychoPy window has focus—the script calls **`_ensure_psychopy_window_key_focus`** after the first name-screen draw (dummy window + macOS can steal focus).
