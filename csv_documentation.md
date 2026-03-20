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

Trigger codes equal event labels (strings). Use these for EEG/fMRI analysis. Phase 1 & 3: **Click** to move, **Enter** to submit. Each click logged as `click_place` (trial_info: click=N).

| Trigger code | Phase | Description |
|--------------|-------|-------------|
| `participant_name_onset` | — | Participant name prompt appeared |
| `participant_name_offset` | — | Participant pressed Enter on name |
| *(Instruction screens: onset, enter, offset)* | — | All Enter-to-continue screens log onset (appeared), enter (keypress), offset (transition) |
| `experiment_start` | — | Experiment started (trial_info: participant=…) |
| `experiment_end` | — | Experiment ended (trial_info: participant=…) |
| `welcome_onset` | — | Welcome screen appeared |
| `welcome_enter` | — | Enter pressed |
| `welcome_offset` | — | Screen transition |
| `tutorial_video_onset` | — | Tutorial video started |
| `tutorial_video_offset` | — | Tutorial video ended |
| `tutorial_fallback_onset` | — | Animated fallback started (trial_info: step=1, 2, 3, 4, 5a, 5b, 6) |
| `tutorial_fallback_offset` | — | Animated fallback step ended |
| `tutorial_debrief_onset` | — | "We sorted by shape" screen appeared |
| `tutorial_debrief_enter` | — | Enter pressed |
| `tutorial_debrief_offset` | — | Screen transition |
| `tutorial_transition_onset` | — | "Let's get started" screen appeared |
| `tutorial_transition_enter` | — | Enter pressed |
| `tutorial_transition_offset` | — | Screen transition |
| `phase1_instr1_onset` | 1 | Phase 1 instruction screen 1 appeared |
| `phase1_instr1_enter` | 1 | Enter pressed |
| `phase1_instr1_offset` | 1 | Screen transition |
| `phase1_instr2_onset` | 1 | Phase 1 instruction screen 2 appeared |
| `phase1_instr2_enter` | 1 | Enter pressed |
| `phase1_instr2_offset` | 1 | Screen transition |
| `phase1_instr3_onset` | 1 | Phase 1 instruction screen 3 appeared |
| `phase1_instr3_enter` | 1 | Enter pressed |
| `phase1_instr3_offset` | 1 | Screen transition |
| `phase1_before_grid_onset` | 1 | "You will see 16 shapes..." appeared |
| `phase1_before_grid_enter` | 1 | Enter pressed |
| `phase1_before_grid_offset` | 1 | Screen transition |
| `phase1_grid_onset` | 1 | Shape grid display started |
| `phase1_grid_offset` | 1 | Shape grid display ended |
| `phase1_fixation_onset` | 1 | Fixation cross onset |
| `phase1_fixation_offset` | 1 | Fixation cross ended |
| `phase1_instruction2a_onset` | 1 | "Group each" instruction appeared |
| `phase1_instruction2a_enter` | 1 | Enter pressed |
| `phase1_instruction2a_offset` | 1 | Screen transition |
| `phase1_instruction2b_onset` | 1 | "Click to place" instruction appeared |
| `phase1_instruction2b_enter` | 1 | Enter pressed |
| `phase1_instruction2b_offset` | 1 | Screen transition |
| `phase1_instruction2c_onset` | 1 | "Once you've submitted..." instruction appeared |
| `phase1_instruction2c_enter` | 1 | Enter pressed |
| `phase1_instruction2c_offset` | 1 | Screen transition |
| `phase1_stimulus_onset` | 1 | Shape shown (trial_info: trial=N) |
| `phase1_stimulus_offset` | 1 | Shape display ended, clickable |
| `phase1_click_place` | 1 | Each click to move shape (trial_info: trial=N, shape=…, click=N) |
| `phase1_enter_submit` | 1 | Enter to submit (trial_info: trial=N, shape=…) |
| `phase2_instr1_onset` | 2 | Phase 2 instruction screen 1 appeared |
| `phase2_instr1_enter` | 2 | Enter pressed |
| `phase2_instr1_offset` | 2 | Screen transition |
| `phase2_instr2_onset` | 2 | Phase 2 instruction screen 2 appeared |
| `phase2_instr2_enter` | 2 | Enter pressed |
| `phase2_instr2_offset` | 2 | Screen transition |
| `phase2_instr3_onset` | 2 | Phase 2 instruction screen 3 appeared |
| `phase2_instr3_enter` | 2 | Enter pressed |
| `phase2_instr3_offset` | 2 | Screen transition |
| `phase2_instr4_onset` | 2 | "Do your best since you will be recorded..." appeared |
| `phase2_instr4_enter` | 2 | Enter pressed |
| `phase2_instr4_offset` | 2 | Screen transition |
| `phase2_instr5_onset` | 2 | "You can also re-use answers" appeared |
| `phase2_instr5_enter` | 2 | Enter pressed |
| `phase2_instr5_offset` | 2 | Screen transition |
| `phase2_instr6_onset` | 2 | "Here's an example" appeared |
| `phase2_instr6_enter` | 2 | Enter pressed |
| `phase2_instr6_offset` | 2 | Screen transition |
| `phase2_tutorial_intro_onset` | 2 | Tutorial intro appeared |
| `phase2_tutorial_intro_enter` | 2 | Enter pressed |
| `phase2_tutorial_intro_offset` | 2 | Screen transition |
| `phase2_tutorial_fixation_onset` | 2 | Tutorial fixation |
| `phase2_tutorial_context1_onset` | 2 | Tutorial context 1 |
| `phase2_tutorial_shape_onset` | 2 | Tutorial shape |
| `phase2_tutorial_blank_onset` | 2 | Tutorial blank |
| `phase2_tutorial_reddot_onset` | 2 | Tutorial red dot + PLANET |
| `phase2_tutorial_context2_onset` | 2 | Tutorial context 2 |
| `phase2_tutorial_shape2_onset` | 2 | Tutorial shape 2 |
| `phase2_tutorial_reddot2_onset` | 2 | Tutorial red dot + BALL |
| `phase2_tutorial_reddot2_offset` | 2 | Tutorial red dot 2 ended |
| `phase2_tutorial_blank2_onset` | 2 | Tutorial blank (between shape2 and reddot2) |
| `phase2_tutorial_blank2_offset` | 2 | Tutorial blank 2 ended |
| `phase2_tutorial_question_onset` | 2 | Tutorial question |
| `phase2_tutorial_question_offset` | 2 | Tutorial question ended (after SPACE demo) |
| `phase2_tutorial_response` | 2 | Tutorial response (SPACE) |
| `phase2_tutorial_post_blank_onset` | 2 | Tutorial post-response blank |
| `phase2_tutorial_post_blank_offset` | 2 | Tutorial post-response blank ended |
| `phase2_ready_onset` | 2 | "Ready to try" screen appeared |
| `phase2_ready_enter` | 2 | Enter pressed |
| `phase2_ready_offset` | 2 | Screen transition |
| `phase2_fixation_onset` | 2 | Fixation before trial |
| `phase2_fixation_offset` | 2 | Fixation ended |
| `phase2_context1_onset` | 2 | Context 1 image onset |
| `phase2_context1_offset` | 2 | Context 1 offset |
| `phase2_shape_onset` | 2 | Shape onset |
| `phase2_shape_offset` | 2 | Shape offset |
| `phase2_blank1_onset` | 2 | Blank between shape and red dot (trial_info: trial=N) |
| `phase2_blank1_offset` | 2 | Blank 1 ended |
| `phase2_reddot_onset` | 2 | Red dot + category label onset |
| `phase2_reddot_offset` | 2 | Red dot offset |
| `phase2_context2_onset` | 2 | Context 2 image onset |
| `phase2_context2_offset` | 2 | Context 2 offset |
| `phase2_shape2_onset` | 2 | Shape (2nd) onset |
| `phase2_shape2_offset` | 2 | Shape (2nd) offset |
| `phase2_blank2_onset` | 2 | Blank between shape2 and red dot 2 (trial_info: trial=N) |
| `phase2_blank2_offset` | 2 | Blank 2 ended |
| `phase2_reddot2_onset` | 2 | Red dot 2 onset |
| `phase2_reddot2_offset` | 2 | Red dot 2 offset |
| `phase2_question_onset` | 2 | "Which context fits better?" onset |
| `phase2_response` | 2 | Participant clicked category A or B |
| `phase2_question_offset` | 2 | Question screen ended (after response) |
| `phase2_trial_iti_onset` | 2 | Inter-trial interval blank (trial_info: trial=N) |
| `phase2_trial_iti_offset` | 2 | ITI ended |
| `phase2_break_onset` | 2 | Break screen appeared (every 12 trials) |
| `phase2_break_enter` | 2 | Enter pressed |
| `phase2_break_offset` | 2 | Screen transition |
| `phase3_instr1_onset` | 3 | Phase 3 instruction screen 1 appeared |
| `phase3_instr1_enter` | 3 | Enter pressed |
| `phase3_instr1_offset` | 3 | Screen transition |
| `phase3_instr2_onset` | 3 | Phase 3 instruction screen 2 appeared |
| `phase3_instr2_enter` | 3 | Enter pressed |
| `phase3_instr2_offset` | 3 | Screen transition |
| `phase3_instr3_onset` | 3 | Phase 3 instruction screen 3 appeared |
| `phase3_instr3_enter` | 3 | Enter pressed |
| `phase3_instr3_offset` | 3 | Screen transition |
| `phase3_instr4_onset` | 3 | Phase 3 instruction screen 4 appeared |
| `phase3_instr4_enter` | 3 | Enter pressed |
| `phase3_instr4_offset` | 3 | Screen transition |
| `phase3_instr5_onset` | 3 | "Once you've submitted..." instruction appeared |
| `phase3_instr5_enter` | 3 | Enter pressed |
| `phase3_instr5_offset` | 3 | Screen transition |
| `phase3_stimulus_onset` | 3 | Shape shown (trial_info: trial=N) |
| `phase3_stimulus_offset` | 3 | Shape display ended, clickable |
| `phase3_click_place` | 3 | Each click to move shape (trial_info: trial=N, shape=…, click=N) |
| `phase3_enter_submit` | 3 | Enter to submit (trial_info: trial=N, shape=…) |
| `phase3_debrief_onset` | 3 | Debrief question onset |
| `phase3_debrief_response` | 3 | Participant clicked Yes/No |
| `phase1_placements_saved` | 1 | Phase 1 placement image saved (trial_info: filename) |
| `phase3_placements_saved` | 3 | Phase 3 placement image saved (trial_info: filename) |
| `summary_saved` | — | Summary CSV written (trial_info: filename) |
| `thanks_onset` | — | Thank-you screen appeared |
| `thanks_offset` | — | Thank-you screen ended |

---

## Phase 1 CSV (phase1_{participant}_{datetime}.csv)

Per-shape data from the bottom-up shape classification phase.

| Column | Type | Description |
|--------|------|-------------|
| `shape_path` | String | Full path to the shape image file |
| `final_x` | Float | Final x position in screen coordinates (height units) |
| `final_y` | Float | Final y position in screen coordinates (height units) |
| `rt` | Float | Reaction time from clickable onset to last click (seconds). If no clicks, time to Enter. |
| `stimulus_onset_ttl` | Float | TTL timestamp at stimulus onset |
| `stimulus_offset_ttl` | Float | TTL timestamp at stimulus offset |
| `click_ttl` | Float | TTL timestamp at first click to place |
| `all_click_ttl` | String | Semicolon-separated timestamps of all clicks (Unix) |
| `submit_ttl` | Float | TTL timestamp when participant pressed Enter to submit |

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
| `trial_variant` | String | original, context_swapped, control_context, control_context_swapped |
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

Post–Phase 3 questionnaire (3 questions). One row per question.

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
3. "After thinking about how shapes might fit in different environments, did you find yourself interpreting the shapes differently when you sorted them the second time?"

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
| `phase3_euclidean_distances` | String | Pairwise distances (format: `i-j:dist;...`). Smaller = shapes grouped more similarly (closer categorically). |

---

## File Saving

- **Location**: `../LOG_FILES/`
- **Filenames**: `{basename}_{participant}_{YYYYMMDD_HHMMSS}.csv` or `.png`
- **Test participants**: Name contains "test" → no files written (TTL log deleted)
