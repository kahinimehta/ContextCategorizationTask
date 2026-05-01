# Context Shape Task — Technical Description

Canonical **`context_shape_task.py`** reference: **`*_SEC` timings**, stimulus paths, **`phase2_trial_order.csv`**, grid mapping, **troubleshooting**. **Verbatim screens + run order:** **`script.md`**. **TTL triggers + CSV schemas:** **`csv_documentation.md`**. **What files are written where:** **`README.md`**.

---

## Code overview

PsychoPy (**`requirements.txt`**: **`psychopy>=2025.2,<2027`**), Python 3. Main module: **`context_shape_task.py`**.

**Output directory / filenames / `test`:** **`README.md`**.

---

## Specifications

### Stimulus Paths

- **Task objects (.bmp):** `STIMULI/shapes/*.bmp` — 16 stimuli are the first 16 files by sorted name (excludes `ShapeGrid*`); each maps to a 4×4 cell by that order (row-major). At load, each **task** `.bmp` (not `ShapeGrid*` composites) has **near-white matte pixels** (R, G, B ≥ **`OBJECT_WHITE_BG_STRIP_THRESHOLD`**, default **247**) **set to transparent** in PsychoPy; context PNGs and the grid composite are unchanged.
- **Contexts:** `STIMULI/contexts/{category}1.png` and `STIMULI/contexts/{category}.png` (two variants per category; e.g. `sky1` / `sky`). **Phase 2 tutorial only:** dedicated `practice1.png` / `practice2.png` (**space** / **circus**) in `STIMULI/` or `contexts/`.
- **Phase 2 context on-screen framing:** Every context image (tutorial + main trials) is drawn in a **fixed square** centered on screen in PsychoPy `units='height'`: side length **`PHASE2_CONTEXT_MAX_EXTENT`** (default **1.0**), with **`PHASE2_CONTEXT_FRAME_ASPECT_W_OVER_H`** default **1.0** (square). Source PNGs are **uniformly scaled** and **center-cropped** (object-fit **cover**) in Pillow so pixels keep aspect ratio inside that box — see **`_phase2_context_frame_size_height_units`** / **`_phase2_context_image_cropped_pil`** in **`context_shape_task.py`**.
- **Phase 2 spoken prompt:** **`PHASE2_OBJECT_QUESTION_TEXT`** (default **"What is the object?"**) — full-screen **`TextStim`** after each object epoch (tutorial adds demo lines below). TTL **`phase2_object_question_*`** / **`phase2_object_question2_*`**; **`phase2_*.csv`** columns **`object_question_onset_ttl`** / **`object_question2_onset_ttl`**.
- **Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png` — Phase 1/3: fullscreen preview + bottom-right miniature through fixation, instructions, and sorting. Regenerate if you change the task `.bmp` set so cell order matches **sorted** `*.bmp` (`ShapeGrid*` excluded); **no grid-builder script in repo**.
- **Phase 1 & 3 sorting instructions:** Single canonical sentence **`PHASE13_CLICK_ENTER_INSTRUCTION`** in **`context_shape_task.py`** — gray trial hint plus **`phase1_instr3`** / **`phase3_instruction2c`**; tutorial fallback steps **2** and **6** use the same text.

### Phase 2 trial template (`phase2_trial_order.csv`)

- **Location:** Task root (next to `context_shape_task.py`).
- **Size:** Header row plus **N** trial rows (row order = run order for every participant). The shipped template defines **64** trials; replacing the file updates N automatically (`stderr` prints the loaded count at run time).
- **Required columns** (must be present; header order may vary — enforced by **`PHASE2_CSV_REQUIRED`** in **`context_shape_task.py`**): `shape_path`, `context1_image`, `context2_image`, `context1`, `context2`, `variant`.
- **Optional columns** (repo template includes these for bookkeeping; loader does not require them): `trial_number`, `shape`, `primary_context`, `secondary_context` — **`primary_context` / `secondary_context`** may also appear under legacy names `strong_context` / `neutral_context`.
- **Typical header order** in the shipped template: `trial_number`, `shape`, `shape_path`, `primary_context`, `secondary_context`, `context1`, `context1_image`, `context2`, `context2_image`, `variant`.
- **Paths:** `shape_path`, `context1_image`, and `context2_image` may be absolute or relative paths resolved under **`STIMULI/`** (e.g. **`shapes/foo.bmp`**, **`contexts/bar.png`** — see shipped template). The script normalizes `Shapes`/`Contexts` in absolute paths to on-disk `shapes`/`contexts`; **prefer lowercase repo-relative paths** so edits survive moves and case-sensitive filesystems (Linux).
- **What the code reads:** stimulus paths and `context1`/`context2` (A/B); `variant` plus primary/secondary labels are **logged only**. Presentation follows **`context*_image`** paths and button labels—not `variant`-driven branching.
- **Output alignment:** `phase2_*.csv` rows match template rows in order (trial 1…N). Onset columns mirror **`ttl_log_*`** (see **`csv_documentation.md`**).

---

## Timing (Stimulus Durations)

**Source of truth:** `context_shape_task.py` module constants (names ending in `_SEC`; e.g. `PHASE2_OBJECT_QUESTION_DURATION_SEC`, `PHASE_GRID_PREVIEW_SEC`, `PHASE13_BEFORE_GRID_MIN_SEC`, `TRAINING_DEMO_SCREEN_EXTRA_SEC` adds time on scripted training-demo screens only — real Phase 2 trials still use `PHASE2_SEGMENT_SEC` / `PHASE2_OBJECT_QUESTION_DURATION_SEC`). Phase 2 transitions from each **task object** epoch to **`PHASE2_OBJECT_QUESTION_TEXT`** (default **"What is the object?"**) with **no** intervening blank (`PHASE2_SEGMENT_SEC` still controls context/object display length only). **Tutorial fallback:** `TUTORIAL_FB_SHAPE_PREFLASH_SEC` — steps **3–4** only (brief new-shape flash on empty canvas before isolate). `TUTORIAL_FB_TARGET_ANCHORS_PREVIEW_SEC` — previously placed shapes visible on target epoch **before** halo/click (moving item still hidden). `TUTORIAL_FB_CURSOR_BEFORE_PLACEMENT_REVEAL_SEC` — light-blue **double halo** at empty placement before steelblue click + reveal on steps **2–4** fallback (isolate **center** epoch has **no** expanding steelblue ring).

**Phase 2 object-question screen:** Centered **`TextStim`** with **`PHASE2_OBJECT_QUESTION_TEXT`** (tutorial adds demo subtitles underneath). Durations **`PHASE2_OBJECT_QUESTION_DURATION_SEC`** (trials) and **`PHASE2_TUTORIAL_OBJECT_QUESTION_SEC`** (tutorial).

### Tutorial (fallback)

Durations below; **verbatim subtitles and transition:** **`script.md`** (Tutorial). Steps **2–4:** **`TUTORIAL_FB_CLICK_CENTER_SEC` + `TUTORIAL_FB_CLICK_TARGET_SEC`** each; steps **3–4** add **`TUTORIAL_FB_SHAPE_PREFLASH_SEC`** before center. Within **`TUTORIAL_FB_CLICK_TARGET_SEC`**: **`TUTORIAL_FB_TARGET_ANCHORS_PREVIEW_SEC`** (anchors-only) + halo + click + reveal + hold. **`tutorial_fallback_step{n}_*`** TTLs: **`csv_documentation.md`**.

**Presentation:** **Step 1:** Intro subtitle + **all three** shapes **together** for **`TUTORIAL_FB_OVERVIEW_SEC`** at **spread** overview positions (**`ov_sq`**, **`ov_red`**, **`ov_green`** in code — not overlapping). **Center (steps 2–4):** **only** moving object — **no** expanding steelblue ring. **Target:** anchors (+ subtitle) **`TUTORIAL_FB_TARGET_ANCHORS_PREVIEW_SEC`** with moving shape **hidden** and **no cursor**; **then** light-blue halo + steelblue expanding ring + **cursor** at **empty** **`end_pos`** (**moving shape hidden**); **then** shape at **final** coords + hold — totals **`TUTORIAL_FB_CLICK_TARGET_SEC`**. **Steps 3–4:** **`TUTORIAL_FB_SHAPE_PREFLASH_SEC`** on empty canvas; then center isolate (placed objects **not** drawn); then target as above. Demo **final positions** use staggered **y**. Black **cursor**: **triangle** + **narrow tail** along bisector (**`_make_tutorial_cursor`**). **Preflash** + **center** + anchor preview: **no cursor**. **Step 2** subtitle = **`PHASE13_CLICK_ENTER_INSTRUCTION`**; steps **3–4** grouping narrative (**`script.md`**).

| Step | Duration | Content (summary) |
|------|----------|-------------------|
| 1 | **4** s (`TUTORIAL_FB_OVERVIEW_SEC` = 2.5 s + `TRAINING_DEMO_SCREEN_EXTRA_SEC`) | Intro subtitle + **all three shapes at once** (spread overview positions) |
| 2 | **6** s total | Red square; subtitle **`PHASE13_CLICK_ENTER_INSTRUCTION`** |
| 3 | **≈6.4** s (`TUTORIAL_FB_SHAPE_PREFLASH_SEC` + center + target) | Red circle joins cluster; grouping subtitle (**`script.md`**) |
| 4 | **≈6.4** s (`TUTORIAL_FB_SHAPE_PREFLASH_SEC` + center + target) | Green circle to right group; grouping subtitle (**`script.md`**) |
| 5a | **4.5** s | Color-group summary (outline **circles** around reds vs green; centers follow staggered placements) |
| 5b | **5.5** s | Spectrum / proximity subtitle |
| 6 | **8.5** s | **`PHASE13_CLICK_ENTER_INSTRUCTION`** (same as **`phase1_instr3`** / trial hint) *(optional “large spread” line commented out in code)* |

### Phase 1

| Event | Duration |
|-------|----------|
| Before grid (`phase1_before_grid`) | Min **`PHASE13_BEFORE_GRID_MIN_SEC`** (**1.5** s) before **Enter** registers; copy **`script.md`** |
| Grid (`ShapeGrid_4x4_bmp.png`) | `PHASE_GRID_PREVIEW_SEC` (5 s); large centered grid + **miniature** same PNG bottom-right |
| Fixation (cross) | `PHASE_FIXATION_CROSS_SEC` (1 s); cross + **miniature** grid bottom-right |
| Task object display (before clickable) | `SHAPE_STATIC_PREVIEW_SEC` (1 s); **miniature** `ShapeGrid_4x4_bmp.png` bottom-right (same as placement) |
| Click-to-place | Participant-paced; gray hint matches **`phase1_instr3`**: **"Click where you want to place each object, then press Enter to confirm."** At least one click per object, then Enter. Miniature full grid in bottom-right for entire sorting block (same inset as preview) |

### Phase 2 Tutorial

**Instructions before the demo (**`phase2_questions`** … **`phase2_instr4`**):** verbatim on-screen copy in **`script.md`** (**Phase 2 — Context incorporation**). The timed spoken-cue screen uses **`PHASE2_OBJECT_QUESTION_TEXT`** in **`context_shape_task.py`** (editable; default **"What is the object?"**).

| Event | Duration |
|-------|----------|
| Intro (`phase2_tutorial_intro`) | Min **`PHASE2_INSTR5_MIN_SEC`** (5 s) before Enter; on-screen copy is the single sentence **"Watch this demo before you start the task!"** (also in **`script.md`**) |
| Fixation | `PHASE2_TUTORIAL_FIXATION_SEC` (2 s); main trials remain `PHASE2_FIXATION_PRE_TRIAL_SEC` |
| Context 1 (**`practice1.png`**, SPACE) | `PHASE2_TUTORIAL_SEGMENT_SEC` (2.5 s); main trials: `PHASE2_SEGMENT_SEC`; **same square framing as trials** (center cover crop) |
| Task object (blue circle) | `PHASE2_TUTORIAL_SEGMENT_SEC` |
| Object question (**`PHASE2_OBJECT_QUESTION_TEXT`**) + demo hint (PLANET) | `PHASE2_TUTORIAL_OBJECT_QUESTION_SEC` (3.5 s); main trials: `PHASE2_OBJECT_QUESTION_DURATION_SEC` (**immediately** after object) |
| Context 2 (**`practice2.png`**, CIRCUS) | `PHASE2_TUTORIAL_SEGMENT_SEC` |
| Task object 2 | `PHASE2_TUTORIAL_SEGMENT_SEC` |
| Object question + demo hint (BALL) | `PHASE2_TUTORIAL_OBJECT_QUESTION_SEC` |
| Choice preview then highlight | **`PHASE2_TUTORIAL_QUESTION_PREVIEW_SEC`** (**3** s = 1.5 + `TRAINING_DEMO_SCREEN_EXTRA_SEC`): prompt **"Which context fits best? Use the left/right keys to choose."** with SPACE (left) / CIRCUS (right) buttons, no selection shown. Then **`PHASE2_TUTORIAL_HIGHLIGHT_FEEDBACK_SEC`** (**2.5** s = 1.0 + `TRAINING_DEMO_SCREEN_EXTRA_SEC`): **right** button (CIRCUS / second practice context) drawn as selected (steel blue), subtitle **"You might say 'CIRCUS' (right key) is the better context"**. TTL labels: **`csv_documentation.md`** (`phase2_tutorial_question_*`, `phase2_tutorial_demo_select_*`). |
| Post-blank | **`PHASE2_TUTORIAL_POST_BLANK_SEC`** (**4.5** s = 3.0 + `TRAINING_DEMO_SCREEN_EXTRA_SEC`) |

### Phase 2 Trials (per trial)

| Event | Duration |
|-------|----------|
| Fixation | `PHASE2_FIXATION_PRE_TRIAL_SEC` (0.5 s) |
| Context 1 | 1 s (`PHASE2_SEGMENT_SEC`); **centered square**, center **cover** crop (same size all trials) |
| Task object | 1 s (`PHASE2_SEGMENT_SEC`); object-question screen follows **without** intervening blank |
| Object question (`PHASE2_OBJECT_QUESTION_TEXT`) | `PHASE2_OBJECT_QUESTION_DURATION_SEC` (2 s) |
| Context 2 | 1 s (`PHASE2_SEGMENT_SEC`); same square as context 1 |
| Task object 2 | 1 s (`PHASE2_SEGMENT_SEC`); second object-question follows **without** intervening blank |
| Object question 2 | `PHASE2_OBJECT_QUESTION_DURATION_SEC` (2 s) |
| Question | Participant-paced; prompt and keys — **`script.md`**; **TTL / RT** — **`csv_documentation.md`**. |
| ITI (blank) | `PHASE2_TRIAL_ITI_SEC` (0.5 s); TTL **`phase2_trial_iti_onset`** / **`phase2_trial_iti_offset`** after **`phase2_question_offset`** (**`csv_documentation.md`**) |

**Fixation → context 1:** The fixation epoch is **`PHASE2_FIXATION_PRE_TRIAL_SEC`** (0.5 s), but the transition to context 1 is **not** immediate after fixation ends: Pillow center-crop work for the context adds a variable **~200–400 ms** before the first frame of context 1. **`phase2_*.csv`** **`context1_onset_ttl`** (and **`phase2_context1_onset`** in **`ttl_log_*`**) reflect the true onset. For neural alignment, use those timestamps directly rather than **fixation onset + 0.5 s** — see **`csv_documentation.md`** (Phase 2 CSV).

### Phase 3

| Event | Duration |
|-------|----------|
| Before grid (`phase3_before_grid`) | Min **`PHASE13_BEFORE_GRID_MIN_SEC`** (**1.5** s) before **Enter**; copy **`script.md`** |
| Grid (`ShapeGrid_4x4_bmp.png`) | `PHASE_GRID_PREVIEW_SEC`; large + miniature bottom-right (same as Phase 1) |
| Fixation (cross) | `PHASE_FIXATION_CROSS_SEC`; cross + miniature bottom-right |
| Task object display (before clickable) | `SHAPE_STATIC_PREVIEW_SEC` (1 s); miniature grid bottom-right (same as Phase 1) |
| Click-to-place | Same wording as Phase 1 (**`phase3_instruction2c`** + gray hint): **"Click where you want to place each object, then press Enter to confirm."** At least one click per object, then Enter. Miniature full grid in bottom-right for entire sorting block |

### Other

| Event | Duration |
|-------|----------|
| Thank-you screen | `THANKS_SCREEN_SEC` (2 s) |
| Break (every 16 Phase 2 trials) | Participant-paced |
| Enter-to-continue instruction screens | Participant-paced; copy **`script.md`** |
| Debrief (after Phase 3 sort) | Participant-paced; Yes/No layout aligned with Phase 2 choice screen (**`script.md`**); **`phase3_debrief_*`** in **`csv_documentation.md`** |

---

## Trial order, mapping, randomization

| Phase | Selection | Ground truth / mapping |
|-------|-----------|------------------------|
| **1** | `random.shuffle(get_shape_paths())`; if first item is alphabetically first task shape (`ball_slope.bmp` default), rotate it to end | Clicks → `(x,y)`; row/col from index in sorted 4×4 list (same order as **`ShapeGrid_4x4_bmp.png`**). |
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
