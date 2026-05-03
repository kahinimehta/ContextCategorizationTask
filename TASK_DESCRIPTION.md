# Context Shape Task — Timings & Key Details

All durations from `context_shape_task.py` constants. Verbatim screen copy: `script.md`. TTL triggers + CSV schemas: `csv_documentation.md`.

---

## Tutorial (Animated Fallback)

`TRAINING_DEMO_SCREEN_EXTRA_SEC = 1.5 s` added to every timed tutorial screen. Real Phase 2 trials unaffected.

| Step | Duration | Notes |
|------|----------|-------|
| 1 — Overview | **4.0 s** (`TUTORIAL_FB_OVERVIEW_SEC` = 2.5 + 1.5) | All three shapes at spread positions simultaneously |
| 2 — Red square | **6.0 s** (`TUTORIAL_FB_CLICK_CENTER_SEC` 2.5 + `TUTORIAL_FB_CLICK_TARGET_SEC` 3.5) | Subtitle = `PHASE13_CLICK_ENTER_INSTRUCTION` (only appearance in fallback) |
| 3 — Red circle | **≈6.4 s** (`TUTORIAL_FB_SHAPE_PREFLASH_SEC` 0.38 + 2.5 + 3.5) | Grouping subtitle; preflash on empty canvas before center isolate |
| 4 — Green circle | **≈6.4 s** (same as step 3) | Grouping subtitle; preflash on empty canvas before center isolate |
| 5a — Color-group summary | **4.5 s** (`TUTORIAL_FB_STEP5A_SEC` = 3.0 + 1.5) | Outline circles around reds vs green |
| 5b — Proximity subtitle | **5.5 s** (`TUTORIAL_FB_STEP5B_SEC` = 4.0 + 1.5) | |

**Within each target epoch (`TUTORIAL_FB_CLICK_TARGET_SEC`):** `TUTORIAL_FB_TARGET_ANCHORS_PREVIEW_SEC` (0.38 s) anchors-only, no cursor → light-blue double halo (`TUTORIAL_FB_CURSOR_BEFORE_PLACEMENT_REVEAL_SEC` 0.40 s) → steelblue click pulse (`TUTORIAL_FB_CURSOR_CLICK_FEEDBACK_SEC` 0.14 s) → shape reveal + hold. Moving shape hidden until reveal. No cursor on preflash / center / anchor preview.

---

## Phase 1

| Event | Duration |
|-------|----------|
| `phase1_before_grid` | Min **1.5 s** (`PHASE13_BEFORE_GRID_MIN_SEC`) before Enter registers |
| Grid preview (`ShapeGrid_4x4_bmp.png`) | **5 s** (`PHASE_GRID_PREVIEW_SEC`); large + miniature bottom-right |
| Fixation cross | **1 s** (`PHASE_FIXATION_CROSS_SEC`); miniature grid bottom-right |
| Per-object isolate preview | **1 s** (`SHAPE_STATIC_PREVIEW_SEC`); miniature grid bottom-right |
| Click-to-place | Participant-paced; at least one click then Enter per object |

---

## Phase 2 Tutorial

| Event | Duration |
|-------|----------|
| `phase2_tutorial_intro` ("Watch this demo…") | Min **5 s** (`PHASE2_INSTR5_MIN_SEC`) before Enter |
| Fixation | **2.0 s** (`PHASE2_TUTORIAL_FIXATION_SEC` = 0.5 + 1.5) |
| Context 1 / Context 2 | **2.5 s** each (`PHASE2_TUTORIAL_SEGMENT_SEC` = 1.0 + 1.5) |
| Task object (blue circle) ×2 | **2.5 s** each |
| Object question + demo hint ×2 | **3.5 s** each (`PHASE2_TUTORIAL_OBJECT_QUESTION_SEC` = 2.0 + 1.5) |
| Choice preview (both buttons neutral) | **3.0 s** (`PHASE2_TUTORIAL_QUESTION_PREVIEW_SEC` = 1.5 + 1.5) |
| Highlight (CIRCUS selected) | **2.5 s** (`PHASE2_TUTORIAL_HIGHLIGHT_FEEDBACK_SEC` = 1.0 + 1.5) |
| Post-blank | **4.5 s** (`PHASE2_TUTORIAL_POST_BLANK_SEC` = 3.0 + 1.5) |

---

## Phase 2 Trials (per trial)

| Event | Duration |
|-------|----------|
| Fixation | **0.5 s** (`PHASE2_FIXATION_PRE_TRIAL_SEC`) |
| Context 1 | **1.0 s** (`PHASE2_SEGMENT_SEC`) |
| Task object | **1.0 s** |
| Object question (`PHASE2_OBJECT_QUESTION_TEXT`) | **2.0 s** (`PHASE2_OBJECT_QUESTION_DURATION_SEC`); no blank between object and question |
| Context 2 | **1.0 s** |
| Task object 2 | **1.0 s** |
| Object question 2 | **2.0 s** |
| Choice screen | Participant-paced |
| ITI (blank) | **0.5 s** (`PHASE2_TRIAL_ITI_SEC`) |

**Note:** Pillow cover-crop adds ~200–400 ms between fixation offset and context 1 onset. Use `context1_onset_ttl` directly for neural alignment, not fixation onset + 0.5 s.

Break every 16 trials (participant-paced).

---

## Phase 3

Identical timing to Phase 1. `phase3_before_grid` min **1.5 s** before Enter. Same grid/fixation/isolate/click-to-place structure.

---

## Other

| Event | Duration |
|-------|----------|
| Thank-you screen | **2 s** (`THANKS_SCREEN_SEC`) |
| All Enter-to-continue instruction screens | Participant-paced |
| Debrief (3 questions, after Phase 3) | Participant-paced |
