# Context Shape Task — Technical Description

Complete technical specification: code structure, timing, trial selection, randomization, stimulus durations, and troubleshooting.

---

## Code Overview

**Implementation:** PsychoPy (v2025.1.1), Python 3. Main script: `context_shape_task.py`.

**Flow:**
1. **Login** — Participant name (fullscreen, Enter to submit)
2. **Welcome** — "Let's get started. First, watch this example video..."
3. **Tutorial** — Video (`STIMULI/tutorial_video.mp4`) or animated fallback (red square, red circle, green circle; click-to-place demo)
4. **Phase 1** — Bottom-up shape classification: grid preview (5 s) → fixation (1 s) → 16 shapes one-by-one (click to place, Enter to submit)
5. **Phase 2** — Top-down context: 64 trials from `phase2_trial_order.csv` (fixed order); each trial: context1 → shape → blank → red dot → context2 → shape → blank → red dot → question (choose A or B)
6. **Phase 3** — Post-context shape reclassification: same click-to-place task as Phase 1 (no grid preview); 16 shapes in different random order
7. **Debrief** — 3 Yes/No questions
8. **End** — Thank-you screen (2 s)

**Output:** CSVs in `../LOG_FILES/` (phase1, phase2, phase3, debrief, summary, ttl_log). No files if participant name contains "test".

---

## Specifications

### Stimulus Paths

- **Shapes:** `STIMULI/Shapes/Shape_X_Y.png` (X,Y 0–3). Format: `.../ContextCategorizationTask/STIMULI/Shapes/Shape_X_Y.png`
- **Context images:** `STIMULI/Context_Images/{category}1.png` or `{category}_1.png` (original), `{category}2.png` or `{category}_2.png` (control)
- **Grid:** `STIMULI/Shapes/ShapeGrid_4x4_scrambled.png` for Phase 1 preview
- **Phase 2 trial order:** `phase2_trial_order.csv` — paths can be absolute or relative to STIMULI

### Phase 2 Trial Variants

| Variant | Description |
|---------|-------------|
| `original` | Strong context first, neutral second; standard mapping |
| `context_swapped` | Order of contexts swapped (left/right button positions) |
| `control_context` | Control context images used |
| `control_context_swapped` | Control context images + order swapped |

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
| 6 | 2.5 s | Enter to submit reminder |

### Phase 1

| Event | Duration |
|-------|----------|
| Grid (ShapeGrid_4x4_scrambled) | 5 s |
| Fixation (cross) | 1 s |
| Shape display (before clickable) | 1 s |
| Click-to-place | Participant-paced; Enter to submit |

### Phase 2 Tutorial

| Event | Duration |
|-------|----------|
| Fixation | 0.5 s |
| Context 1 (practice1) | 1 s |
| Shape (blue circle) | 1 s |
| Blank | 1 s |
| Red dot + label (PLANET) | 3 s |
| Context 2 (practice2) | 1 s |
| Shape 2 | 1 s |
| Blank 2 | 1 s |
| Red dot 2 (BALL) | 3 s |
| Question (demo) | Participant-paced |
| Post-blank | 3 s |

### Phase 2 Trials (per trial)

| Event | Duration |
|-------|----------|
| Fixation | 0.5 s |
| Context 1 | 1 s |
| Shape | 1 s |
| Blank 1 | 1 s |
| Red dot | 3 s |
| Context 2 | 1 s |
| Shape 2 | 1 s |
| Blank 2 | 1 s |
| Red dot 2 | 3 s |
| Question (click A or B) | Participant-paced |
| ITI (blank) | 0.5 s |

### Phase 3

| Event | Duration |
|-------|----------|
| Shape display (before clickable) | 1 s |
| Click-to-place | Participant-paced |

### Other

| Event | Duration |
|-------|----------|
| Thank-you screen | 2 s |
| Break (every 16 Phase 2 trials) | Participant-paced |
| Instruction screens | Participant-paced (Enter to continue); phase2_instr5 min 5 s |

---

## Trial Selection and Mapping

### Phase 1

- **Source:** All 16 shapes from `STIMULI/Shapes/` (excludes ShapeGrid).
- **Selection:** `get_shape_paths()` returns sorted paths; then `random.shuffle(shapes)`.
- **Constraint:** If first shape is `Shape_0_0.png`, move it to end (`shapes.append(shapes.pop(0))`).
- **Mapping:** Shape paths mapped to `(x, y)` final positions via participant clicks. Ground truth from filename `Shape_X_Y.png` (grid row/col 0–3).

### Phase 2

- **Source:** `phase2_trial_order.csv` — fixed order for all participants.
- **Selection:** No randomization. Order is defined by CSV row order.
- **Mapping:** Each row: `shape_path`, `context1_image`, `context2_image`, `context1` (cat_a), `context2` (cat_b), `variant`. Trial variants control context image choice and left/right assignment.

### Phase 3

- **Source:** Same 16 shapes as Phase 1.
- **Selection:** `random.shuffle(shapes3)` with constraint: `shapes3 != shapes` (different order than Phase 1); reshuffle until different.
- **Mapping:** Same as Phase 1. Euclidean distances between final positions used for similarity analysis.

---

## Randomization Summary

| Phase | What | How |
|-------|------|-----|
| Phase 1 | Shape order | `random.shuffle(shapes)`; Shape_0_0 not first |
| Phase 2 | Trial order | None — fixed from CSV |
| Phase 3 | Shape order | `random.shuffle(shapes3)`; must differ from Phase 1 |
| Tutorial fallback | N/A | Fixed sequence |
| Phase 2 tutorial | N/A | Fixed (practice1, practice2, circle, PLANET/BALL) |

---

## Troubleshooting

- **Random/accidental quits:** ESC is not a global key (like Social Recognition Task). It only works during interactive screens (instructions, name entry, shape placement, Phase 2 questions, debrief). During timed displays (grid, fixation, stimulus), ESC does nothing—reduces accidental quits from key repeat or stray keypresses.
- **`zsh: killed` (OOM, often during Phase 3):** Use windowed mode to reduce memory: `PSYCHOPY_WINDOWED=1` (1280×720). Default is fullscreen. The task also runs periodic garbage collection between phases and trials.
- **Dummy window:** A small 100×100 window is kept open (like Social Recognition Task) to improve stability. Disable with `PSYCHOPY_DUMMY_WINDOW=0`.
- **Mac:** Parallel port is not supported; TTL is logged only. Cedrus pyxid2 works if connected.
- **Mac `ObjCInstance` crash:** If the task crashes during timed displays with `ObjCInstance has no attribute type`, the script uses `time.sleep` instead of `core.wait` on macOS to avoid this pyglet Cocoa bug.
- **Mac Enter/keys not working:** On macOS, the script disables PsychoPy's hardware keyboard backend (known to freeze or ignore keys) and uses `event.getKeys` only. If keys still don't register, ensure the PsychoPy window has focus.
