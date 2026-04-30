# Experimenter Script — run sheet

**Roles:** **`script.md`** (this file) = verbatim on-screen copy + run order + representative TTL names. **`TASK_DESCRIPTION.md`** = `*_SEC`, paths, **`phase2_trial_order.csv`**, troubleshooting. **`csv_documentation.md`** = full **`ttl_log_*`** + **`*.csv`** schema (**authoritative** for event spellings).

**Operational:** `python context_shape_task.py` from **`ContextCategorizationTask/`**; outputs in **`../LOG_FILES/`** with **`{participant}_{YYYYMMDD_HHMMSS}`** in each filename (**patterns:** **`README.md`**); no saves if **`test`** in participant name. **`PSYCHOPY_WINDOWED=1`** → 1280×720 windowed; **`PSYCHOPY_DUMMY_WINDOW=0`** disables the extra 100×100 window; **`PSYCHOPY_CHECK_TIMING=1`** enables frame calibration (macOS: rarely). **ESC** / keyboard quirks: **`TASK_DESCRIPTION.md`**.

**Enter-to-advance:** Every **`wait_for_continue`** screen shows the main text (and optional mini-grid inset) plus gray **"Enter to continue."** at the bottom (**Enter** only; no mouse).

**TTL / CSV:** Trigger names in the experiment sections below are **not** exhaustive. **`*_onset` / `*_offset` / Enter-screen rules**, the full mapping table, **`escape_pressed`**, and behavioral **`*.csv`** columns are in **`csv_documentation.md`**.

---

## Full Experiment Script

### Participant login

**Display:** **"Enter your name"** (upper); centered entry line. **Enter** submits; **ESC** quits. Key handling: **`TASK_DESCRIPTION.md`** (macOS / unrestricted poll).

**TTL:** `participant_name_onset`, `participant_name_offset`; then **`experiment_start`** (**`trial_info: participant=…`**) immediately after the name is finalized, **before** **`welcome`** (no separate participant-facing screen).

---

### Welcome

**Display:** **"Welcome to your task! — Hit Enter to watch the tutorial video."**  
(Plus **"Enter to continue."** — see preamble.)

**TTL:** `welcome_onset`, `welcome_enter`, `welcome_offset`

---

### Tutorial (Phase 1 training)

**Training demo (fallback):** Red square + circles; **groups by color** (reds left cluster, green apart). Steps **2–4** show an **animated cursor** (pointer moves in, brief click ring, shape moves to the target with the cursor, click ring at destination). If **`STIMULI/tutorial_video.mp4`** is present and plays, it replaces the fallback TTL stream—video subtitles/overlays **should mirror** the captions below where applicable.

**Video** (`tutorial_video.mp4`): motion carries meaning; captions need not match the fallback line-for-line but keep **5a–6** gist.

**Fallback** (durations **`TASK_DESCRIPTION.md`**, Tutorial fallback):

**Step 1** (`tutorial_fallback_onset` / `offset`, `trial_info: step=1`): **"The first part of the task is about sorting objects. Watch how we sort these objects!"**

**Step 2** (`tutorial_fallback_step2_*`): **"First, let's click to place the red square on the left — Then, we hit Enter."**

**Step 3** (`tutorial_fallback_step3_*`): **"Now, let's group the red circle with the red square on the left."**

**Step 4** (`tutorial_fallback_step4_*`): **"Let's place the green circle to the right (in a different group)."**

**Step 5a** (`step=5a`): **"See how we ended up sorting by color? We could have sorted by shape too — there are no wrong answers here!"**

**Step 5b** (`step=5b`): **"We created groups, not a spectrum — nearby objects share a group."**

**Step 6** (`step=6`): **"Click to place — Enter submits each placement."**  
*(A possible “large spread is OK” line exists only as a commented-out stim in code; not shown.)*

**Transition:** **"Your turn to group some objects! — Remember the same rules."**

**TTL:** `tutorial_video_*` **or** `tutorial_fallback_*` (+ `tutorial_fallback_step{2|3|4}_{center|target}_*` for steps 2–4), then `tutorial_transition_*`.

---

### Phase 1 — Object sorting

**Instructions (before grid):**  
1. **"Ask the experimenter if you have any questions!"** · `phase1_questions`

**TTL:** `phase1_questions_*`

**Code vs older drafts:** After the Phase 1 tutorial, **`main()`** runs **`phase1_questions`** then **`phase1_before_grid`** with **no** screens in between. In **`context_shape_task.py`**, three **`wait_for_continue`** entries (**"You will now sort some objects."**, **"Place one at a time (same as demo)."**, **"Group by proximity—not along a spectrum."**) are **commented out** inside **`p1_screens`** — they **never** appear and **must not** be confused with the **`phase1_instr1`** … **`phase1_instr3`** screens **after** fixation below (different copy, same TTL names would have collided if those lines were uncommented).

**Before grid:** **"You will now see all 16 objects you will be sorting at the same time — for reference only; just watch & don't memorize."** · `phase1_before_grid`

**TTL:** `phase1_before_grid_*`

**Grid / fixation:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png` fullscreen + same composite as **miniature bottom-right** inset (**timings** **`TASK_DESCRIPTION.md`**).

**TTL:** `phase1_grid_*`, `phase1_fixation_*`

**After fixation (in order):**  
1. **"Now, group these objects like in the demo."** · `phase1_instr1` (mini-grid inset)  
2. **"Use as many groups as you want, and group objects however feels intuitive."** · `phase1_instr2` (full screen, no inset)  
3. **"Click to place each object — Enter locks. You can't change previous answers after submitting. Hit Enter to start!"** · `phase1_instr3` (mini-grid inset)

**TTL:** `phase1_instr1_*`, `phase1_instr2_*`, `phase1_instr3_*`

**Task:** One task **`.bmp`** per trial; miniature grid inset bottom-right throughout; gray hint **"Click to place — Enter submits."** Matte / transparency: **`TASK_DESCRIPTION.md`**.

**TTL / CSV:** `phase1_stimulus_*`, `phase1_click_place`, `phase1_enter_submit`, `phase1_placements_saved`, `phase1_complete`, **`phase1_{participant}_{YYYYMMDD_HHMMSS}.csv`**.

---

### Phase 2 — Context incorporation

Each **recorded trial** shows this **timed sequence**: **context 1** → **same task object (BMP)** → **first cue dot** → **context 2** → **same object again** → **second cue dot** → **choice screen** (participant-paced). Participants **say aloud** a label **each time** a cue dot appears (**two** spoken passes per trial). **←** / **→** apply **only** on the final choice screen (**left** = label under **`context_1`**, **right** = **`context_2`**). Main prompt only: **"Which context fits best? Use the left/right keys to choose."** (no separate gray arrow subtitle).

**Cue dot appearance:** On screen the dots are **black** PsychoPy **`Circle`** stimuli (**`fillColor='black'`**) in both the Phase 2 tutorial and main trials. TTL labels **`phase2_reddot_*`**, **`phase2_reddot2_*`**, **`phase2_tutorial_reddot*`**, and timing constants such as **`PHASE2_REDDOT_DURATION_SEC`** are **historical names**—not red graphics.

**Instructions (5 screens)** before the Phase 2 demo (verbatim copy):  
1. **"Ask the experimenter if you have any questions!"** · `phase2_questions`  
2. **"For the next part of the task, we will show you a demo first. For this part, you will see each object paired with two contexts."** · `phase2_instr1`  
3. **"You will see: a context → object → dot."** · `phase2_instr2`  
4. **"When you see the dot, say what the object might be in that context aloud. Then, use the left/right keys to choose which context fits best."** · `phase2_instr3`  
5. **"The experimenter will record your responses, but don't panic. Just do your best and feel free to re-use answers."** · `phase2_instr4`

**Experimenter note:** **`phase2_instr2`** compresses the sequence into one **context → object → dot** clause; participants actually see **two** such passes (**two contexts**, **two dots**, **same object twice**) before the choice—mirror of **`TASK_DESCRIPTION.md`** / **`csv_documentation.md`** (**`phase2_context1_*`** … **`phase2_reddot2_*`**).

**TTL:** `phase2_questions_*` … `phase2_instr4_*`

**Tutorial:** **"Watch this demo before you start the task!"** · `phase2_tutorial_intro` (min **`PHASE2_INSTR5_MIN_SEC`** before Enter) · fixation · practice **context** PNGs (large **square**, center **cover** crop per **`TASK_DESCRIPTION.md`**) · blue **circle** · **black** cue dots (same visual style as recorded trials) · **"You might say the circle is a 'PLANET'"** / **"'BALL'"** · choice: same main prompt + **SPACE** \| **CIRCUS** → TTL **`phase2_tutorial_question_onset`**, timed preview, then **`phase2_tutorial_question_preview_offset`**, then timed highlight of **CIRCUS** (**right** button, steel blue) + subtitle **"You might say 'CIRCUS' (right key) is the better context"** (**`phase2_tutorial_demo_select_*`**, **`phase2_tutorial_response`**) → post-blank → **"Ready for recorded trials?"** · `phase2_ready` (Enter + **"Enter to continue."**)

**TTL:** through **`phase2_tutorial_*`**, **`phase2_ready_*`**, **`phase2_before_trials_*`**.

**Before recorded trials:** **"Ask the experimenter if you have any questions — Enter to start."** · `phase2_before_trials`

**Recorded trials:** Timed **context 1 → object → black dot → context 2 → object → black dot → choice**; **break** every **16** trials · **`phase2_break`**. Trial list: **`phase2_trial_order.csv`**.

**TTL / CSV:** `phase2_fixation_*` … `phase2_complete`, **`phase2_{participant}_{YYYYMMDD_HHMMSS}.csv`**.

**Experimenter:** remind **←** / **→** on choice screens if needed.

---

### Phase 3 — Re-sort post-context

**Instructions:**  
1. **"Ask the experimenter if you have any questions!"** · `phase3_questions`  
2. **"Now you will sort the objects again — like you did right in the beginning. See all the objects first."** · `phase3_instr1`  
3. **"Use whatever grouping method feels intuitive to you."** · `phase3_instr2`

**TTL:** `phase3_questions_*`, `phase3_instr1_*`, `phase3_instr2_*`

**Before grid:** **"You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize."** · `phase3_before_grid`

**TTL:** `phase3_before_grid_*`

**Grid / fixation:** Same as Phase 1 (`ShapeGrid_4x4_bmp.png` + bottom-right inset).

**TTL:** `phase3_grid_*`, `phase3_fixation_*`

**Instruction (mini-grid):** **"As before, sort the objects. Click to place — Enter locks."** · `phase3_instruction2c`

**TTL:** `phase3_instruction2c_*`

**Task:** Same as Phase 1 pattern: one **`.bmp`** per trial, inset, hint **"Click to place — Enter submits."**; object order **≠** Phase 1 (**`TASK_DESCRIPTION.md`**).

**TTL / CSV:** `phase3_stimulus_*`, `phase3_click_place`, `phase3_enter_submit`, `phase3_placements_saved`, `phase3_complete`, **`phase3_{participant}_{YYYYMMDD_HHMMSS}.csv`**.

**Debrief (3 questions):** **←** = **Yes**, **→** = **No** (not mouse). Bottom hint: **USE THE ARROW KEYS TO ANSWER**. **Yes** / **No** beside green / red rectangles.  
1. **"Did you group the objects differently the second time around?"**  
2. **"Did the contexts you saw change your grouping the second time?"**  
3. **"Did you see the objects differently the second time grouping them than you did when you first saw them?"**

**TTL:** per question: `phase3_debrief_onset` → `phase3_debrief_response` (`trial_info`: `answer=Yes|No`, `key=left|right`) → `phase3_debrief_offset`  
**CSV:** **`debrief_{participant}_{YYYYMMDD_HHMMSS}.csv`**

**After debrief (log order):** `summary_saved` → `experiment_end` → `thanks_onset` / `thanks_offset`

---

### End

**Display:** **"Done. Thank you!"** (**`THANKS_SCREEN_SEC`** s)

**TTL:** `summary_saved` · `experiment_end` · `thanks_onset` · `thanks_offset`

---

**Escape (`escape_pressed`):** `trial_info` is `screen=<label>` on **`wait_for_continue`** screens (`welcome`, `tutorial_transition`, `phase1_questions`, `phase1_before_grid`, `phase1_instr1` … `phase1_instr3`, `phase2_questions`, `phase2_instr1` … `phase2_instr4`, `phase2_tutorial_intro`, `phase2_ready`, `phase2_before_trials`, `phase2_break`, `phase3_questions`, `phase3_instr1`, `phase3_instr2`, `phase3_before_grid`, `phase3_instruction2c`) **or** fixed strings: `participant_name`, `tutorial_video`, `phase1_click_place`, `phase3_click_place`, `phase2_question`, `phase3_debrief`. Complete `screen=` list: **`csv_documentation.md`** (`escape_pressed` row).

---

## Notes

If Phase 2 speech is faint, cue: **say the label aloud**, **then (← / →)**.
