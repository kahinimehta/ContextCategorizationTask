# CSV and TTL Documentation

Definitions for **`ttl_log_*`** (columns below; mapping table follows) plus **`phase*_*.csv`**, **`debrief`**, **`summary`**.

**Elsewhere:** run sheet (**`script.md`**); stimuli + timings + **`phase2_trial_order.csv`** (**`TASK_DESCRIPTION.md`**); repo bootstrap / example filenames (**`README.md`**).

## TTL Log (ttl_log_{participant}_{datetime}.csv)

Every TTL trigger is logged with timestamp, trigger code, event label, and trial info. Written incrementally as each event occurs. The file is initially created as `ttl_log_{datetime}.csv` (before participant name is known), then renamed to include the participant at task end.

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | Float (Unix) | Time when TTL fired |
| `trigger_code` | String | Event identifier (same as event_label unless overridden) |
| `event_label` | String | Human-readable event name |
| `trial_info` | String | Optional trial metadata (e.g., trial=3, shape=Shape_0_1.png) |

**Event types**: See TTL Trigger Mapping below.

For **fixed-duration** segments, `*_onset` fires immediately **before** the first `flip()` of that segment and `*_offset` immediately **after** the last frame (after `_wait(duration)`). Instruction screens additionally log `*_enter` on keypress. On Phase 2 question trials, **`phase2_response`** is logged immediately before **`phase2_question_offset`** (response TTL, then epoch end).

**Tutorial path:** Exactly one training stream runs — either **`tutorial_video_onset`** / **`tutorial_video_offset`** (successful **`STIMULI/tutorial_video.mp4`** playback **without** fallback TTLs inside the tutorial), **or** the **`tutorial_fallback_*`** / **`tutorial_fallback_step{2–4}_*_`** sequence (**animated color-sort**, **`trial_info: step=…`** on `tutorial_fallback_onset`).

---

**Historical:** Older `ttl_log` files may still list `phase1_instruction2a_*` / `phase3_instruction2a_*` (participant-paced “expect to see” prompts; no longer emitted).

## TTL Trigger Mapping

Trigger codes equal event labels (strings). Use these for EEG/fMRI analysis. Phase 1 & 3: **Click** to move, **Enter** to submit. Each click logged as `click_place` (trial_info: click=N).

| Trigger code | Phase | Description |
|--------------|-------|-------------|
| `participant_name_onset` | — | Participant id entry (typed text + cursor; no format instructions on screen) |
| `participant_name_offset` | — | Participant pressed Enter on name |
| *(Instruction screens: onset, enter, offset)* | — | All Enter-to-continue screens log onset (appeared), enter (keypress), offset (transition) |
| `experiment_start` | — | Experiment started (trial_info: participant=…) |
| `experiment_end` | — | Experiment ended (trial_info: participant=…) |
| `welcome_onset` | — | Welcome screen appeared |
| `welcome_enter` | — | Enter pressed |
| `welcome_offset` | — | Screen transition |
| `tutorial_video_onset` | — | Tutorial video started |
| `tutorial_video_offset` | — | Tutorial video ended |
| `tutorial_fallback_onset` | — | Fallback **tutorial** step onset (`trial_info: step=1, 2, 3, 4, 5a, 5b, or 6`). Only when **`STIMULI/tutorial_video.mp4`** is absent or playback fails — **color-sort** demo (**`script.md`**); see separate `tutorial_fallback_step{n}_*` timestamps for stimulus epochs inside steps 2–4. |
| `tutorial_fallback_offset` | — | Fallback step ended (**same `trial_info: step=`** as matching onset). Steps **5a–b** and **6** are single static screens (no `tutorial_fallback_step*_center` / `target` children). |
| `tutorial_fallback_step2_center_onset` | — | Step 2: red **square** center epoch begins (logged **before** center `flip()`; display lasts **`TUTORIAL_FB_CLICK_CENTER_SEC`**) |
| `tutorial_fallback_step2_center_offset` | — | Step 2: center hold ended (after **`TUTORIAL_FB_CLICK_CENTER_SEC`**). |
| `tutorial_fallback_step2_target_onset` | — | Step 2: square at **left-cluster** target (`TUTORIAL_FB_CLICK_TARGET_SEC`). Color-sort layout. |
| `tutorial_fallback_step2_target_offset` | — | Step 2: target epoch ended |
| `tutorial_fallback_step3_center_onset` | — | Step 3: red **circle** center epoch (`TUTORIAL_FB_CLICK_CENTER_SEC`) |
| `tutorial_fallback_step3_center_offset` | — | Step 3: center epoch ended |
| `tutorial_fallback_step3_target_onset` | — | Step 3: circle beside square (`TUTORIAL_FB_CLICK_TARGET_SEC`) — **red-with-red** placement |
| `tutorial_fallback_step3_target_offset` | — | Step 3: target epoch ended |
| `tutorial_fallback_step4_center_onset` | — | Step 4: **green** circle center epoch (`TUTORIAL_FB_CLICK_CENTER_SEC`) |
| `tutorial_fallback_step4_center_offset` | — | Step 4: center epoch ended |
| `tutorial_fallback_step4_target_onset` | — | Step 4: green circle at **right** target (`TUTORIAL_FB_CLICK_TARGET_SEC`) — separate **color** from reds |
| `tutorial_fallback_step4_target_offset` | — | Step 4: target epoch ended |
| `tutorial_transition_onset` | — | End of Phase 1 tutorial: **"Your turn—same rules."** appeared |
| `tutorial_transition_enter` | — | Enter pressed |
| `tutorial_transition_offset` | — | Screen transition |
| `phase1_questions_onset` | 1 | Phase 1 first instruction: "Questions? Ask now." |
| `phase1_questions_enter` | 1 | Enter pressed |
| `phase1_questions_offset` | 1 | Screen transition |
| `phase1_instr1_onset` | 1 | **"Sort objects—all on screen first."** |
| `phase1_instr1_enter` | 1 | Enter pressed |
| `phase1_instr1_offset` | 1 | Screen transition |
| `phase1_instr2_onset` | 1 | **"Place one at a time (same as demo)."** |
| `phase1_instr2_enter` | 1 | Enter pressed |
| `phase1_instr2_offset` | 1 | Screen transition |
| `phase1_instr3_onset` | 1 | **"Group by proximity—not along a spectrum."** |
| `phase1_instr3_enter` | 1 | Enter pressed |
| `phase1_instr3_offset` | 1 | Screen transition |
| `phase1_instr4_onset` | 1 | **"Use as many groups as you want."** |
| `phase1_instr4_enter` | 1 | Enter pressed |
| `phase1_instr4_offset` | 1 | Screen transition |
| `phase1_before_grid_onset` | 1 | **"16 objects next — reference only; don't memorize."** |
| `phase1_before_grid_enter` | 1 | Enter pressed |
| `phase1_before_grid_offset` | 1 | Screen transition |
| `phase1_grid_onset` | 1 | Object grid display started |
| `phase1_grid_offset` | 1 | Object grid display ended |
| `phase1_fixation_onset` | 1 | Fixation cross onset |
| `phase1_fixation_offset` | 1 | Fixation cross ended |
| `phase1_instruction2c_onset` | 1 | **"Click to place — Enter locks. Mini-grid bottom-right stays. Help? Ask."** (with miniature grid inset) |
| `phase1_instruction2c_enter` | 1 | Enter pressed |
| `phase1_instruction2c_offset` | 1 | Screen transition |
| `phase1_complete` | 1 | Phase 1 drag task finished (all objects placed) |
| `phase1_stimulus_onset` | 1 | Isolation preview: centered object (BMP) + miniature grid bottom-right (trial_info: trial=N, shape=*.bmp filename) |
| `phase1_stimulus_offset` | 1 | Isolation preview ended, click-to-place (same inset; trial_info: trial=N, shape=*.bmp) |
| `phase1_click_place` | 1 | Each click to move object (trial_info: trial=N, shape=…, click=N) |
| `phase1_enter_submit` | 1 | Enter to submit (trial_info: trial=N, shape=…) |
| `phase2_questions_onset` | 2 | Phase 2 first instruction: **"Questions? Ask now."** |
| `phase2_questions_enter` | 2 | Enter pressed |
| `phase2_questions_offset` | 2 | Screen transition |
| `phase2_instr1_onset` | 2 | **"Each object paired with two contexts."** |
| `phase2_instr1_enter` | 2 | Enter pressed |
| `phase2_instr1_offset` | 2 | Screen transition |
| `phase2_instr2_onset` | 2 | **"Trial: scene → object → dot."** |
| `phase2_instr2_enter` | 2 | Enter pressed |
| `phase2_instr2_offset` | 2 | Screen transition |
| `phase2_instr2b_onset` | 2 | **"On the dot: say a label aloud. ←/→ chooses fit — speak each trial."** |
| `phase2_instr2b_enter` | 2 | Enter pressed |
| `phase2_instr2b_offset` | 2 | Screen transition |
| `phase2_instr3_onset` | 2 | **"Recorded — demo runs first."** |
| `phase2_instr3_enter` | 2 | Enter pressed |
| `phase2_instr3_offset` | 2 | Screen transition |
| `phase2_instr4_onset` | 2 | **"Reuse OK; vary when possible."** |
| `phase2_instr4_enter` | 2 | Enter pressed |
| `phase2_instr4_offset` | 2 | Screen transition |
| `phase2_instr5_onset` | 2 | **"Watch demo next."** (min display `PHASE2_INSTR5_MIN_SEC`, 5 s) |
| `phase2_instr5_enter` | 2 | Enter pressed |
| `phase2_instr5_offset` | 2 | Screen transition |
| `phase2_tutorial_intro_onset` | 2 | Phase 2 tutorial intro: **"Space scene → circle → circus scene. Name the object aloud; then we choose which fits."** |
| `phase2_tutorial_intro_enter` | 2 | Enter pressed |
| `phase2_tutorial_intro_offset` | 2 | Screen transition |
| `phase2_tutorial_fixation_onset` | 2 | Tutorial fixation onset |
| `phase2_tutorial_fixation_offset` | 2 | Tutorial fixation ended |
| `phase2_tutorial_context1_onset` | 2 | Tutorial context 1 onset |
| `phase2_tutorial_context1_offset` | 2 | Tutorial context 1 ended |
| `phase2_tutorial_shape_onset` | 2 | Tutorial focal object onset (event label **`shape`** retained) |
| `phase2_tutorial_shape_offset` | 2 | Tutorial focal object ended |
| `phase2_tutorial_blank_onset` | 2 | Legacy — **not emitted** in current code (1 s blank between object epoch and cue dot was removed) |
| `phase2_tutorial_blank_offset` | 2 | Legacy — **not emitted** |
| `phase2_tutorial_reddot_onset` | 2 | Tutorial cue dot (black circle) + on-screen PLANET cue (`PHASE2_REDDOT_DURATION_SEC`) |
| `phase2_tutorial_reddot_offset` | 2 | Tutorial cue dot ended |
| `phase2_tutorial_context2_onset` | 2 | Tutorial context 2 onset |
| `phase2_tutorial_context2_offset` | 2 | Tutorial context 2 ended |
| `phase2_tutorial_shape2_onset` | 2 | Tutorial second object onset |
| `phase2_tutorial_shape2_offset` | 2 | Tutorial second object ended |
| `phase2_tutorial_blank2_onset` | 2 | Legacy — **not emitted** in current code (blank before second cue dot removed) |
| `phase2_tutorial_blank2_offset` | 2 | Legacy — **not emitted** |
| `phase2_tutorial_reddot2_onset` | 2 | Tutorial cue dot 2 (black) + on-screen BALL cue |
| `phase2_tutorial_reddot2_offset` | 2 | Tutorial cue dot 2 ended |
| `phase2_tutorial_question_onset` | 2 | Tutorial question (SPACE \| CIRCUS) |
| `phase2_tutorial_demo_select_onset` | 2 | Tutorial highlight: right button (CIRCUS) + subtitle **"e.g., CIRCUS"** |
| `phase2_tutorial_demo_select_offset` | 2 | Highlight / subtitle phase ended |
| `phase2_tutorial_question_offset` | 2 | Question screen ended (after demo selection) |
| `phase2_tutorial_response` | 2 | Scripted demo choice (e.g. **trial_info: CIRCUS**) |
| `phase2_tutorial_post_blank_onset` | 2 | White full-screen blank after tutorial |
| `phase2_tutorial_post_blank_offset` | 2 | Post-response blank ended |
| `phase2_ready_onset` | 2 | **"Ready for recorded trials?"** (Enter + **"Enter to continue."** hint) |
| `phase2_ready_enter` | 2 | Enter pressed |
| `phase2_ready_offset` | 2 | Screen transition |
| `phase2_before_trials_onset` | 2 | **"Questions? Enter to start."** |
| `phase2_before_trials_enter` | 2 | Enter pressed |
| `phase2_before_trials_offset` | 2 | Screen transition |
| `phase2_fixation_onset` | 2 | Fixation before trial (trial_info: trial=N) |
| `phase2_fixation_offset` | 2 | Fixation ended (trial_info: trial=N) |
| `phase2_context1_onset` | 2 | Context 1 display onset (trial_info: trial=N, shape=*.bmp) |
| `phase2_context1_offset` | 2 | Context 1 offset (trial_info: trial=N) |
| `phase2_shape_onset` | 2 | Task object (BMP) onset (trial_info: trial=N, shape=*.bmp) |
| `phase2_shape_offset` | 2 | Task object epoch ended (trial_info: trial=N) |
| `phase2_blank1_onset` | 2 | Legacy — **not emitted** (object epoch → cue dot is immediate; formerly 1 s blank) |
| `phase2_blank1_offset` | 2 | Legacy — **not emitted** |
| `phase2_reddot_onset` | 2 | Black cue dot + “say aloud” epoch (trial_info: trial=N, shape=*.bmp). Event label **`reddot`** is historical |
| `phase2_reddot_offset` | 2 | Cue dot offset (trial_info: trial=N) |
| `phase2_context2_onset` | 2 | Context 2 display onset (trial_info: trial=N, shape=*.bmp) |
| `phase2_context2_offset` | 2 | Context 2 offset (trial_info: trial=N) |
| `phase2_shape2_onset` | 2 | Task object (2nd) onset (trial_info: trial=N) |
| `phase2_shape2_offset` | 2 | Task object (2nd) epoch ended (trial_info: trial=N) |
| `phase2_blank2_onset` | 2 | Legacy — **not emitted** (2nd object epoch → cue dot 2 is immediate) |
| `phase2_blank2_offset` | 2 | Legacy — **not emitted** |
| `phase2_reddot2_onset` | 2 | Second black cue dot + “say aloud” (trial_info: trial=N, shape=*.bmp) |
| `phase2_reddot2_offset` | 2 | Cue dot 2 offset (trial_info: trial=N) |
| `phase2_question_onset` | 2 | **"Better context?"** with category labels (trial_info: trial=N, cat_a=X, cat_b=Y, variant=…) |
| `phase2_response` | 2 | **Left**/**right** arrow selects **`context_1`** / **`context_2`** (trial_info: trial=N, response=label) |
| `phase2_question_offset` | 2 | Question screen ended (trial_info: trial=N) |
| `phase2_trial_iti_onset` | 2 | Inter-trial interval blank (trial_info: trial=N) |
| `phase2_trial_iti_offset` | 2 | ITI ended |
| `phase2_complete` | 2 | Phase 2 trials finished |
| `phase2_break_onset` | 2 | **"Take a break!"** + progress bar (trial_info on **onset** only: **after_trial** = 0-based index of next trial, **total_trials** = N; first break at **after_trial=16** for 64 trials) |
| `phase2_break_enter` | 2 | Enter pressed |
| `phase2_break_offset` | 2 | Screen transition |
| `phase3_questions_onset` | 3 | **"Questions? Enter when ready."** |
| `phase3_questions_enter` | 3 | Enter pressed |
| `phase3_questions_offset` | 3 | Screen transition |
| `phase3_instr1_onset` | 3 | **"Sort again — like Phase 1. See all objects first."** |
| `phase3_instr1_enter` | 3 | Enter pressed |
| `phase3_instr1_offset` | 3 | Screen transition |
| `phase3_instr2_onset` | 3 | **"Place one at a time (same as earlier)."** |
| `phase3_instr2_enter` | 3 | Enter pressed |
| `phase3_instr2_offset` | 3 | Screen transition |
| `phase3_instr3_onset` | 3 | **"Groups by proximity — not along a spectrum."** |
| `phase3_instr3_enter` | 3 | Enter pressed |
| `phase3_instr3_offset` | 3 | Screen transition |
| `phase3_instr4_onset` | 3 | **"Any intuitive grouping counts."** |
| `phase3_instr4_enter` | 3 | Enter pressed |
| `phase3_instr4_offset` | 3 | Screen transition |
| `phase3_before_grid_onset` | 3 | **"Same rule: 16 objects — reference grid only."** |
| `phase3_before_grid_enter` | 3 | Enter pressed |
| `phase3_before_grid_offset` | 3 | Screen transition |
| `phase3_grid_onset` | 3 | Object grid display started |
| `phase3_grid_offset` | 3 | Object grid display ended |
| `phase3_fixation_onset` | 3 | Fixation cross onset |
| `phase3_fixation_offset` | 3 | Fixation cross ended |
| `phase3_instruction2c_onset` | 3 | Same as Phase 1 **phase1_instruction2c**: **"Click to place — Enter locks…"** (mini-grid bottom-right) |
| `phase3_instruction2c_enter` | 3 | Enter pressed |
| `phase3_instruction2c_offset` | 3 | Screen transition |
| `phase3_stimulus_onset` | 3 | Isolation preview: centered object (BMP) + miniature grid bottom-right (trial_info: trial=N, shape=*.bmp) |
| `phase3_stimulus_offset` | 3 | Isolation preview ended, click-to-place (same inset; trial_info: trial=N, shape=*.bmp) |
| `phase3_click_place` | 3 | Each click to move object (trial_info: trial=N, shape=…, click=N) |
| `phase3_enter_submit` | 3 | Enter to submit (trial_info: trial=N, shape=…) |
| `phase3_complete` | 3 | Phase 3 drag task finished (all objects placed) |
| `phase3_debrief_onset` | 3 | Debrief question appeared (trial_info: question=1–3); order each question **onset** → **phase3_debrief_response** (click) → **offset** |
| `phase3_debrief_response` | 3 | Participant clicked Yes/No (trial_info: question=N, answer=Yes/No). Logged 3×. |
| `phase3_debrief_offset` | 3 | Debrief question N ended (trial_info: question=N). Logged 3×. |
| `phase1_placements_saved` | 1 | Phase 1 placement image saved incrementally after each object (trial_info: filename trial=N) |
| `phase3_placements_saved` | 3 | Phase 3 placement image saved incrementally after each object (trial_info: filename trial=N) |
| `summary_saved` | — | Summary CSV written (trial_info: filename) |
| `thanks_onset` | — | Thank-you screen appeared |
| `thanks_offset` | — | Thank-you screen ended |
| `escape_pressed` | — | Participant pressed Escape to quit (trial_info: `screen=<event_label>` for **`wait_for_continue`** screens, or fixed strings e.g. **`participant_name`**, **`tutorial_video`**, **`phase1_click_place`** / **`phase3_click_place`**, **`phase2_question`**, **`phase3_debrief`**). Not emitted during timed grid/fixation/stimulus epochs. |

---

## Phase 1 CSV (phase1_{participant}_{datetime}.csv)

Per-trial object data from Phase 1 (bottom-up grouping; **`shape`** in filenames / `trial_info` retains technical label).

| Column | Type | Description |
|--------|------|-------------|
| `shape_path` | String | Full path to the BMP stimulus file identifying the object |
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

Per-trial (**`trial`** aligns with **`phase2_trial_order.csv`**). Template (**`phase2_trial_order.csv`**, **`PHASE2_CSV_REQUIRED`**) and **`stderr`** row-count banner: **`TASK_DESCRIPTION.md`** only.

Placeholder epoch columns (`fixation_onset_ttl` … `question_onset_ttl`): schema only; timings in **`ttl_log_*`**. **`response_ttl`** populated.

| Column | Type | Description |
|--------|------|-------------|
| `trial` | Integer | Trial number (1…N; same order as rows in `phase2_trial_order.csv`) |
| `shape_path` | String | Full path to the BMP object stimulus |
| `context_1_path` | String | Full path to first context stimulus |
| `context_2_path` | String | Full path to second context stimulus |
| `trial_variant` | String | Copy of the template `variant` cell (e.g. `primary_first_img0` or `secondary_first_img1`) |
| `response` | String | Selected category (**uppercased**); **left arrow** = label on left (**`context_1`**), **right arrow** = label on right (**`context_2`**) |
| `rt` | Float | Reaction time from question onset to arrow key press (seconds) |
| `fixation_onset_ttl` … `question_onset_ttl` | Float | Unused placeholders (epoch markers live in **`ttl_log_*`** only) |
| `response_ttl` | Float | Participant choice (**populated**) |

---

## Phase 3 CSV (phase3_{participant}_{datetime}.csv)

Same structure as Phase 1 (including click_ttl = last click, all_click_ttl = all clicks). Post-context re-grouping trials; object order is randomized differently from Phase 1.

---

## Placement Images (phase1_placements_*.png, phase3_placements_*.png)

PNG images of final object placements at the end of Phase 1 and Phase 3. **White** canvas with each object drawn at its final (x, y) position (task objects use the same **white-matte strip** as on-screen; see **`OBJECT_WHITE_BG_STRIP_THRESHOLD`** in **`context_shape_task.py`**). Saved only for non-test participants.

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
1. "Same grouping style as Phase 1?"
2. "Did contexts sway round-2 groups?"
3. "See objects differently the second sort?"

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
| `phase3_euclidean_distances` | String | Pairwise distances (format: `i-j:dist;...`). Smaller = objects grouped more similarly (closer categorically). |

---

## File Saving

- **Location**: `../LOG_FILES/`
- **Filenames**: `{basename}_{participant}_{YYYYMMDD_HHMMSS}.csv` or `.png`
- **Test participants**: Name contains "test" → no files written (TTL log deleted)

Example filenames: **README.md** → Data output.
