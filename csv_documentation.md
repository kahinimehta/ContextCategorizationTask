# CSV Variables Documentation

Complete reference for all CSV outputs from the ContextShape Task. See `script.md` for experimenter instructions.

## TTL Log (ttl_log_{participant}.csv)

Every TTL trigger is logged with timestamp, trigger code, event label, and trial info. Written incrementally as each event occurs.

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | Float (Unix) | Time when TTL fired |
| `trigger_code` | String | Event identifier (same as event_label unless overridden) |
| `event_label` | String | Human-readable event name |
| `trial_info` | String | Optional trial metadata (e.g., trial=3, shape=Shape_0.10_1.70.png) |

**Event types**: welcome, welcome_click, tutorial_overview_onset/offset, tutorial_instruction_onset/offset, tutorial_practice_stimulus_onset/offset, tutorial_practice_drag_start, tutorial_practice_submit, tutorial_debrief, tutorial_transition, phase1_instructions, phase1_grid_onset/offset, phase1_fixation_onset/offset, phase1_instruction2, phase1_stimulus_onset/offset, phase1_drag_start, phase1_submit, phase2_instructions, phase2_tutorial_*, phase2_ready, phase2_fixation_onset/offset, phase2_context1_onset/offset, phase2_shape_onset/offset, phase2_reddot_onset/offset, phase2_context2_onset/offset, phase2_shape2_onset/offset, phase2_reddot2_onset/offset, phase2_question_onset, phase2_response, phase2_break_onset, phase3_instructions, phase3_stimulus_onset/offset, phase3_drag_start, phase3_submit.

---

## Phase 1 CSV (phase1_{participant}.csv)

Per-shape data from the bottom-up shape classification phase.

| Column | Type | Description |
|--------|------|-------------|
| `shape_path` | String | Full path to the shape image file |
| `final_x` | Float | Final x position in screen coordinates (height units) |
| `final_y` | Float | Final y position in screen coordinates (height units) |
| `rt` | Float | Reaction time from drag-enable to SUBMIT (seconds) |
| `stimulus_onset_ttl` | Float | TTL timestamp at stimulus onset |
| `stimulus_offset_ttl` | Float | TTL timestamp at stimulus offset |
| `drag_start_ttl` | Float | TTL timestamp when drag started |
| `drag_end_ttl` | Float | TTL timestamp when drag ended |
| `submit_ttl` | Float | TTL timestamp at SUBMIT click |

---

## Phase 2 CSV (phase2_{participant}.csv)

Per-trial data from the top-down context incorporation phase (48 trials).

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

## Phase 3 CSV (phase3_{participant}.csv)

Same structure as Phase 1. Per-shape data from the post-context shape reclassification phase. Shape order is randomized differently from Phase 1.

---

## Summary CSV (summary_{participant}.csv)

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
| `phase3_euclidean_distances` | String | Pairwise Euclidean distances between all Phase 3 final positions (format: `i-j:dist;...`) |

---

## File Saving

- **Location**: `../LOG_FILES/` (relative to task root)
- **Incremental writes**: All CSVs are written row-by-row with flush to disk
- **Test participants**: If participant name contains "test" (case-insensitive), file saving is skipped
