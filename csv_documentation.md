# CSV and TTL Documentation

Reference for all CSV outputs and TTL triggers. **Example files (repo root):** `README.md` (Data output → Example output). **Experimenter script:** `script.md`. **Technical spec:** `TASK_DESCRIPTION.md`.

## TTL Log (ttl_log_{participant}_{datetime}.csv)

Every TTL trigger is logged with timestamp, trigger code, event label, and trial info. Written incrementally as each event occurs. The file is initially created as `ttl_log_{datetime}.csv` (before participant name is known), then renamed to include the participant at task end.

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | Float (Unix) | Time when TTL fired |
| `trigger_code` | String | Event identifier (same as event_label unless overridden) |
| `event_label` | String | Human-readable event name |
| `trial_info` | String | Optional trial metadata (e.g., trial=3, shape=Shape_0_1.png) |

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
| `tutorial_fallback_step2_center_onset` | — | Step 2: shape at center (1 s) |
| `tutorial_fallback_step2_center_offset` | — | Step 2: center ended |
| `tutorial_fallback_step2_target_onset` | — | Step 2: shape at target (2 s) |
| `tutorial_fallback_step2_target_offset` | — | Step 2: target ended |
| `tutorial_fallback_step3_center_onset/offset` | — | Step 3: center phase |
| `tutorial_fallback_step3_target_onset/offset` | — | Step 3: target phase |
| `tutorial_fallback_step4_center_onset/offset` | — | Step 4: center phase |
| `tutorial_fallback_step4_target_onset/offset` | — | Step 4: target phase |
| `tutorial_transition_onset` | — | "Now that we've seen a demo... let's get started on your version!" screen appeared |
| `tutorial_transition_enter` | — | Enter pressed |
| `tutorial_transition_offset` | — | Screen transition |
| `phase1_questions_onset` | 1 | "If you have any questions, ask the experimenter now" appeared |
| `phase1_questions_enter` | 1 | Enter pressed |
| `phase1_questions_offset` | 1 | Screen transition |
| `phase1_instr1_onset` | 1 | Phase 1 instruction screen 1 appeared |
| `phase1_instr1_enter` | 1 | Enter pressed |
| `phase1_instr1_offset` | 1 | Screen transition |
| `phase1_instr2_onset` | 1 | Phase 1 instruction screen 2 appeared |
| `phase1_instr2_enter` | 1 | Enter pressed |
| `phase1_instr2_offset` | 1 | Screen transition |
| `phase1_instr3_onset` | 1 | "Group them into groups—not on a spectrum..." appeared |
| `phase1_instr3_enter` | 1 | Enter pressed |
| `phase1_instr3_offset` | 1 | Screen transition |
| `phase1_instr4_onset` | 1 | "Use as many groups as you need" appeared |
| `phase1_instr4_enter` | 1 | Enter pressed |
| `phase1_instr4_offset` | 1 | Screen transition |
| `phase1_before_grid_onset` | 1 | "You will now see 16 shapes..." appeared |
| `phase1_before_grid_enter` | 1 | Enter pressed |
| `phase1_before_grid_offset` | 1 | Screen transition |
| `phase1_grid_onset` | 1 | Shape grid display started |
| `phase1_grid_offset` | 1 | Shape grid display ended |
| `phase1_fixation_onset` | 1 | Fixation cross onset |
| `phase1_fixation_offset` | 1 | Fixation cross ended |
| `phase1_instruction2a_onset` | 1 | "Sort by where you'd expect to see the shapes" instruction appeared |
| `phase1_instruction2a_enter` | 1 | Enter pressed |
| `phase1_instruction2a_offset` | 1 | Screen transition |
| `phase1_instruction2c_onset` | 1 | "Click somewhere to place, then press Enter to submit. Once you've submitted..." instruction appeared |
| `phase1_instruction2c_enter` | 1 | Enter pressed |
| `phase1_instruction2c_offset` | 1 | Screen transition |
| `phase1_complete` | 1 | Phase 1 drag task finished (all shapes placed) |
| `phase1_stimulus_onset` | 1 | Shape shown (trial_info: trial=N, shape=*.bmp filename) |
| `phase1_stimulus_offset` | 1 | Shape display ended, clickable (trial_info: trial=N, shape=*.bmp) |
| `phase1_click_place` | 1 | Each click to move shape (trial_info: trial=N, shape=…, click=N) |
| `phase1_enter_submit` | 1 | Enter to submit (trial_info: trial=N, shape=…) |
| `phase2_questions_onset` | 2 | "If you have any questions, ask the experimenter now" appeared |
| `phase2_questions_enter` | 2 | Enter pressed |
| `phase2_questions_offset` | 2 | Screen transition |
| `phase2_instr1_onset` | 2 | "Now you'll see the shapes again, paired with different pictures or background contexts. Each shape appears with two context pictures." appeared |
| `phase2_instr1_enter` | 2 | Enter pressed |
| `phase2_instr1_offset` | 2 | Screen transition |
| `phase2_instr2_onset` | 2 | Phase 2 instruction: context → shape → red dot (see on-screen `phase2_instr2` in script) |
| `phase2_instr2_enter` | 2 | Enter pressed |
| `phase2_instr2_offset` | 2 | Screen transition |
| `phase2_instr2b_onset` | 2 | "When the red dot is on screen, say out loud what the shape could be... Then click which picture fits better. We need to hear you say it every time." appeared |
| `phase2_instr2b_enter` | 2 | Enter pressed |
| `phase2_instr2b_offset` | 2 | Screen transition |
| `phase2_instr3_onset` | 2 | "Do your best since you will be recorded... You will watch a demo before you have to do the task, so don't worry if this makes no sense yet." appeared |
| `phase2_instr3_enter` | 2 | Enter pressed |
| `phase2_instr3_offset` | 2 | Screen transition |
| `phase2_instr4_onset` | 2 | "You can also re-use answers, but try to be creative if you can." appeared |
| `phase2_instr4_enter` | 2 | Enter pressed |
| `phase2_instr4_offset` | 2 | Screen transition |
| `phase2_instr5_onset` | 2 | "Now let's watch a quick demo to help you understand how we work on this task" appeared (min 5 s) |
| `phase2_instr5_enter` | 2 | Enter pressed |
| `phase2_instr5_offset` | 2 | Screen transition |
| `phase2_tutorial_intro_onset` | 2 | Tutorial intro appeared |
| `phase2_tutorial_intro_enter` | 2 | Enter pressed |
| `phase2_tutorial_intro_offset` | 2 | Screen transition |
| `phase2_tutorial_fixation_onset` | 2 | Tutorial fixation onset |
| `phase2_tutorial_fixation_offset` | 2 | Tutorial fixation ended |
| `phase2_tutorial_context1_onset` | 2 | Tutorial context 1 onset |
| `phase2_tutorial_context1_offset` | 2 | Tutorial context 1 ended |
| `phase2_tutorial_shape_onset` | 2 | Tutorial shape onset |
| `phase2_tutorial_shape_offset` | 2 | Tutorial shape ended |
| `phase2_tutorial_blank_onset` | 2 | Tutorial blank onset |
| `phase2_tutorial_blank_offset` | 2 | Tutorial blank ended |
| `phase2_tutorial_reddot_onset` | 2 | Tutorial red dot + PLANET onset |
| `phase2_tutorial_reddot_offset` | 2 | Tutorial red dot ended |
| `phase2_tutorial_context2_onset` | 2 | Tutorial context 2 onset |
| `phase2_tutorial_context2_offset` | 2 | Tutorial context 2 ended |
| `phase2_tutorial_shape2_onset` | 2 | Tutorial shape 2 onset |
| `phase2_tutorial_shape2_offset` | 2 | Tutorial shape 2 ended |
| `phase2_tutorial_reddot2_onset` | 2 | Tutorial red dot + BALL |
| `phase2_tutorial_reddot2_offset` | 2 | Tutorial red dot 2 ended |
| `phase2_tutorial_blank2_onset` | 2 | Tutorial blank (between shape2 and reddot2) |
| `phase2_tutorial_blank2_offset` | 2 | Tutorial blank 2 ended |
| `phase2_tutorial_question_onset` | 2 | Tutorial question (SKY \| PETSHOP) |
| `phase2_tutorial_demo_select_onset` | 2 | Tutorial "You might select PETSHOP" demo appeared |
| `phase2_tutorial_demo_select_offset` | 2 | Tutorial demo select ended |
| `phase2_tutorial_question_offset` | 2 | Tutorial question ended (after demo selection) |
| `phase2_tutorial_response` | 2 | Demo choice (e.g. trial_info: PETSHOP) |
| `phase2_tutorial_post_blank_onset` | 2 | Tutorial post-response blank |
| `phase2_tutorial_post_blank_offset` | 2 | Tutorial post-response blank ended |
| `phase2_ready_onset` | 2 | "Ready to try this with some actual shapes and images?" screen appeared |
| `phase2_ready_enter` | 2 | Enter pressed |
| `phase2_ready_offset` | 2 | Screen transition |
| `phase2_before_trials_onset` | 2 | "Ask the experimenter now..." before Phase 2 trials appeared |
| `phase2_before_trials_enter` | 2 | Enter pressed |
| `phase2_before_trials_offset` | 2 | Screen transition |
| `phase2_fixation_onset` | 2 | Fixation before trial (trial_info: trial=N) |
| `phase2_fixation_offset` | 2 | Fixation ended (trial_info: trial=N) |
| `phase2_context1_onset` | 2 | Context 1 image onset (trial_info: trial=N, shape=*.bmp) |
| `phase2_context1_offset` | 2 | Context 1 offset (trial_info: trial=N) |
| `phase2_shape_onset` | 2 | Shape onset (trial_info: trial=N, shape=*.bmp) |
| `phase2_shape_offset` | 2 | Shape offset (trial_info: trial=N) |
| `phase2_blank1_onset` | 2 | Blank between shape and red dot (trial_info: trial=N) |
| `phase2_blank1_offset` | 2 | Blank 1 ended |
| `phase2_reddot_onset` | 2 | Red dot + "say out loud" (trial_info: trial=N, shape=*.bmp) |
| `phase2_reddot_offset` | 2 | Red dot offset (trial_info: trial=N) |
| `phase2_context2_onset` | 2 | Context 2 image onset (trial_info: trial=N, shape=*.bmp) |
| `phase2_context2_offset` | 2 | Context 2 offset (trial_info: trial=N) |
| `phase2_shape2_onset` | 2 | Shape (2nd) onset (trial_info: trial=N) |
| `phase2_shape2_offset` | 2 | Shape (2nd) offset (trial_info: trial=N) |
| `phase2_blank2_onset` | 2 | Blank between shape2 and red dot 2 (trial_info: trial=N) |
| `phase2_blank2_offset` | 2 | Blank 2 ended |
| `phase2_reddot2_onset` | 2 | Red dot 2 + "say out loud" (trial_info: trial=N, shape=*.bmp) |
| `phase2_reddot2_offset` | 2 | Red dot 2 offset (trial_info: trial=N) |
| `phase2_question_onset` | 2 | "Which context fits better?" onset (trial_info: trial=N, cat_a=X, cat_b=Y, variant=…) |
| `phase2_response` | 2 | Participant clicked category A or B (trial_info: trial=N, response=X) |
| `phase2_question_offset` | 2 | Question screen ended (trial_info: trial=N) |
| `phase2_trial_iti_onset` | 2 | Inter-trial interval blank (trial_info: trial=N) |
| `phase2_trial_iti_offset` | 2 | ITI ended |
| `phase2_complete` | 2 | Phase 2 trials finished |
| `phase2_break_onset` | 2 | Break screen appeared (trial_info: after_trial=N, total_trials=M; every 16 trials, progress bar) |
| `phase2_break_enter` | 2 | Enter pressed |
| `phase2_break_offset` | 2 | Screen transition |
| `phase3_questions_onset` | 3 | "If you have any questions, ask the experimenter now. Press Enter when you're ready." (first Phase 3 screen) |
| `phase3_questions_enter` | 3 | Enter pressed |
| `phase3_questions_offset` | 3 | Screen transition |
| `phase3_instr1_onset` | 3 | "Now let's sort some shapes again... First you will see all of them." appeared |
| `phase3_instr1_enter` | 3 | Enter pressed |
| `phase3_instr1_offset` | 3 | Screen transition |
| `phase3_instr2_onset` | 3 | "Then place them one at a time by clicking where you want each to go, as in the demo you saw earlier." appeared |
| `phase3_instr2_enter` | 3 | Enter pressed |
| `phase3_instr2_offset` | 3 | Screen transition |
| `phase3_instr3_onset` | 3 | "Group them into groups—not on a spectrum or line. Shapes closer together are in the same group." appeared |
| `phase3_instr3_enter` | 3 | Enter pressed |
| `phase3_instr3_offset` | 3 | Screen transition |
| `phase3_instr4_onset` | 3 | "Use as many groups as you need, and any grouping that is intuitive to you." appeared |
| `phase3_instr4_enter` | 3 | Enter pressed |
| `phase3_instr4_offset` | 3 | Screen transition |
| `phase3_before_grid_onset` | 3 | "As earlier, you will now see 16 shapes..." appeared |
| `phase3_before_grid_enter` | 3 | Enter pressed |
| `phase3_before_grid_offset` | 3 | Screen transition |
| `phase3_grid_onset` | 3 | Shape grid display started |
| `phase3_grid_offset` | 3 | Shape grid display ended |
| `phase3_fixation_onset` | 3 | Fixation cross onset |
| `phase3_fixation_offset` | 3 | Fixation cross ended |
| `phase3_instruction2a_onset` | 3 | "Sort by where you'd expect to see the shapes" instruction appeared |
| `phase3_instruction2a_enter` | 3 | Enter pressed |
| `phase3_instruction2a_offset` | 3 | Screen transition |
| `phase3_instruction2c_onset` | 3 | "Click somewhere to place, then press Enter to submit. Once you've submitted..." instruction appeared |
| `phase3_instruction2c_enter` | 3 | Enter pressed |
| `phase3_instruction2c_offset` | 3 | Screen transition |
| `phase3_stimulus_onset` | 3 | Shape shown (trial_info: trial=N, shape=*.bmp) |
| `phase3_stimulus_offset` | 3 | Shape display ended, clickable (trial_info: trial=N, shape=*.bmp) |
| `phase3_click_place` | 3 | Each click to move shape (trial_info: trial=N, shape=…, click=N) |
| `phase3_enter_submit` | 3 | Enter to submit (trial_info: trial=N, shape=…) |
| `phase3_complete` | 3 | Phase 3 drag task finished (all shapes placed) |
| `phase3_debrief_onset` | 3 | Debrief question N appeared (trial_info: question=1, 2, or 3). Logged 3×. |
| `phase3_debrief_response` | 3 | Participant clicked Yes/No (trial_info: question=N, answer=Yes/No). Logged 3×. |
| `phase3_debrief_offset` | 3 | Debrief question N ended (trial_info: question=N). Logged 3×. |
| `phase1_placements_saved` | 1 | Phase 1 placement image saved incrementally after each shape (trial_info: filename trial=N) |
| `phase3_placements_saved` | 3 | Phase 3 placement image saved incrementally after each shape (trial_info: filename trial=N) |
| `summary_saved` | — | Summary CSV written (trial_info: filename) |
| `thanks_onset` | — | Thank-you screen appeared |
| `thanks_offset` | — | Thank-you screen ended |
| `escape_pressed` | — | Participant pressed Escape to quit (trial_info: screen=…; e.g. participant_name, tutorial_video, phase1_click_place, phase2_question, phase3_debrief) |

---

## Phase 1 CSV (phase1_{participant}_{datetime}.csv)

Per-shape data from the bottom-up shape classification phase.

| Column | Type | Description |
|--------|------|-------------|
| `shape_path` | String | Full path to the shape image file |
| `final_x` | Float | Final x position in screen coordinates (height units) |
| `final_y` | Float | Final y position in screen coordinates (height units) |
| `rt` | Float | Reaction time from clickable onset to last click (seconds). At least one click required before Enter. |
| `stimulus_onset_ttl` | Float | Reserved (currently empty); use ttl_log for stimulus onset timestamp |
| `stimulus_offset_ttl` | Float | Reserved (currently empty); use ttl_log for stimulus offset timestamp |
| `click_ttl` | Float | TTL timestamp at last click to place |
| `all_click_ttl` | String | Semicolon-separated timestamps of all clicks (Unix) |
| `submit_ttl` | Float | TTL timestamp when participant pressed Enter to submit |

---

## Phase 2 CSV (phase2_{participant}_{datetime}.csv)

Per-trial data from the top-down context incorporation phase. Trial count matches **`phase2_trial_order.csv`** (e.g. 80 rows). Trial order and stimuli match the template row-for-row (`trial` 1…N = template row order).

**Template (`phase2_trial_order.csv`):** Header plus N trial rows. Columns include `trial_number`, `shape`, `shape_path`, `context1`, `context1_image`, `context2`, `context2_image`, `variant`, and design labels `primary_context` / `secondary_context` (or legacy `strong_context` / `neutral_context`). The script loads paths, `context1`/`context2` (A/B), `variant`, and optional primary/secondary labels. Paths may be absolute or relative to `STIMULI/`; `Shapes`/`Contexts` in paths are normalized to `shapes`/`contexts`. `variant` is a pass-through string (e.g. `primary_first_img0`). **TASK_DESCRIPTION.md** has the full spec.

**Note:** TTL columns `fixation_onset_ttl` through `question_onset_ttl` are reserved but currently written empty; use `ttl_log` for full event timestamps. Only `response_ttl` is populated.

| Column | Type | Description |
|--------|------|-------------|
| `trial` | Integer | Trial number (1…N; same order as rows in `phase2_trial_order.csv`) |
| `shape_path` | String | Full path to the shape image |
| `context_1_path` | String | Full path to first context image |
| `context_2_path` | String | Full path to second context image |
| `trial_variant` | String | Copy of the template `variant` cell (e.g. `primary_first_img0` or `secondary_first_img1`) |
| `response` | String | Button clicked: category A or B (e.g., BARK, CLOUD) |
| `rt` | Float | Reaction time from question onset to button click (seconds) |
| `fixation_onset_ttl` | Float | TTL at fixation onset (see note above) |
| `context1_onset_ttl` | Float | TTL at context 1 onset |
| `shape_onset_ttl` | Float | TTL at shape onset |
| `reddot_onset_ttl` | Float | TTL at red dot onset |
| `context2_onset_ttl` | Float | TTL at context 2 onset |
| `shape2_onset_ttl` | Float | TTL at shape 2 onset |
| `reddot2_onset_ttl` | Float | TTL at red dot 2 onset |
| `question_onset_ttl` | Float | TTL at question screen onset |
| `response_ttl` | Float | TTL at response button click (populated) |

---

## Phase 3 CSV (phase3_{participant}_{datetime}.csv)

Same structure as Phase 1 (including click_ttl = last click, all_click_ttl = all clicks). Per-shape data from the post-context shape reclassification phase. Shape order is randomized differently from Phase 1.

---

## Placement Images (phase1_placements_*.png, phase3_placements_*.png)

PNG images of final shape placements at the end of Phase 1 and Phase 3. White canvas with each shape drawn at its final (x, y) position. Saved only for non-test participants.

---

## Debrief CSV (debrief_{participant}_{datetime}.csv)

Post–Phase 3 questionnaire (3 questions). One row per question.

| Column | Type | Description |
|--------|------|-------------|
| `question` | Integer | Question number (1, 2, or 3) |
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
| `shapegrid_width_px` | Integer | ShapeGrid pixel width (from `ShapeGrid_4x4_bmp.png`) |
| `shapegrid_height_px` | Integer | ShapeGrid pixel height |
| `grid_border_coords` | String | Grid border coordinates (if computed) |
| `per_shape_ground_truth` | String | Per-shape: `name.bmp:row=R,col=C,center_x=X,center_y=Y` (4×4 from sorted order; pipe-separated) |
| `scaling_factor` | String | Scaling factor used for display |
| `phase3_euclidean_distances` | String | Pairwise distances (format: `i-j:dist;...`). Smaller = shapes grouped more similarly (closer categorically). |

---

## File Saving

- **Location**: `../LOG_FILES/`
- **Filenames**: `{basename}_{participant}_{YYYYMMDD_HHMMSS}.csv` or `.png`
- **Test participants**: Name contains "test" → no files written (TTL log deleted)

**Examples in the repository:** Filenames and file list: **README.md** (Data output → Example output).
