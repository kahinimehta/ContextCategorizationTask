# Experimenter Script — run sheet

Purpose: verbatim screen copy plus abbreviated TTL names (full TTL table **`csv_documentation.md` only`). Timings/constants and **`phase2_trial_order.csv`:** **`TASK_DESCRIPTION.md`** (**`README.md`** → Documentation summarizes file roles).

**Operational:** `python context_shape_task.py` from task folder; **`../LOG_FILES/`**; participant name **`test`** → no saved files; **`PSYCHOPY_WINDOWED=1`** windowed (**1280×720**); **`PSYCHOPY_DUMMY_WINDOW=0`** disables the extra stability window; **`PSYCHOPY_CHECK_TIMING=1`** enables startup frame calibration (macOS rarely). **ESC** only during interactive canvases; macOS timing/keyboard quirks **`TASK_DESCRIPTION.md`**. Instruction prompts end with **Enter to continue**; avoid accidental double Enter when laggy.

---

## Full Experiment Script

### Participant Login

**Display:** Typed id (centered) plus trailing cursor; **Enter** submits; **ESC** quits (see **`csv_documentation.md`**). No on-screen format instructions.

**TTL:** participant_name_onset, participant_name_offset

---

### Welcome

**Display:** "Welcome — watch the example, then Continue."

**TTL:** welcome_onset, welcome_enter, welcome_offset

---

### Tutorial

**Training demo (fallback):** Red square + circles; **groups by color** (reds left cluster, green apart). **`STIMULI/tutorial_video.mp4`**, when present and playable, replaces this TTL stream—video subtitles/overlays **should mirror** captions below where applicable.

**Video** (`tutorial_video.mp4`): motion carries meaning; captions need not step line-for-line with fallback but keep **5a–5c** gist.

**Fallback** (timing **`TASK_DESCRIPTION.md`**, Tutorial fallback subsection):

**Step 1** (`trial_info`: `step=1`): "Sort these—how? " *(trailing space in code)*  

**Step 2** (`tutorial_fallback_step2_*`): "Red square—with the reds left."

**Step 3** (`tutorial_fallback_step3_*`): "Red circle—next to the square."

**Step 4** (`tutorial_fallback_step4_*`): "Green—away from reds (new color group)."

**Step 5a** (`step=5a`): "We ended up sorting by color (but could have sorted by shape.)"

**Step 5b** (`step=5b`): "Groups, not a line—near things share a group."

**Step 6** (`trial_info`: `step=6`): Upper: "A group need not pack tight—spread is OK." Lower: "Click to place — Enter submits each placement."

**Transition:** "Your turn—same rules."

**TTL:** **`tutorial_video_*`** **or** **`tutorial_fallback_*`** / **`tutorial_fallback_step{2|3|4}_{center|target}_*`** (`step=1`|`2`|`3`|`4`|`5a`|`5b`|`6`); **`tutorial_transition_*`**. Exhaustive **`event_label`** list: **`csv_documentation.md`**.

---

### Phase 1 — Object sorting

**Instructions (5 screens):**
1. "Questions? Ask now."
2. "Sort objects—all on screen first."
3. "Place one at a time (same as demo)."
4. "Group by proximity—not along a spectrum."
5. "Use as many groups as you want."

**TTL:** phase1_questions_* … phase1_instr4_*

**Before grid:** "16 objects next — reference only; don't memorize."

**TTL:** phase1_before_grid_*

**Grid / fixation:** `ShapeGrid_4x4_bmp.png`; miniature grid inset bottom-right (timings **`TASK_DESCRIPTION.md`**).

**TTL:** phase1_grid_* , phase1_fixation_*

**Instruction (mini-grid):** "Click to place — Enter locks. Mini-grid bottom-right stays. Help? Ask."

**TTL:** phase1_instruction2c_*

**Task:** One object per trial (**`STIMULI/shapes`** `.bmp`; near-white matte **stripped at load** — **`TASK_DESCRIPTION.md`**). Mini-grid persists; **`run_drag`** hint strip: "**Click to place — Enter submits.**"

**TTL / CSV:** **`csv_documentation.md`** (`phase1_stimulus_*`, `phase1_click_place`, **`phase1_complete`**, placements PNGs).

---

### Phase 2 — Context incorporation

Cue speech on dot; **`phase2`** questions use **`←`**/**`→`** (left = first label / **`context_1`**, right = **`context_2`**) · on-screen cue **"Better context?"** · hint strip **"← or → arrow"**.

**Instructions (7; screen 7 ≥ **5** s via `phase2_instr5`):**
1. "Questions? Ask now."
2. "Each object paired with two contexts."
3. "Trial: scene → object → dot."
4. "On the dot: say a label aloud. ←/→ chooses fit — speak each trial."
5. "Recorded — demo runs first."
6. "Reuse OK; vary when possible."
7. "Watch demo next."

**TTL (instructions):** **`phase2_questions_*`** … **`phase2_instr5_*`**.

**Tutorial (after screen 7):** Intro: "Space scene → circle → circus scene. Name the object aloud; then we choose which fits." · timed demo (**TASK_DESCRIPTION.md**) · **`Better context?`** SPACE | CIRCUS · highlight line **e.g., CIRCUS** · **`Ready for recorded trials?`**

**TTL (Phase 2 tutorial + handoff):** **`phase2_tutorial_intro_*`**; **`phase2_tutorial_fixation_*`** … **`phase2_tutorial_post_blank_*`**; **`phase2_ready_*`**; **`phase2_before_trials_*`** — full list **`csv_documentation.md`**.

**Before trials:** "Questions? Enter to start."

**Task:** fixation → contexts/objects/dots (**black** cue) → **`Better context?`** (**←**/**→**) → ITI (**`TASK_DESCRIPTION.md`**). Breaks **every 16** trials (**64**-trial template ⇒ **16**, **32**, **48**).

**TTL (trials + breaks):** **`phase2_fixation_*`** through **`phase2_trial_iti_*`** (per trial); **`phase2_break_*`** between trial blocks; **`phase2_complete`** — details **`csv_documentation.md`**.

Experimenter: prompt speech plus valid keys when needed.

---

### Phase 3 — Re-sort post-context

**Instructions (5):**
1. "Questions? Enter when ready."
2. "Sort again — like Phase 1. See all objects first."
3. "Place one at a time (same as earlier)."
4. "Groups by proximity — not along a spectrum."
5. "Any intuitive grouping counts."

**Before grid:** "Same rule: 16 objects — reference grid only."

**Instruction mini-grid:** "Click to place — Enter locks. Mini-grid bottom-right stays. Help? Ask."

**Debrief Yes/No (3):**
1. "Same grouping style as Phase 1?"
2. "Did contexts sway round-2 groups?"
3. "See objects differently the second sort?"

**TTL / CSV:** per **`csv_documentation.md`** (**`phase3_questions_*`** … **`phase3_instruction2c_*`**; **`phase3_grid_*`** / **`phase3_fixation_*`**; **`phase3_stimulus_*`**, **`phase3_click_place`**, **`phase3_enter_submit`**, **`phase3_complete`**, **`phase3_placements_saved`**; **`phase3_debrief_*`**).

---

### End

**Display:** "Done. Thank you!" (2 **`THANKS_SCREEN_SEC`** s)

**TTL:** summary_saved · experiment_end · thanks_*

---

**Escape (`escape_pressed`) screens:** `screen=<label>` from **`wait_for_continue`** (`welcome`, **`tutorial_transition`**, **`phase*_questions`**, **`phase*_instr*`**, **`phase*_before_grid`**, **`phase*_instruction2c`**, **`phase2_before_trials`**, **`phase2_ready`**, **`phase2_break`**), plus **`participant_name`**, **`tutorial_video`**, **`phase1_click_place`** / **`phase3_click_place`**, **`phase2_question`**, **`phase3_debrief`**. Full list **`csv_documentation.md`**.

---

## Notes

If Phase 2 speech is faint, cue: **say the label aloud**, **then (←/→)**.
