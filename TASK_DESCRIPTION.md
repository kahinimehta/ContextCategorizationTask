# Context Shape Task — Technical Description

Technical specification: timing, trial selection, randomization, stimulus durations, troubleshooting. **Experimenter script:** `script.md`. **CSV/TTL mapping:** `csv_documentation.md`.

---

## Code Overview

**Implementation:** PsychoPy (v2025.1.1), Python 3. Main script: `context_shape_task.py`.

**Flow:**
1. **Login** — Participant name (fullscreen, Enter to submit)
2. **Welcome** — Full line on screen: see script.md (Welcome). Video or fallback follows.
3. **Tutorial** — Video (`STIMULI/tutorial_video.mp4`) or animated fallback (red square, red circle, green circle; click-to-place demo)
4. **Phase 1** — Bottom-up shape classification: grid preview (5 s) → fixation (1 s) → 16 shapes one-by-one (click to place, Enter to submit; at least one click required). While placing, a **miniature full grid** (`STIMULI/shapes/ShapeGrid_4x4_bmp.png`) stays in the **bottom-right** for the whole sort.
5. **Phase 2** — Top-down context: 7 instruction screens (instr5 min 5 s: "Now let's watch a quick demo to help you understand..."); tutorial; "Ask the experimenter now if you have any questions" screen; all trials from `phase2_trial_order.csv` (fixed order; breaks every 16); each trial: context1 → shape → blank → red dot (2 s) → context2 → shape → blank → red dot (2 s) → question (choose A or B)
6. **Phase 3** — Post-context shape reclassification: phase3_questions first ("Ask the experimenter now"), then instr1–4; before-grid screen; grid preview (5 s) → fixation (1 s) → 2 instruction screens (sort prompt: "Sort by where you'd expect to see the shapes") → same click-to-place task as Phase 1 including **miniature grid** in the bottom-right; 16 shapes in different random order
7. **Debrief** — 3 Yes/No questions (same grouping strategy?; images influenced grouping?; interpreted shapes differently?)
8. **End** — Thank-you screen (2 s)

**Output:** CSVs/PNGs in `../LOG_FILES/` (phase1, phase2, phase3, debrief, summary, ttl_log, placement images). No files if participant name contains "test". Example filenames in repo: README → Example output.

---

## Specifications

### Stimulus Paths

- **Shapes:** `STIMULI/shapes/*.bmp` — 16 task shapes are the first 16 files by sorted name (excludes `ShapeGrid*`); each maps to a 4×4 cell by that order (row-major)
- **Context images:** `STIMULI/contexts/{category}1.png` and `STIMULI/contexts/{category}.png` (two variants per category; e.g. `sky1` / `sky`)
- **Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png` for Phase 1 and Phase 3 preview and inset
- **Phase 2 trial template:** See **Phase 2 trial template** subsection below.

### Phase 2 trial template (`phase2_trial_order.csv`)

- **Location:** Task root (next to `context_shape_task.py`).
- **Size:** Header row plus **N** trial rows (row order = run order for every participant).
- **Columns:** `trial_number`, `shape`, `shape_path`, `context1`, `context1_image`, `context2`, `context2_image`, `variant`; design labels `primary_context` & `secondary_context` (or legacy `strong_context` / `neutral_context`).
- **Paths:** `shape_path`, `context1_image`, and `context2_image` may be absolute or relative to `STIMULI/`. The script normalizes `Shapes`/`Contexts` in absolute paths to on-disk `shapes`/`contexts`.
- **What the code reads:** `shape_path`, `context1_image`, `context2_image`, `context1` and `context2` (category labels for A/B), `variant`, and optional primary/secondary context labels for logging.
- **Output alignment:** Each row of `phase2_{participant}_{datetime}.csv` matches the same-index row in this file (stimulus columns + variant); `trial` is 1…N in presentation order.

### Phase 2 Trial Variants

The `variant` column is a **pass-through** design label in the current template (e.g. `primary_first_img0`, `secondary_first_img1`); the script does not change trial logic based on it—only **which image** is in `context1_image` / `context2_image` and **which** labels are in `context1` / `context2` matter for presentation.

### TTL

Every screen change and response logged. Backend: Cedrus pyxid2 or parallel port (Mac: log only). See `csv_documentation.md` for full mapping.

---

## Timing (Stimulus Durations)

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
| Grid (`ShapeGrid_4x4_bmp.png`) | 5 s |
| Fixation (cross) | 1 s |
| Shape display (before clickable) | 1 s |
| Click-to-place | Participant-paced; at least one click required, then Enter to submit. Miniature full grid in bottom-right for entire phase |

### Phase 2 Tutorial

| Event | Duration |
|-------|----------|
| Fixation | 0.5 s |
| Context 1 (practice1) | 1 s |
| Shape (blue circle) | 1 s |
| Blank | 1 s |
| Red dot + label (PLANET) | 2 s |
| Context 2 (practice2) | 1 s |
| Shape 2 | 1 s |
| Blank 2 | 1 s |
| Red dot 2 (BALL) | 2 s |
| Question (CIRCUS | SPACE) | 1.5 s |
| Demo select ("You might select CIRCUS") | 1 s |
| Post-blank | 3 s |

### Phase 2 Trials (per trial)

| Event | Duration |
|-------|----------|
| Fixation | 0.5 s |
| Context 1 | 1 s |
| Shape | 1 s |
| Blank 1 | 1 s |
| Red dot | 2 s |
| Context 2 | 1 s |
| Shape 2 | 1 s |
| Blank 2 | 1 s |
| Red dot 2 | 2 s |
| Question (click A or B) | Participant-paced |
| ITI (blank) | 0.5 s |

### Phase 3

| Event | Duration |
|-------|----------|
| Grid (`ShapeGrid_4x4_bmp.png`) | 5 s |
| Fixation (cross) | 1 s |
| Shape display (before clickable) | 1 s |
| Click-to-place | Participant-paced; at least one click required, then Enter to submit. Miniature full grid in bottom-right for entire phase |

### Other

| Event | Duration |
|-------|----------|
| Thank-you screen | 2 s |
| Break (every 16 Phase 2 trials) | Participant-paced |
| Instruction screens | Participant-paced (Enter to continue); phase2_instr5 min 5 s |
| Phase 2 before trials | "Ask the experimenter now if you have any questions. Press Enter when you're ready to begin." |

---

## Trial Selection and Mapping

### Phase 1

- **Source:** First 16 `*.bmp` in `STIMULI/shapes/` by sorted filename (excludes `ShapeGrid*`).
- **Selection:** `get_shape_paths()`; then `random.shuffle(shapes)`.
- **Constraint:** If the first shuffled file is the alphabetically first task shape (`ball_slope.bmp` in the default set), move it to the end of the list.
- **Mapping:** Clicks to `(x, y)`; ground-truth row/col is the shape’s index in the sorted 4×4 list (0–3 for row and column), not the filename.

### Phase 2

- **Source:** `phase2_trial_order.csv` — fixed order for all participants (N rows in the template).
- **Selection:** No randomization. Order is CSV row order after the header.
- **Mapping:** Each row supplies `shape_path`, `context1_image`, `context2_image`, `context1` (left label / cat_a), `context2` (right label / cat_b), `variant`. Variants control which images appear and how left/right map to categories.

### Phase 3

- **Source:** Same 16 shapes as Phase 1.
- **Selection:** `random.shuffle(shapes3)` with constraint: `shapes3 != shapes` (different order than Phase 1); reshuffle until different.
- **Mapping:** Same as Phase 1. Euclidean distances between final positions used for similarity analysis.

---

## Randomization Summary

| Phase | What | How |
|-------|------|-----|
| Phase 1 | Shape order | `random.shuffle(shapes)`; default first sorted `.bmp` not first |
| Phase 2 | Trial order | None — fixed from CSV |
| Phase 3 | Shape order | `random.shuffle(shapes3)`; must differ from Phase 1 |
| Tutorial fallback | N/A | Fixed sequence |
| Phase 2 tutorial | N/A | Fixed (`sky1`, `petshop1`, circle, PLANET/BALL, SKY/PETSHOP demo) |

---

## Troubleshooting

- **Random/accidental quits:** ESC is not a global key (like Social Recognition Task). It only works during interactive screens (instructions, name entry, shape placement, Phase 2 questions, debrief). During timed displays (grid, fixation, stimulus), ESC does nothing—reduces accidental quits from key repeat or stray keypresses. Command + Q will always kill the tasks. 
- **`zsh: killed` (OOM, often during Phase 3):** Use windowed mode to reduce memory: `PSYCHOPY_WINDOWED=1` (1280×720). Default is fullscreen. The task also runs periodic garbage collection between phases and trials.
- **Dummy window:** A small 100×100 window is kept open (like Social Recognition Task) to improve stability. Disable with `PSYCHOPY_DUMMY_WINDOW=0`.
- **Mac:** Parallel port is not supported; TTL is logged only. Cedrus pyxid2 works if connected.
- **Mac `ObjCInstance` crash:** If the task crashes during timed displays with `ObjCInstance has no attribute type`, the script uses `time.sleep` instead of `core.wait` on macOS to avoid this pyglet Cocoa bug.
- **Mac Enter/keys not working:** On macOS, the script disables PsychoPy's hardware keyboard backend (known to freeze or ignore keys) and uses `event.getKeys` only. If keys still don't register, ensure the PsychoPy window has focus.
- **csvs** are written out incrementally
