# CSV Variables Documentation

Complete reference for all CSV outputs from the ContextShape Task. See `script.md` for experimenter instructions (including ELI5/simple versions for explaining to participants).

## TTL Log (ttl_log_{participant}_{datetime}.csv)

Every TTL trigger is logged with timestamp, trigger code, event label, and trial info. Written incrementally as each event occurs.

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | Float (Unix) | Time when TTL fired |
| `trigger_code` | String | Event identifier (same as event_label unless overridden) |
| `event_label` | String | Human-readable event name |
| `trial_info` | String | Optional trial metadata (e.g., trial=3, shape=Shape_0.10_1.70.png) |

**Event types**: See TTL Trigger Mapping below.

---

## TTL Trigger Mapping

Trigger codes equal event labels (strings). Use these for EEG/fMRI analysis. Phase 1 & 3 use **click-to-place**; placement is logged as `click_place`.

| Trigger code | Phase | Description |
|--------------|-------|-------------|
| `welcome` | — | Welcome screen onset |
| `welcome_enter` | — | Participant pressed Enter on welcome |
| `tutorial_video_onset` | — | Tutorial video started |
| `tutorial_video_offset` | — | Tutorial video ended |
| `tutorial_fallback_onset` | — | Animated fallback started (trial_info: step=1–6) |
| `tutorial_fallback_offset` | — | Animated fallback step ended |
| `tutorial_debrief` | — | "We sorted by shape" screen |
| `tutorial_transition` | — | "Let's get started" screen |
| `phase1_instructions` | 1 | Phase 1 instructions onset |
| `phase1_grid_onset` | 1 | Shape grid display started |
| `phase1_grid_offset` | 1 | Shape grid display ended |
| `phase1_fixation_onset` | 1 | Fixation cross onset |
| `phase1_fixation_offset` | 1 | Fixation cross ended |
| `phase1_instruction2` | 1 | "Click to place" instruction onset |
| `phase1_stimulus_onset` | 1 | Shape shown (trial_info: trial=N) |
| `phase1_stimulus_offset` | 1 | Shape display ended, clickable |
| `phase1_click_place` | 1 | **Participant clicked to place shape** (trial_info: trial=N, shape=…) |
| `phase2_instructions` | 2 | Phase 2 instructions onset |
| `phase2_tutorial_*` | 2 | Tutorial: fixation, context1, shape, blank, reddot, context2, shape2, question, response |
| `phase2_ready` | 2 | "Ready to try" screen |
| `phase2_fixation_onset` | 2 | Fixation before trial |
| `phase2_fixation_offset` | 2 | Fixation ended |
| `phase2_context1_onset` | 2 | Context 1 image onset |
| `phase2_context1_offset` | 2 | Context 1 offset |
| `phase2_shape_onset` | 2 | Shape onset |
| `phase2_shape_offset` | 2 | Shape offset |
| `phase2_reddot_onset` | 2 | Red dot + category label onset |
| `phase2_reddot_offset` | 2 | Red dot offset |
| `phase2_context2_onset` | 2 | Context 2 image onset |
| `phase2_context2_offset` | 2 | Context 2 offset |
| `phase2_shape2_onset` | 2 | Shape (2nd) onset |
| `phase2_shape2_offset` | 2 | Shape (2nd) offset |
| `phase2_reddot2_onset` | 2 | Red dot 2 onset |
| `phase2_reddot2_offset` | 2 | Red dot 2 offset |
| `phase2_question_onset` | 2 | "Which context fits better?" onset |
| `phase2_response` | 2 | Participant clicked category A or B |
| `phase2_break_onset` | 2 | Break screen (every 12 trials) |
| `phase3_instructions` | 3 | Phase 3 instructions onset |
| `phase3_stimulus_onset` | 3 | Shape shown (trial_info: trial=N) |
| `phase3_stimulus_offset` | 3 | Shape display ended, clickable |
| `phase3_click_place` | 3 | **Participant clicked to place shape** (trial_info: trial=N, shape=…) |
| `phase3_debrief_onset` | 3 | Debrief question onset |
| `phase3_debrief_response` | 3 | Participant clicked Yes/No |

---

## Phase 1 CSV (phase1_{participant}_{datetime}.csv)

Per-shape data from the bottom-up shape classification phase.

| Column | Type | Description |
|--------|------|-------------|
| `shape_path` | String | Full path to the shape image file |
| `final_x` | Float | Final x position in screen coordinates (height units) |
| `final_y` | Float | Final y position in screen coordinates (height units) |
| `rt` | Float | Reaction time from clickable onset to click (seconds) |
| `stimulus_onset_ttl` | Float | TTL timestamp at stimulus onset |
| `stimulus_offset_ttl` | Float | TTL timestamp at stimulus offset |
| `click_ttl` | Float | TTL timestamp when participant clicked to place |
| `submit_ttl` | Float | TTL timestamp at placement (same as click_ttl) |

---

## Phase 2 CSV (phase2_{participant}_{datetime}.csv)

Per-trial data from the top-down context incorporation phase (48 trials).

**Design:** Each shape is associated with exactly 2 context categories (A and B). Four trials per shape: (1) A then B, (2) B then A, (3) A-control then B-control, (4) B-control then A-control. Control = different image from same category (*_02s.jpg vs *_01b.jpg). Each context *pair* (A,B) is unique to one shape, but the same context category can appear across shapes (e.g. BARK with shape 1 and shape 5 in different pairs).

| Column | Type | Description |
|--------|------|-------------|
| `trial` | Integer | Trial number (1–48) |
| `shape_path` | String | Full path to the shape image |
| `context_1_path` | String | Full path to first context image |
| `context_2_path` | String | Full path to second context image |
| `trial_variant` | String | original, context_swapped, control_context, control_context_swapped. Control variants use control images (different image from same category), not the exact same context. |
| `response` | String | Button clicked: category A or B (e.g., BARK, CLOUD) |
| `rt` | Float | Reaction time from question onset to button click (seconds) |
| `fixation_onset_ttl` | Float | TTL timestamp at fixation onset |
| `context1_onset_ttl` | Float | TTL timestamp at context 1 onset |
| `shape_onset_ttl` | Float | TTL timestamp at shape onset |
| `reddot_onset_ttl` | Float | TTL timestamp at red dot onset |
| `context2_onset_ttl` | Float | TTL timestamp at context 2 onset |
| `shape2_onset_ttl` | Float | TTL timestamp at shape 2 onset |
| `reddot2_onset_ttl` | Float | TTL timestamp at red dot 2 onset |
| `question_onset_ttl` | Float | TTL timestamp at question screen onset |
| `response_ttl` | Float | TTL timestamp at response button click |

---

## Phase 3 CSV (phase3_{participant}_{datetime}.csv)

Same structure as Phase 1. Per-shape data from the post-context shape reclassification phase. Shape order is randomized differently from Phase 1.

---

## Placement Images (phase1_placements_*.png, phase3_placements_*.png)

PNG images of final shape placements at the end of Phase 1 and Phase 3. White canvas with each shape drawn at its final (x, y) position. Saved only for non-test participants.

---

## Debrief CSV (debrief_{participant}_{datetime}.csv)

Post–Phase 3 questionnaire (2 questions). One row per question.

| Column | Type | Description |
|--------|------|-------------|
| `question` | Integer | Question number (1 or 2) |
| `question_text` | String | Full question text |
| `answer` | String | Participant response: "Yes" or "No" |
| `rt` | Float | Reaction time from question onset to button click (seconds) |
| `onset_ttl` | Float | TTL timestamp at question screen onset |
| `response_ttl` | Float | TTL timestamp at Yes/No button click |

**Questions:**
1. "Did you use the same grouping strategy as the first time you sorted these shapes?"
2. "Did the images associated with each shape you saw influence your grouping the second time around?"

---

## Summary CSV (summary_{participant}_{datetime}.csv)

Overall experiment summary.

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | String | Participant identifier |
| `total_task_time_seconds` | Float | Total duration from start to end |
| `shapegrid_width_px` | Integer | ShapeGrid_4x4.png pixel width |
| `shapegrid_height_px` | Integer | ShapeGrid_4x4.png pixel height |
| `grid_border_coords` | String | Grid border coordinates (if computed) |
| `per_shape_ground_truth` | String | Per-shape ground-truth: `Shape_X_Y.png:row=R,col=C,center_x=X,center_y=Y` (pipe-separated) |
| `scaling_factor` | String | Scaling factor used for display |
| `phase3_euclidean_distances` | String | Pairwise Euclidean distances between all Phase 3 final positions (format: `i-j:dist;...`). In layman terms: smaller distances mean shapes were placed closer together on screen, indicating they were grouped more similarly—i.e., how close the shapes are categorically to each other. |

---

## File Saving

- **Location**: `../LOG_FILES/` (relative to task root)
- **Filenames**: All CSVs and PNGs include date/time: `{basename}_{participant}_{YYYYMMDD_HHMMSS}.csv` or `.png`
  - Example: `phase1_john_20250318_143022.csv`, `phase1_placements_john_20250318_143022.png`, `ttl_log_john_20250318_143022.csv`
- **Placement images**: `phase1_placements_*.png` and `phase3_placements_*.png` saved at end of Phase 1 and Phase 3 (white canvas with shapes at final positions)
- **Incremental writes**: All CSVs are written row-by-row with flush to disk
- **Test participants**: If participant name contains "test" (case-insensitive), **no files are written**. All phase, debrief, summary, TTL log, and placement PNG files are skipped. Use this for practice runs.
