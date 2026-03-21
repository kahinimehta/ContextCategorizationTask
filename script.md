# Experimenter Script

**Specs:** README.md. **CSV/TTL mapping:** `csv_documentation.md`.

**Convention:** Instruction screens: "Press Enter to continue" at bottom. Max 2 sentences per screen. TTL: `*_onset` (appeared), `*_enter` (keypress), `*_offset` (transition).

**ELI5 tips:** "Put" not "place"; "go together" not "group"; break into one idea at a time. Phase 1 & 3: "Things that go together go close." Phase 2: "Say out loud what it could be, then pick which picture fits better."

---

## Quick Start

1. Run `python context_shape_task.py` from task directory
2. Enter participant name (no spaces); Enter when done
3. **ESC** during interactive screens only—not during timed displays (grid, fixation, stimulus)
4. **Data:** `../LOG_FILES/` — date/time in filenames. Name contains "test" → no files.
5. **Windowed mode:** `PSYCHOPY_WINDOWED=1` (1280×720)

---

## Full Experiment Script

### Participant Login

**Display:** "Enter your first name and last initial with no spaces/capitals: Hit Enter when done."

**TTL:** participant_name_onset, participant_name_offset

---

### Welcome

**Display:** "Welcome! Let's get started. First, watch this example video of how we work on this task."

**TTL:** welcome_onset, welcome_enter, welcome_offset

---

### Tutorial

**Video:** `STIMULI/tutorial_video.mp4`. See `STIMULI/tutorial_video_spec.md`. Subtitles describe on-screen action; include "We sorted by shapes but could have sorted by color" and "Shapes closer together are in the same group."

**Fallback** (no video): Step 1 — three shapes; Step 2 — red square center→left; Step 3 — red circle center→right; Step 4 — green circle center→right (with red); Step 5a — sorted by shape, could sort by color (circles drawn around each group: square, two circles); Step 5b — groups, not line/spectrum; Step 6 — "Click to place. Press Enter to submit."

**Transition:** "Let's get started on your task!" (1 Enter)

**TTL:** tutorial_video_onset/offset or tutorial_fallback_onset/offset (step=1–6), tutorial_transition_onset/enter/offset

---

### Phase 1 — Bottom-Up Shape Classification

**Instructions (5 screens):**
1. "If you have any questions, ask the experimenter now. Press Enter when you're ready."
2. "Let's sort some shapes. First you will see all of them."
3. "Then place them one at a time by clicking where you want each to go, as in the demo you just saw."
4. "Group them into groups—not on a spectrum or line. Shapes closer together are in the same group."
5. "Use as many groups as you need."

**TTL:** phase1_questions_onset/enter/offset, phase1_instr1–4_onset/enter/offset

**Before grid:** "You will see 16 shapes. You do not need to memorize them, recreate this grid, or remember any of the shapes—you will see them all together just for context."

**TTL:** phase1_before_grid_onset/enter/offset

**Grid:** ShapeGrid_4x4_scrambled.png, 5 s. **Fixation:** black cross, 1 s.

**TTL:** phase1_grid_onset/offset, phase1_fixation_onset/offset

**Instructions (2 screens):**
1. "You'll see the shapes from before, one at a time. Group each where you think it belongs."
2. "Click to place, press Enter to submit. Once you've submitted the position of a shape, you can't move it again."

**TTL:** phase1_instruction2a/2c_onset/enter/offset

**Task:** 16 shapes, one at a time in random order. 1 s display, then clickable. Hint on screen: "Click to place. Press Enter to submit."

**TTL:** phase1_stimulus_onset/offset, phase1_click_place (each click), phase1_enter_submit, phase1_placements_saved (after each shape)

---

### Phase 2 — Top-Down Context Incorporation

*Make sure they are speaking out loud when needed. can remind them at breaks/ in between as needed.*

**Instructions (6 screens; screen 6 min 5 s):**
1. "If you have any questions, ask the experimenter now. Press Enter when you're ready."
2. "Now you'll see the shapes again, paired with different pictures. Each shape appears with two pictures."
3. "For each picture, you'll see the shape, then a red dot. When the red dot is on screen, say out loud what the shape could be in that context—e.g., planet or ball. Then click which picture the shape fits better with. We need to hear you say it every time."
4. "Do your best since you will be recorded, but don't panic if nothing comes to mind."
5. "You can also re-use answers."
6. "Let's watch a quick demo."

**TTL:** phase2_questions_onset/enter/offset, phase2_instr1–5_onset/enter/offset

**Tutorial:** "You'll see a space picture, then a circle, then a circus picture..." (1 Enter) → Fixation 500 ms → practice1 (space) → circle → blank → red dot 3 s + PLANET → practice2 (circus) → circle → blank2 → red dot 3 s + BALL → Question CIRCUS | SPACE (participant watches; CIRCUS highlighted + "You might select CIRCUS") → Blank 3 s → Ready (1 Enter).

**TTL:** phase2_tutorial_intro_onset/enter/offset, phase2_tutorial_fixation_onset/offset, phase2_tutorial_context1/shape/blank/reddot_onset/offset, phase2_tutorial_context2/shape2/blank2/reddot2_onset/offset, phase2_tutorial_question_onset/offset, phase2_tutorial_response, phase2_tutorial_post_blank_onset/offset, phase2_ready_onset/enter/offset

**Task:** Trial order from `phase2_trial_order.csv` (fixed for all participants). Per trial: Fixation 500 ms → Context 1 → Shape 1 s → Blank → Red dot 3 s → Context 2 → Shape 1 s → Blank → Red dot 3 s → Question (click A or B) → ITI 500 ms.

**Breaks:** Every 16 trials; "Take a break!" + progress bar.

**TTL:** phase2_fixation, phase2_context1/shape, phase2_blank1, phase2_reddot, phase2_context2/shape2, phase2_blank2, phase2_reddot2, phase2_question_onset, phase2_response, phase2_question_offset, phase2_trial_iti_onset/offset, phase2_break_onset/enter/offset, phase2_complete

---

### Phase 3 — Post-Context Shape Reclassification

**Instructions (5 screens):**
1. "If you have any questions, ask the experimenter now. Press Enter when you're ready."
2. "Let's sort some shapes again, like we did in the VERY beginning. Click to place each shape where you think it belongs."
3. "Again, shapes closer together are ones you're grouping as more similar."
4. "Feel free to use whatever grouping feels intuitive."
5. "Once you've submitted the position of a shape, you can't move it again."

**TTL:** phase3_questions_onset/enter/offset, phase3_instr1–4_onset/enter/offset

**Task:** Same as Phase 1 (no grid preview). Shapes in different random order than Phase 1. Hint: "Click to place. Press Enter to submit."

**TTL:** phase3_stimulus_onset/offset, phase3_click_place, phase3_enter_submit, phase3_placements_saved (after each shape), phase3_complete

**Debrief (3 Yes/No questions):**
1. "Did you use the same grouping strategy as the first time you sorted these shapes?"
2. "Did the images associated with each shape you saw influence your grouping the second time around?"
3. "After thinking about how shapes might fit in different environments, did you find yourself interpreting the shapes differently when you sorted them the second time?"

**TTL:** phase3_debrief_onset, phase3_debrief_response, phase3_debrief_offset (per question)

---

### End

**Display:** "Thank you! Task complete." (2 s)

**TTL:** summary_saved (during write_summary), experiment_end, thanks_onset, thanks_offset

**Escape:** If participant presses ESC during any interactive screen, `escape_pressed` is logged (trial_info: screen=…). Logged before quit. Screens: participant_name, instruction screens (via wait_for_continue), phase1/phase3_click_place, tutorial_video, phase2_question, phase3_debrief.

---

## Notes

- **Phase 2:** Enforce saying out loud. If quiet: "What could this shape be? Say it out loud."
- **Troubleshooting:** See TASK_DESCRIPTION.md (OOM, windowed mode, Mac TTL).
