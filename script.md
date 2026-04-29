# Experimenter Script — run sheet

**Roles:** **`script.md`** (this file) = verbatim copy + run order + example TTL names. **`TASK_DESCRIPTION.md`** = `*_SEC`, paths, **`phase2_trial_order.csv`**, troubleshooting. **`csv_documentation.md`** = full **`ttl_log_*`** + **`*.csv`** schema (**authoritative** for event spellings).

**Operational:** `python context_shape_task.py` from task folder; **`../LOG_FILES/`**; no saves if **`test`** in name. **`PSYCHOPY_WINDOWED=1`** → 1280×720; **`PSYCHOPY_DUMMY_WINDOW=0`**; **`PSYCHOPY_CHECK_TIMING=1`** enables frame calibration (macOS: rarely needed). **ESC** / keyboard quirks: **`TASK_DESCRIPTION.md`**. Gray **Enter to continue** on **`wait_for_continue`** screens.

---

## Full Experiment Script

### Participant Login

**Display:** **Enter your name** (upper); centered entry + **`_`** cursor. **Enter** submits; **ESC** quits. Key handling: **`TASK_DESCRIPTION.md`** (macOS / unrestricted poll).

**TTL:** participant_name_onset, participant_name_offset

---

### Welcome

**Display:** "Welcome to your task! — Hit Enter to watch the tutorial video."

**TTL:** welcome_onset, welcome_enter, welcome_offset

---

### Tutorial

**Training demo (fallback):** Red square + circles; **groups by color** (reds left cluster, green apart). **`STIMULI/tutorial_video.mp4`**, when present and playable, replaces this TTL stream—video subtitles/overlays **should mirror** captions below where applicable.

**Video** (`tutorial_video.mp4`): motion carries meaning; captions need not step line-for-line with fallback but keep **5a–6** gist.

**Fallback** (timing **`TASK_DESCRIPTION.md`**, Tutorial fallback subsection):

**Step 1** (`trial_info`: `step=1`): "The first part of the task is about sorting shapes. Watch how we sort these shapes!"

**Step 2** (`tutorial_fallback_step2_*`): "First, let's click to place the red square on the left — Then, we hit Enter."

**Step 3** (`tutorial_fallback_step3_*`): "Now, let's group the red circle with the red square on the left."

**Step 4** (`tutorial_fallback_step4_*`): "Let's place the green circle to the right (in a different group)."

**Step 5a** (`step=5a`): "See how we ended up sorting by color? We could have sorted by shape too — there are no wrong answers here!"

**Step 5b** (`step=5b`): "We created groups, not a spectrum — nearby objects share a group."

**Step 6** (`trial_info`: `step=6`): "Click to place — Enter submits each placement." *(Upper “large spread is OK” line exists in code only as a comment; not shown.)*

**Transition:** "Your turn to group some objects! — Remember the same rules."

**TTL:** **`tutorial_video_*`** or **`tutorial_fallback_*`** (+ **`tutorial_fallback_step{2|3|4}_{center|target}_`** for steps 2–4, plus `step=1`…`6` bundles on **`tutorial_fallback_*`**); **`tutorial_transition_*`**. Full list: **`csv_documentation.md`**.

---

### Phase 1 — Object sorting

**Instructions (1 screen before grid):**
1. "Ask the experimenter if you have any questions!" · **`phase1_questions`**

**TTL:** phase1_questions_*

**Before grid:** "You will now see all 16 objects you will be sorting at the same time — for reference only; just watch & don't memorize."

**TTL:** phase1_before_grid_*

**Grid / fixation:** `ShapeGrid_4x4_bmp.png` + bottom-right inset (**`TASK_DESCRIPTION.md`**).

**TTL:** `phase1_grid_*`, `phase1_fixation_*`

**After fixation:** *(in order)*  
1. "Now, group these objects like in the demo." · **`phase1_instr1`** (mini-grid)  
2. "Use as many groups as you want, and group objects however feels intuitive." · **`phase1_instr2`** (full screen)  
3. "Click to place each object — Enter locks. You can't change previous answers after submitting. Hit Enter to start!" · **`phase1_instr3`** (mini-grid)  

**TTL:** phase1_instr1_* · phase1_instr2_* · phase1_instr3_*

**Task:** One `.bmp` per trial (mini-grid; hint **"Click to place — Enter submits."**). Object matte / transparency: **`TASK_DESCRIPTION.md`**.

**TTL / CSV:** **`csv_documentation.md`** (sorting trials + placements).

---

### Phase 2 — Context incorporation

Cue speech on dot; **`phase2`** recorded trials use **`←`**/**`→`** (left = first label / **`context_1`**, right = **`context_2`**) · on-screen prompt **"Which context fits best? Use the left/right keys to choose."** · hint strip **"← or → arrow"**.

**Instructions (5 screens)** before the Phase 2 demo:
1. "Ask the experimenter if you have any questions!" · **`phase2_questions`**
2. "For the next part of the task, we will show you a demo first. For this part, you will see each object paired with two contexts." · **`phase2_instr1`**
3. "You will see: a context → object → dot." · **`phase2_instr2`**
4. "When you see the dot, say what the object might be in that context aloud. Then, use the left/right keys to choose which context fits best." · **`phase2_instr3`**
5. "The experimenter will record your responses, but don't panic. Just do your best and feel free to re-use answers." · **`phase2_instr4`**

**TTL (instruction block):** **`phase2_questions_*`** … **`phase2_instr4_*`**.

**Tutorial (after instructions):** Intro: **"Watch this demo before you start the task!"** · **`phase2_tutorial_intro`** (minimum **`PHASE2_INSTR5_MIN_SEC`** before Enter) · fixation · two practice **context** images (large **centered square**, center **cover** crop) · blue **circle** · black cue **dots** · **"You might say the circle is a 'PLANET'"** / **"'BALL'"** · choice screen: **"Which context fits best? Use the left/right keys to choose."** + **SPACE** \| **CIRCUS** (timed preview, then scripted highlight + bottom line **"You might say 'CIRCUS' (right key) is the better context"**) · blank · **"Ready for recorded trials?"** · Enter to continue ( **`phase2_ready`** ).

**TTL (tutorial → handoff):** intro → fixation → … → post-blank → **`phase2_ready_*`** → **`phase2_before_trials_*`** — **`csv_documentation.md`**.

**Before trials:** "Ask the experimenter if you have any questions — Enter to start."

**Task:** Timed context / object / **black** cue epochs, then **same choice screen** (**←**/**→**) + **"← or → arrow"** hint; **break** every **16** trials (**`phase2_break`**). Durations / framing: **`TASK_DESCRIPTION.md`**.

**TTL (trials):** **`phase2_fixation_*`** … **`phase2_complete`** — **`csv_documentation.md`**.

Experimenter: cue speech on dot; remind **←** / **→** on choice screens.

---

### Phase 3 — Re-sort post-context

**Instructions (3):**
1. "Ask the experimenter if you have any questions!" · **`phase3_questions`**
2. "Now you will sort the objects again — like you did right in the beginning. See all the objects first." · **`phase3_instr1`**
3. "Use whatever grouping method feels intuitive to you." · **`phase3_instr2`**

**Before grid:** "You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize."

**TTL:** phase3_before_grid_*

**Grid / fixation:** `ShapeGrid_4x4_bmp.png` + miniature inset (same pattern as Phase 1; timings **`TASK_DESCRIPTION.md`**).

**TTL:** phase3_grid_* , phase3_fixation_*

**Instruction mini-grid:** "As before, sort the objects. Click to place — Enter locks." · **`phase3_instruction2c`**

**Debrief Yes/No (3):**
1. "Same grouping style as Phase 1?"
2. "Did contexts sway round-2 groups?"
3. "See objects differently the second sort?"

**TTL / CSV:** Phase 3 instructions through debrief — **`csv_documentation.md`**.

---

### End

**Display:** "Done. Thank you!" (2 **`THANKS_SCREEN_SEC`** s)

**TTL:** summary_saved · experiment_end · thanks_*

---

**Escape (`escape_pressed`) screens:** `screen=<label>` from **`wait_for_continue`** (`welcome`, **`tutorial_transition`**, **`phase*_questions`**, **`phase*_instr*`**, **`phase3_instruction2c`**, **`phase*_before_grid`**, **`phase2_before_trials`**, **`phase2_ready`**, **`phase2_break`**), plus **`participant_name`**, **`tutorial_video`**, **`phase2_tutorial_intro`**, **`phase1_click_place`** / **`phase3_click_place`**, **`phase2_question`**, **`phase3_debrief`**. Full list **`csv_documentation.md`**.

---

## Notes

If Phase 2 speech is faint, cue: **say the label aloud**, **then (←/→)**.
