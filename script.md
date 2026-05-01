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

**Training demo (fallback):** Red square + circles; **groups by color** (reds left cluster, green apart). Final demo placements are **not collinear** — red square and red circle sit left at **different heights**; green circle **right** (`sq_pos` / `circ_red_pos` / `circ_green_pos` in **`context_shape_task.py`**). **Step 1:** intro subtitle while **all three** demo shapes appear **together** on **`TUTORIAL_FB_OVERVIEW_SEC`** at **spread** overview coords (`ov_sq` / `ov_red` / `ov_green`), not stacked. **Center epoch (steps 2–4):** moving shape **only** — **no** expanding steelblue ring (**placement** feedback only on target). **Target epoch:** **`TUTORIAL_FB_TARGET_ANCHORS_PREVIEW_SEC`** with **anchors only** (moving shape hidden; step **2** is blank + subtitle); **then** light-blue double halo + steelblue click at **empty** coords + cursor (**moving shape still hidden**); **then** moving shape at **final** position. **Steps 3–4:** **`TUTORIAL_FB_SHAPE_PREFLASH_SEC`** new-shape flash on empty canvas (`tutorial_fallback_step{n}_preflash_*`), then center isolate (**prior placements not drawn**), then target as above. Steps **2** & **6** bottom subtitles = **`PHASE13_CLICK_ENTER_INSTRUCTION`**. **Cursor** = **triangle** + **narrow tail** along bisector (**`_make_tutorial_cursor`**). **No cursor** on preflash, center, or anchor-preview beat; cursor **only** during halo + steelblue pulse. If **`STIMULI/tutorial_video.mp4`** plays, it replaces this TTL stream—video subtitles **should mirror** the gist below where applicable.

**Video** (`tutorial_video.mp4`): motion carries meaning; captions need not match the fallback line-for-line but keep **5a–6** gist.

**Fallback** (durations **`TASK_DESCRIPTION.md`**, Tutorial fallback):

**Step 1** (`tutorial_fallback_onset` / `offset`, `trial_info: step=1`): **"The first part of the task is about sorting objects. Watch how we sort these objects!"** — **square**, **red circle**, and **green circle** visible **at once** for **`TUTORIAL_FB_OVERVIEW_SEC`** (spread layout).

**Step 2** (`tutorial_fallback_step2_*`): **`PHASE13_CLICK_ENTER_INSTRUCTION`** — **"Click where you want to place each object, then press Enter to confirm."**

**Step 3** (`tutorial_fallback_step3_*`): **"Now, let's group the red circle with the red square on the left."**

**Step 4** (`tutorial_fallback_step4_*`): **"Let's place the green circle to the right (in a different group)."**

**Step 5a** (`step=5a`): **"See how we ended up sorting by color? We could have sorted by shape too — there are no wrong answers here!"**

**Step 5b** (`step=5b`): **"We created groups, not a spectrum — nearby objects share a group."**

**Step 6** (`step=6`): **`PHASE13_CLICK_ENTER_INSTRUCTION`** — **"Click where you want to place each object, then press Enter to confirm."**  
*(A possible “large spread is OK” line exists only as a commented-out stim in code; not shown.)*

**Transition:** **"Your turn to group some objects! Remember the same rules."**

**TTL:** `tutorial_video_*` **or** `tutorial_fallback_*` (+ `tutorial_fallback_step{2|3|4}_{preflash|center|target}_*` — step **2** has **no** `preflash`; steps **3–4** include `preflash`), then `tutorial_transition_*`.

---

### Phase 1 — Object sorting

**Instructions (before grid):**  
1. **"Ask the experimenter if you have any questions!"** · `phase1_questions`

**TTL:** `phase1_questions_*`

**Code vs older drafts:** After the Phase 1 tutorial, **`main()`** runs **`phase1_questions`** then **`phase1_before_grid`** with **no** screens in between. In **`context_shape_task.py`**, three **`wait_for_continue`** entries (**"You will now sort some objects."**, **"Place one at a time (same as demo)."**, **"Group by proximity—not along a spectrum."**) are **commented out** inside **`p1_screens`** — they **never** appear and **must not** be confused with the **`phase1_instr1`** … **`phase1_instr3`** screens **after** fixation below (different copy, same TTL names would have collided if those lines were uncommented).

**Before grid:** **"You will now see all 16 objects you will be sorting at the same time — for reference only; just watch & don't memorize."** · `phase1_before_grid` · **Enter** ignored until **`PHASE13_BEFORE_GRID_MIN_SEC`** (**`TASK_DESCRIPTION.md`** timings).

**TTL:** `phase1_before_grid_*`

**Grid / fixation:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png` fullscreen + same composite as **miniature bottom-right** inset (**timings** **`TASK_DESCRIPTION.md`**).

**TTL:** `phase1_grid_*`, `phase1_fixation_*`

**After fixation (in order):**  
1. **"Now, group these objects like in the demo."** · `phase1_instr1` (mini-grid inset)  
2. **"Use as many groups as you want, and group objects however feels intuitive."** · `phase1_instr2` (full screen, no inset)  
3. **"Click where you want to place each object, then press Enter to confirm."** · `phase1_instr3` (mini-grid inset)

**TTL:** `phase1_instr1_*`, `phase1_instr2_*`, `phase1_instr3_*`

**Task:** One task **`.bmp`** per trial; miniature grid inset bottom-right throughout; gray bottom hint **"Click where you want to place each object, then press Enter to confirm."** (same wording as **`phase1_instr3`**). Matte / transparency: **`TASK_DESCRIPTION.md`**.

**TTL / CSV:** `phase1_stimulus_*`, `phase1_click_place`, `phase1_enter_submit`, `phase1_placements_saved`, `phase1_complete`, **`phase1_{participant}_{YYYYMMDD_HHMMSS}.csv`**.

---

### Phase 2 — Context incorporation

Each **recorded trial** shows this **timed sequence**: **context 1** → **same task object (BMP)** → **first object question** (**`PHASE2_OBJECT_QUESTION_TEXT`**, e.g. **"What is the object?"**) → **context 2** → **same object again** → **second object question** → **choice screen** (participant-paced). Participants **say aloud** what the object might be **each time** that question appears (**two** spoken passes per trial). **←** / **→** apply **only** on the final choice screen (**left** = label under **`context_1`**, **right** = **`context_2`**). Main prompt only: **"Which context fits best? Use the left/right keys to choose."** (no separate gray arrow subtitle).

**Object-question screen:** Text-only (**`TextStim`**), not a fixation dot — same **`PHASE2_OBJECT_QUESTION_TEXT`** in the Phase 2 tutorial (with extra demo lines below) and in recorded trials. TTL labels **`phase2_reddot_*`**, **`phase2_reddot2_*`**, **`phase2_tutorial_reddot*`**, and **`PHASE2_REDDOT_DURATION_SEC`** are **historical names** (legacy **black dot** cue).

**Experimenter:** To change the question wording on screen, edit **`PHASE2_OBJECT_QUESTION_TEXT`** in **`context_shape_task.py`** (keep **`phase2_instr2`** / **`phase2_instr3`** in sync if you change how you describe the task).

**Instructions (5 screens)** before the Phase 2 demo (verbatim copy):  
1. **"Ask the experimenter if you have any questions!"** · `phase2_questions`  
2. **"For the next part of the task, we will show you a demo first. For this part, you will see each object paired with two contexts."** · `phase2_instr1`  
3. **"You will see: a context → object → question asking what the object is."** · `phase2_instr2`  
4. **"When you see that question, say aloud what the object might be in that context. Then, use the left/right keys to choose which context fits best."** · `phase2_instr3`  
5. **"The experimenter will record your responses, but don't panic. Just do your best and feel free to re-use answers."** · `phase2_instr4`

**Experimenter note:** **`phase2_instr2`** compresses the sequence into one **context → object → question** clause; participants actually see **two** such passes (**two contexts**, **two question screens**, **same object twice**) before the choice—mirror of **`TASK_DESCRIPTION.md`** / **`csv_documentation.md`** (**`phase2_context1_*`** … **`phase2_reddot2_*`**).

**TTL:** `phase2_questions_*` … `phase2_instr4_*`

**Tutorial:** **"Watch this demo before you start the task!"** · `phase2_tutorial_intro` (min **`PHASE2_INSTR5_MIN_SEC`** before Enter) · fixation · practice **context** PNGs (large **square**, center **cover** crop per **`TASK_DESCRIPTION.md`**) · blue **circle** · **`PHASE2_OBJECT_QUESTION_TEXT`** + **"You might say the circle is a 'PLANET'"** / **"'BALL'"** · choice: same main prompt + **SPACE** \| **CIRCUS** → TTL **`phase2_tutorial_question_onset`**, timed preview, then **`phase2_tutorial_question_preview_offset`**, then timed highlight of **CIRCUS** (**right** button, steel blue) + subtitle **"You might think 'CIRCUS' (right key) is the better context"** (**`phase2_tutorial_demo_select_*`**, **`phase2_tutorial_response`**) → post-blank → **"Ready to start?"** · `phase2_ready` (Enter + **"Enter to continue."**)

**TTL:** through **`phase2_tutorial_*`**, **`phase2_ready_*`**, **`phase2_before_trials_*`**.

**Before recorded trials:** **"Ask the experimenter if you have any questions — Enter to start."** · `phase2_before_trials`

**Recorded trials:** Timed **context 1 → object → object question → context 2 → object → object question → choice**; **break** every **16** trials · **`phase2_break`**. Trial list: **`phase2_trial_order.csv`**.

**TTL / CSV:** `phase2_fixation_*` … `phase2_complete`, **`phase2_{participant}_{YYYYMMDD_HHMMSS}.csv`**.

**Experimenter:** remind **←** / **→** on choice screens if needed.

---

### Phase 3 — Re-sort post-context

**Instructions:**  
1. **"Ask the experimenter if you have any questions!"** · `phase3_questions`  
2. **"Now you will sort the objects again — like you did right in the beginning. See all the objects first."** · `phase3_instr1`  
3. **"Use whatever grouping method feels intuitive to you."** · `phase3_instr2`

**TTL:** `phase3_questions_*`, `phase3_instr1_*`, `phase3_instr2_*`

**Before grid:** **"You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize."** · `phase3_before_grid` · **Enter** ignored until **`PHASE13_BEFORE_GRID_MIN_SEC`** (**`TASK_DESCRIPTION.md`** timings).

**TTL:** `phase3_before_grid_*`

**Grid / fixation:** Same as Phase 1 (`ShapeGrid_4x4_bmp.png` + bottom-right inset).

**TTL:** `phase3_grid_*`, `phase3_fixation_*`

**Instruction (mini-grid):** **"Click where you want to place each object, then press Enter to confirm."** · `phase3_instruction2c`

**TTL:** `phase3_instruction2c_*`

**Task:** Same as Phase 1 pattern: one **`.bmp`** per trial, inset, gray hint **"Click where you want to place each object, then press Enter to confirm."**; object order **≠** Phase 1 (**`TASK_DESCRIPTION.md`**).

**TTL / CSV:** `phase3_stimulus_*`, `phase3_click_place`, `phase3_enter_submit`, `phase3_placements_saved`, `phase3_complete`, **`phase3_{participant}_{YYYYMMDD_HHMMSS}.csv`**.

**Debrief (3 questions):** **←** = **Yes**, **→** = **No** (not mouse). Bottom hint: **USE THE ARROW KEYS TO ANSWER**. **Yes** / **No** on green / coral rectangles — same layout as Phase 2 choice (**`TASK_DESCRIPTION.md`**).  
1. **"Did you group the objects differently the second time around?"**  
2. **"Did the contexts you saw change your grouping the second time?"**  
3. **"Did you see the objects differently the second time grouping them than you did when you first saw them?"**

**TTL:** per question: `phase3_debrief_onset` → `phase3_debrief_response` (`trial_info`: `answer=Yes|No`, `key=left|right`) → `phase3_debrief_offset`  
**CSV:** **`debrief_{participant}_{YYYYMMDD_HHMMSS}.csv`**

**After debrief (log order):** `summary_saved` → `experiment_end` → `thanks_onset` / `thanks_offset`

---

### End

**Display:** **"You did an amazing job with these objects. Thank you!"** (**`THANKS_SCREEN_SEC`** s)

**TTL:** `summary_saved` · `experiment_end` · `thanks_onset` · `thanks_offset`

---

**Escape (`escape_pressed`):** `trial_info` is `screen=<label>` on **`wait_for_continue`** screens (`welcome`, `tutorial_transition`, `phase1_questions`, `phase1_before_grid`, `phase1_instr1` … `phase1_instr3`, `phase2_questions`, `phase2_instr1` … `phase2_instr4`, `phase2_tutorial_intro`, `phase2_ready`, `phase2_before_trials`, `phase2_break`, `phase3_questions`, `phase3_instr1`, `phase3_instr2`, `phase3_before_grid`, `phase3_instruction2c`) **or** fixed strings: `participant_name`, `tutorial_video`, `phase1_click_place`, `phase3_click_place`, `phase2_question`, `phase3_debrief`. Complete `screen=` list: **`csv_documentation.md`** (`escape_pressed` row).

---

## Notes

If Phase 2 speech is faint, cue: **answer the object question aloud**, **then (← / →)**.
