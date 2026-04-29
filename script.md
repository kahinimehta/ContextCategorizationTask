# Experimenter Script — run sheet

Purpose: verbatim screen copy plus abbreviated TTL names (full TTL table **`csv_documentation.md` only**). Timings/constants and **`phase2_trial_order.csv`:** **`TASK_DESCRIPTION.md`** (**`README.md`** → Documentation summarizes file roles).

**Operational:** `python context_shape_task.py` from task folder; **`../LOG_FILES/`**; participant name **`test`** → no saved files; **`PSYCHOPY_WINDOWED=1`** windowed (**1280×720**); **`PSYCHOPY_DUMMY_WINDOW=0`** disables the extra stability window; **`PSYCHOPY_CHECK_TIMING=1`** enables startup frame calibration (macOS rarely). **ESC** only during interactive canvases; macOS timing/keyboard/focus quirks **`TASK_DESCRIPTION.md`**. Instruction prompts end with **Enter to continue**; avoid accidental double Enter when laggy.

---

## Full Experiment Script

### Participant Login

**Display:** Instruction **Enter your name** (upper); centered typed characters + **`_`** cursor. **Enter** submits; **ESC** quits. Keyboard: **`event.getKeys()`** with an unrestricted poll, then local filtering (alphanumeric, backspace, **`return`** / **`enter`** / numpad Enter variants, **`escape`**); Darwin focus quirks **`TASK_DESCRIPTION.md`**.

**TTL:** participant_name_onset, participant_name_offset

---

### Welcome

**Display:** "Welcome — watch the example, then Continue."

**TTL:** welcome_onset, welcome_enter, welcome_offset

---

### Tutorial

**Training demo (fallback):** Red square + circles; **groups by color** (reds left cluster, green apart). **`STIMULI/tutorial_video.mp4`**, when present and playable, replaces this TTL stream—video subtitles/overlays **should mirror** captions below where applicable.

**Video** (`tutorial_video.mp4`): motion carries meaning; captions need not step line-for-line with fallback but keep **5a–6** gist.

**Fallback** (timing **`TASK_DESCRIPTION.md`**, Tutorial fallback subsection):

**Step 1** (`trial_info`: `step=1`): "Watch how we sort these shapes."

**Step 2** (`tutorial_fallback_step2_*`): "First let's place the red square to the left."

**Step 3** (`tutorial_fallback_step3_*`): "Let's group the red circle with the red square and place it to the left."

**Step 4** (`tutorial_fallback_step4_*`): "Let's place the green circle to the right (different group)."

**Step 5a** (`step=5a`): "See how we ended up sorting by color (but could have sorted by shape?)"

**Step 5b** (`step=5b`): "We created groups, not a spectrum - nearby objects share a group."

**Step 6** (`trial_info`: `step=6`): Upper: "A group does not have to pack tight— a large spread is OK." Lower: "Click to place — Enter submits each placement."

**Transition:** "Your turn to group some objects! Remember the same rules."

**TTL:** **`tutorial_video_*`** **or** **`tutorial_fallback_*`** / **`tutorial_fallback_step{2|3|4}_{center|target}_*`** (`step=1`|`2`|`3`|`4`|`5a`|`5b`|`6`); **`tutorial_transition_*`**. Exhaustive **`event_label`** list: **`csv_documentation.md`**.

---

### Phase 1 — Object sorting

**Instructions (3 screens):**
1. "Ask the experimenter if you have any questions!" · **`phase1_questions`**
2. "You will now sort some objects." · **`phase1_instr1`**
3. "Use as many groups as you want, and group objects however feels intuitive." · **`phase1_instr4`**

**TTL:** phase1_questions_* … phase1_instr4_*

**Before grid:** "You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize."

**TTL:** phase1_before_grid_*

**Grid / fixation:** `ShapeGrid_4x4_bmp.png`; miniature grid inset bottom-right (timings **`TASK_DESCRIPTION.md`**).

**TTL:** phase1_grid_* , phase1_fixation_*

**Instruction (mini-grid):** "Click to place each object — Enter locks. You can't change previous answers after submitting. Hit Enter to start!"

**TTL:** phase1_instruction2c_*

**Task:** One object per trial (**`STIMULI/shapes`** `.bmp`; near-white matte **stripped at load** — **`TASK_DESCRIPTION.md`**). Mini-grid persists; **`run_drag`** hint strip: "**Click to place — Enter submits.**"

**TTL / CSV:** **`csv_documentation.md`** (`phase1_stimulus_*`, `phase1_click_place`, **`phase1_complete`**, placements PNGs).

---

### Phase 2 — Context incorporation

Cue speech on dot; **`phase2`** questions use **`←`**/**`→`** (left = first label / **`context_1`**, right = **`context_2`**) · on-screen cue **"Better context?"** · hint strip **"← or → arrow"**.

**Instructions (6 screens):** screen 6 (**`phase2_instr5`**) has a **minimum 5 s** before Enter (`PHASE2_INSTR5_MIN_SEC`).
1. "Ask the experimenter if you have any questions!" · **`phase2_questions`**
2. "For the next part of the task, we will show you a demo first. For this part, you will see each object paired with two contexts." · **`phase2_instr1`**
3. "You will see: a context → object → dot." · **`phase2_instr2`**
4. "When you see the dot, say what the object might be in that context aloud. Then, use the left/right keys to choose which context fits best." · **`phase2_instr2b`**
5. "The experimenter will record your responses, but don't panic. Just do your best and feel free to re-use answers." · **`phase2_instr3`**
6. "Watch this demo before you start the task!" · **`phase2_instr5`**

**TTL (instructions):** **`phase2_questions_*`** … **`phase2_instr5_*`** (includes **`phase2_instr2b_*`**).

**Tutorial (after screen 6):** Intro: "Space scene → circle → circus scene. Name the object aloud; then we choose which fits." · fixation · two practice **context** images (fixed 16∶9 frame, center **cover** crop — same on-screen size for every context) · blue **circle** demo shape · red-dot + example lines · **`Better context?`** SPACE \| CIRCUS · highlight line **e.g., CIRCUS** · blank · **`Ready for recorded trials?`** (with Continue control as on other Enter screens).

**TTL (Phase 2 tutorial + handoff):** **`phase2_tutorial_intro_*`**; **`phase2_tutorial_fixation_*`** … **`phase2_tutorial_post_blank_*`**; **`phase2_ready_*`**; **`phase2_before_trials_*`** — full list **`csv_documentation.md`**.

**Before trials:** "Questions? Enter to start."

**Task:** fixation → contexts/objects/dots (**black** cue) → **`Better context?`** (**←**/**→**) → ITI (**`TASK_DESCRIPTION.md`**). Context scenes: same fixed frame (large height per **`PHASE2_CONTEXT_MAX_EXTENT`**, width from aspect ratio constant in code). Breaks **every 16** trials (**64**-trial template ⇒ **16**, **32**, **48**).

**TTL (trials + breaks):** **`phase2_fixation_*`** through trial/ITI events (**`csv_documentation.md`**); **`phase2_break_*`** between trial blocks; **`phase2_complete`**.

Experimenter: prompt speech plus valid keys when needed.

---

### Phase 3 — Re-sort post-context

**Instructions (3):**
1. "Ask the experimenter if you have any questions!" · **`phase3_questions`**
2. "Now you will sort the objects again — like you did right in the beginning. See all the objects first." · **`phase3_instr1`**
3. "Use whatever grouping method feels intuitive to you." · **`phase3_instr4`**

**Before grid:** "You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize."

**Instruction mini-grid:** "As before, sort the objects. Click to place — Enter locks."

**Debrief Yes/No (3):**
1. "Same grouping style as Phase 1?"
2. "Did contexts sway round-2 groups?"
3. "See objects differently the second sort?"

**TTL / CSV:** per **`csv_documentation.md`** (**`phase3_questions_*`** … **`phase3_instr4_*`**; **`phase3_before_grid_*`**; **`phase3_grid_*`** / **`phase3_fixation_*`**; **`phase3_instruction2c_*`**; **`phase3_stimulus_*`**, **`phase3_click_place`**, **`phase3_enter_submit`**, **`phase3_complete`**, **`phase3_placements_saved`**; **`phase3_debrief_*`**).

---

### End

**Display:** "Done. Thank you!" (2 **`THANKS_SCREEN_SEC`** s)

**TTL:** summary_saved · experiment_end · thanks_*

---

**Escape (`escape_pressed`) screens:** `screen=<label>` from **`wait_for_continue`** (`welcome`, **`tutorial_transition`**, **`phase*_questions`**, **`phase*_instr*`**, **`phase*_before_grid`**, **`phase*_instruction2c`**, **`phase2_before_trials`**, **`phase2_ready`**, **`phase2_break`**), plus **`participant_name`**, **`tutorial_video`**, **`phase1_click_place`** / **`phase3_click_place`**, **`phase2_question`**, **`phase3_debrief`**. Full list **`csv_documentation.md`**.

---

## Notes

If Phase 2 speech is faint, cue: **say the label aloud**, **then (←/→)**.
