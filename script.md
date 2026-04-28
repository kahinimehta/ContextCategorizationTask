# Experimenter Script

On-screen wording, phase sequence, TTL **names** (not the full lookup table).

| Doc | Use |
|-----|-----|
| **`README.md`** | Repo layout, Quick Start |
| **`TASK_DESCRIPTION.md`** | Durations/constants, paths, **`phase2_trial_order.csv`**, troubleshooting |
| **`csv_documentation.md`** | Output column definitions; complete TTL/code list |

**Instruction screens** include **Enter to continue** at the bottom. Avoid double-Enter during laggy screens.

### Quick reminders

- **`python context_shape_task.py`** from task directory; participant name (**`test`** in name → **no saved files**)
- **ESC** only during **interactive** screens (not grid / fixation / timed stimulus trains)
- Data under **`../LOG_FILES/`**; **`PSYCHOPY_WINDOWED=1`** for windowed 1280×720

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

**Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png`, 5 s. **Fixation:** black cross, 1 s.

**TTL:** phase1_grid_onset/offset, phase1_fixation_onset/offset

**Instructions (2 screens):**
1. "Sort by where you'd expect to see the shapes"
2. "Click somewhere to place, then press Enter to submit. Once you've submitted the position of a shape, you can't move it again. Ask the experimenter now if you need help."

**TTL:** phase1_instruction2a/2c_onset/enter/offset

**Task:** 16 shapes (`.bmp` in `STIMULI/shapes/`), one at a time in random order. 1 s display, then clickable. A miniature full grid (`ShapeGrid_4x4_bmp.png`) is shown in the **bottom-right** for the full click-to-place block (all 16 trials). At least one click required before Enter. Hint: "Click somewhere to place, then press Enter to submit."

**TTL:** phase1_stimulus_onset/offset (trial_info: trial=N, shape=…), phase1_click_place (each click), phase1_enter_submit, phase1_placements_saved (after each shape). **CSV:** all clicks in all_click_ttl; click_ttl = last click timestamp.

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

**TTL:** phase2_questions_onset/enter/offset, phase2_instr1_onset/enter/offset, phase2_instr2_onset/enter/offset, phase2_instr2b_onset/enter/offset, phase2_instr3–5_onset/enter/offset

**Tutorial:** After intro (**Enter**): fixation (**~0.5 s**) → images **`practice1.png`** / **`practice2.png`** (**`STIMULI/`** or **`contexts/`**) → blue circle intervals → PLANET cue on red dot (**~2 s**) → second context + circle sequence → BALL cue (**~2 s**) → **Which context fits the object better?** with SPACE \| CIRCUS → highlight + "You might select CIRCUS" → post-demo blank → Ready (**Enter**). Exact seconds: **`TASK_DESCRIPTION.md`** (Phase 2 tutorial table).

**Before trials:** "Ask the experimenter now if you have any questions. Press Enter when you're ready to begin." (1 Enter)

**TTL (tutorial & before trials):** `phase2_tutorial_*`, `phase2_ready_*`, `phase2_before_trials_*`—see csv_documentation.md.

**Task:** Fixed CSV order (**64** trials in shipped file; **`stderr`** prints `Phase 2: N trials from phase2_trial_order.csv`). Timeline: fixation → contexts/shapes/blanks/red dots → question **Which context fits the object better?** → ITI. Timing constants **`TASK_DESCRIPTION.md`**.

**Breaks:** After every **16** trials (**16**, **32**, **48**) for the shipped length; breaks scale with **`N`** if you lengthen the CSV.

Experimenter to nudge them if they are not speaking out loud/ not doing their best. 

**TTL (trials & breaks):** `phase2_fixation` through `phase2_trial_iti`, `phase2_break_*`, `phase2_complete`; `phase2_response` on choice. Trial `trial_info`: trial, shape, cat_a, cat_b, variant—full labels in csv_documentation.md.

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

**Grid:** `STIMULI/shapes/ShapeGrid_4x4_bmp.png`, 5 s. **Fixation:** black cross, 1 s.

**TTL:** phase3_grid_onset/offset, phase3_fixation_onset/offset

**Instructions (2 screens):**
1. "Sort by where you'd expect to see the shapes"
2. "Click somewhere to place, then press Enter to submit. Once you've submitted the position of a shape, you can't move it again. Ask the experimenter now if you need help."

**TTL:** phase3_instruction2a/2c_onset/enter/offset

**Task:** Same as Phase 1 (including miniature full grid in the bottom-right during click-to-place). Shapes in different random order than Phase 1. At least one click required before Enter. Hint: "Click somewhere to place, then press Enter to submit."

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

