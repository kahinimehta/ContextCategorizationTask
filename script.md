# Experimenter Script — run sheet

Purpose: verbatim screen copy plus abbreviated TTL names (full TTL table **`csv_documentation.md` only`). Timings/constants and **`phase2_trial_order.csv`:** **`TASK_DESCRIPTION.md`** (**`README.md`** → Documentation summarizes file roles).

**Operational:** `python context_shape_task.py` from task folder; **`../LOG_FILES/`**; participant name **`test`** → no saved files; **`PSYCHOPY_WINDOWED=1`** windowed (**1280×720**); **`PSYCHOPY_DUMMY_WINDOW=0`** disables the extra stability window; **`PSYCHOPY_CHECK_TIMING=1`** enables startup frame calibration (macOS rarely). **ESC** only during interactive canvases; macOS timing/keyboard quirks **`TASK_DESCRIPTION.md`**. Instruction prompts end with **Enter to continue**; avoid accidental double Enter when laggy.

---

## Full Experiment Script

### Participant Login

**Display:** "Enter your first name and last initial with no spaces/capitals:\n\nHit Enter when done."

Here, the experimenter should enter their anonymized name. 

**TTL:** participant_name_onset, participant_name_offset

---

### Welcome

**Display:** "Welcome! Let's get started. First, watch this example video of how we work on this task."

**TTL:** welcome_onset, welcome_enter, welcome_offset

---

### Tutorial

**Video:** `STIMULI/tutorial_video.mp4`. See `STIMULI/tutorial_video_spec.md`. Subtitles describe on-screen action; include "We ended up sorting by shapes (but could have sorted by color.)" and "Note that we are grouping into groups—not arranging on a line or spectrum."

**Fallback** (no video): Step 1 — "Three shapes appear. How can we sort them?"; Step 2 — red square center→left ("Red square appears. We might click to place it on the left."); Step 3 — red circle center→right ("Red circle appears. Clicking to place on the right."); Step 4 — green circle center→right ("Green circle appears. Clicking to place on the right."); Step 5a — "We ended up sorting by shapes (but could have sorted by color.)" + circles around groups; Step 5b — "Note that we are grouping into groups—not arranging on a line or spectrum. Shapes closer together are in the same group."; Step 6 — "Objects in a group can be farther apart while also being part of the same group: some shapes may appear to belong to a group more strongly than others" + "We click to place each shape and press Enter to submit each shape's position." (7 s)


**Transition:** "Now that we've seen a demo of how we work on this task, let's get started on your version!" (1 Enter)

**TTL:** tutorial_video_onset/offset or tutorial_fallback_onset/offset (step=1–6), tutorial_fallback_step2/3/4_center/target_onset/offset, tutorial_transition_onset/enter/offset

---

### Phase 1 — Bottom-Up Shape Classification

**Instructions (5 screens):**
1. "If you have any questions, ask the experimenter now."
2. "Let's sort some shapes. First you will see all of them."
3. "Then place them one at a time by clicking where you want each to go, as in the demo you just saw."
4. "Group them into groups—not on a spectrum or line. Shapes closer together are in the same group."
5. "Use as many groups as you need."

**TTL:** phase1_questions_onset/enter/offset, phase1_instr1–4_onset/enter/offset

**Before grid:** "You will now see 16 shapes. You do not need to memorize them, recreate this grid, or remember any of the shapes—you will see them all together just for context."

**TTL:** phase1_before_grid_onset/enter/offset

**Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png`, 5 s (large centered; **same miniature bottom-right inset** as in sorting). **Fixation:** black cross, 1 s (**miniature inset** still bottom-right).

**TTL:** phase1_grid_onset/offset, phase1_fixation_onset/offset

**Instructions (1 screen):**
1. "Click somewhere to place, then press Enter to submit. Once you've submitted the position of a shape, you can't move it again. A miniature picture of all 16 shapes in a grid will stay in the bottom-right corner for every trial—use it if it helps. Ask the experimenter now if you need help."

**TTL:** phase1_instruction2c_onset/enter/offset

**Task:** 16 shapes (`.bmp` in `STIMULI/shapes/`), one at a time in random order. **Miniature 4×4 grid** (**`ShapeGrid_4x4_bmp.png`**, aspect preserved) stays **bottom-right** from **grid preview** (with large grid) through **fixation**, **instruction** (screen above), then each shape’s **1 s preview** and **click-to-place** until this phase ends. Each shape is drawn at **native aspect ratio** (not forced square). At least one click required before Enter. Hint repeats instruction above.

**TTL:** phase1_stimulus_onset/offset (trial_info: trial=N, shape=…), phase1_click_place (each click), phase1_enter_submit, phase1_placements_saved (after each shape), **phase1_complete**. **CSV:** all clicks in all_click_ttl; click_ttl = last click timestamp.

---

### Phase 2 — Top-Down Context Incorporation

*Make sure they are speaking out loud when needed. Can remind them at breaks/in between as needed.*

**Instructions (7 screens; screen 7 min 5 s):**
1. "If you have any questions, ask the experimenter now."
2. "Now you'll see the shapes again, paired with different pictures or background contexts. Each shape appears with two context pictures."
3. "For each context-picture pair, you'll first see the context (for example a kitchen or a park scene), then the shape (like the ones you sorted before), and then a red dot."
4. "When the red dot is on screen, say out loud what the shape could be in that context—e.g., planet or ball. Then click which picture the shape fits better with. We need to hear you say it every time."
5. "Do your best since you will be recorded, but don't panic if nothing comes to mind. You will watch a demo before you have to do the task, so don't worry if this makes no sense yet."
6. "You can also re-use answers, but try to be creative if you can."
7. "Now let's watch a quick demo to help you understand how we work on this task."

**TTL:**
- Instructions (above): `phase2_questions_*` … `phase2_instr5_*` (**`phase2_instr5`** onset has min display **5 s** before Enter).
- Tutorial (**SPACE**/ **CIRCUS** demo — intro screen **`phase2_tutorial_intro`** first): `phase2_tutorial_*`, **`phase2_ready_*`** (“Ready…” after demo).
- Before Phase 2 trial list: **`phase2_before_trials_*`**.
- Each trial + mandatory breaks (**every 16** trials): **`phase2_fixation_*`** … **`phase2_trial_iti_*`**, **`phase2_break_*`**, **`phase2_complete`**, **`phase2_response`** (full **`event_label`** / **`trial_info`**: **`csv_documentation.md`**).

**Tutorial (after screen 7 — one Enter):**
- **Intro:** “You'll see a space picture, then a circle, then a circus picture. Say what the shape could be in each, then watch as we pick which fits better.” (**Enter**)
- **Sequence:** fixation **0.5 s** → first **`practice1.png`** **1 s** → blue circle **1 s** → blank **1 s** → red dot + “You might say the circle is a 'PLANET'” **2 s** → second **`practice2.png`** **1 s** → same circle **1 s** → blank **1 s** → red dot + “You might say the circle is a 'BALL'” **2 s** → **Which context fits the object better?** with **SPACE** | **CIRCUS** (initial **1.5 s**, then highlight) → **CIRCUS** highlighted + “You might select CIRCUS” **1 s** → blank **3 s** → **Ready:** “Ready to try this with some actual shapes and images?” (**Enter**). PNGs: **`STIMULI/`** or **`STIMULI/contexts/`** (see code). Exact constants: **`TASK_DESCRIPTION.md`**.

**Before trials:** “Ask the experimenter now if you have any questions. Press Enter when you're ready to begin.” (**Enter**)

**Task:** Trials follow **`phase2_trial_order.csv`** (**`stderr`:** `Phase 2: N trials …`). fixation → alternating contexts/shapes/red dots → question (**Which context fits the object better?**) → ITI (**timings/constants `TASK_DESCRIPTION.md`**). Mandatory breaks every **16** trials (**16**, **32**, **48** for the shipped **64** trials).

Experimenter to nudge them if they are not speaking out loud / not doing their best. 

---

### Phase 3 — Post-Context Shape Reclassification

**Instructions (5 screens):**
1. "If you have any questions, ask the experimenter now. Press Enter when you're ready."
2. "Now let's sort some shapes again, like we did in the VERY beginning. First you will see all of them."
3. "Then place them one at a time by clicking where you want each to go, as in the demo you saw earlier."
4. "Group them into groups—not on a spectrum or line. Shapes closer together are in the same group."
5. "Use as many groups as you need, and any grouping that is intuitive to you."

**TTL:** phase3_questions_onset/enter/offset, phase3_instr1–4_onset/enter/offset

**Before grid:** "As earlier, you will now see 16 shapes. You do not need to memorize them, recreate this grid, or remember any of the shapes—you will see them all together just for context."

**TTL:** phase3_before_grid_onset/enter/offset

**Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png`, 5 s (large centered; **same miniature bottom-right inset** as in sorting). **Fixation:** black cross, 1 s (**miniature inset** still bottom-right).

**TTL:** phase3_grid_onset/offset, phase3_fixation_onset/offset

**Instructions (1 screen):**
1. "Click somewhere to place, then press Enter to submit. Once you've submitted the position of a shape, you can't move it again. A miniature picture of all 16 shapes in a grid will stay in the bottom-right corner for every trial—use it if it helps. Ask the experimenter now if you need help."

**TTL:** phase3_instruction2c_onset/enter/offset

**Task:** Same structure as Phase 1: **miniature 4×4 grid** bottom-right from **grid preview** through **fixation**, **instruction** (screen above), each **1 s preview** and **click-to-place**; shapes at **native aspect ratio**. Shapes in a different random order than Phase 1. At least one click required before Enter. Hint matches instruction above.

**TTL:** phase3_stimulus_onset/offset (trial_info: trial=N, shape=…), phase3_click_place, phase3_enter_submit, phase3_placements_saved (after each shape), phase3_complete. **CSV:** all clicks in all_click_ttl; click_ttl = last click timestamp.

**Debrief (3 Yes/No questions):**
1. "Did you use the same grouping strategy as the first time you sorted these shapes?"
2. "Did the images associated with each shape you saw influence your grouping the second time around?"
3. "After thinking about how shapes might fit in different environments, did you find yourself interpreting the shapes differently when you sorted them the second time?"

**TTL:** phase3_debrief_onset, phase3_debrief_response, phase3_debrief_offset (per question)

---

### End

**Display:** "Thank you! Task complete." (2 s)

**TTL:** summary_saved (during write_summary), experiment_end, thanks_onset, thanks_offset

**Escape:** If participant presses ESC during any interactive screen, `escape_pressed` is logged (trial_info: screen=…). Logged before quit. Screens: participant_name, welcome, instruction screens (via wait_for_continue), tutorial_video, tutorial_transition, phase1/phase3_click_place, phase2_question, phase2_before_trials, phase2_break, phase3_debrief.

---

## Notes

If a participant barely speaks **Phase 2** prompts, cue them to label the shape aloud, then respond on screen.

