# Experimenter Script

Full task specs: README.md. CSV/TTL: `csv_documentation.md`. Use "Simple version" when participants need plain language.

**Convention:** Instruction screens show "Press Enter to continue" at bottom. Max 2 sentences per screen. TTL: `*_onset` when screen appears, `*_enter` when Enter pressed, `*_offset` when screen transitions. Full TTL mapping: `csv_documentation.md`.

---

## Explaining to Participants (ELI5)

**Explain the task like participants are 5.** Use short sentences, simple words, and no jargon. If someone looks confused, slow down and rephrase in even simpler terms.

**General tips:**
- Use "put" instead of "place," "click" instead of "select," "go together" instead of "group"
- Break instructions into one idea at a time
- Check in: "Does that make sense?" or "Any questions before we start?"
- For Phase 1 & 3: "Things that go together go close together. Things that are different go far apart."
- For Phase 2: "What could this shape be in this picture? Say it out loud. Then pick which picture it fits better with."

---

## Quick Start

1. Open terminal in the task directory
2. Run: `python context_shape_task.py`
3. Enter participant name on the fullscreen prompt (like Social Recognition Task)
4. **ESC** exits at any time (no Exit button)

**Data saved to**: `../LOG_FILES/` (one level up from task folder). Filenames include date/time (e.g., `phase1_john_20250318_143022.csv`, `phase1_placements_john_20250318_143022.png`). No files written if name contains "test".

**Display:** Mac defaults to windowed (1280×720). Fullscreen: `PSYCHOPY_WINDOWED=0`. On Windows/Linux, windowed: `PSYCHOPY_WINDOWED=1`.

---

## Full Experiment Script

### Participant Login (fullscreen, like SRT)

**Display:** "Enter your first name and last initial with no spaces/capitals: Hit Enter when done."

**What to say:** "Type your name. No spaces. Enter when done."

**Simple version:** "Type your name. No spaces. Enter when finished."

**TTL:** participant_name_onset, participant_name_offset

---

### Welcome Screen

**Display says:**
"Welcome! Let's get started. First, watch this example video of how we work on this task."

**What to say:** "Welcome! Read the message."

**Simple version:** "Hi! Read what it says."

**TTL:** welcome_onset, welcome_enter, welcome_offset

---

### Tutorial — Video with subtitles

**Shapes:** Red square, red circle, green circle.

**Option A (video):** Place `STIMULI/tutorial_video.mp4` in the stimuli folder. See `STIMULI/tutorial_video_spec.md` for full production spec. The video shows click-to-place—shapes appearing and being clicked to place. **Subtitles describe what's on screen** (e.g., "Red square appears. Clicking to place on the left."), not instructions read aloud. Include: "We sorted by shapes but could have sorted by color." then "Shapes closer together are in the same group. Objects in a group can still be slightly further apart than from objects in another group." ESC exits.

**Option B (fallback):** If no video, a click-to-place sequence (no dragging) simulates the tutorial:
- Step 1: "Three shapes appear."
- Step 2: Red square appears at center, then at left: "Red square appears. Clicking to place on the left."
- Step 3: Red circle appears at center, then at right: "Red circle appears. Clicking to place on the right."
- Step 4: Green circle appears at center, then at right (next to red circle): "Green circle appears. Clicking to place on the right."
- Step 5a: "We sorted by shapes but could have sorted by color."
- Step 5b: "Shapes closer together are in the same group. Objects in a group can still be slightly further apart than from objects in another group."
- Step 6: "Click to place each shape. Press Enter to submit."

**What to say:** "Watch the tutorial. It shows click to place, Enter to submit."

**Simple version:** "Watch this short video. Click to put shapes where you want, press Enter when done."

**TTL:** tutorial_video_onset/offset or tutorial_fallback_onset/offset (step=1, 2, 3, 4, 5a, 5b, 6)

#### Debrief

**Display says:** "In this practice, we sorted all objects by shape!"

**What to say:** "Great! We sorted by shape."

**Simple version:** "Nice! We put the shapes that look alike together."

**TTL:** tutorial_debrief_onset, tutorial_debrief_enter, tutorial_debrief_offset

#### Transition

**Display says:** "Let's get started on your task!"

**What to say:** "Ready for the real task."

**Simple version:** "Now we'll do the real thing."

**TTL:** tutorial_transition_onset, tutorial_transition_offset

---

### Phase 1 — Bottom-Up Shape Classification

#### Instructions (split screens, max 2 sentences each; last screen min 8 s)

**Screen 1:** "Let's sort some shapes. First you will see all of them."

**Screen 2:** "Then place them one at a time by clicking where you want each to go, as in the practice."

**Screen 3:** "Shapes closer together are ones you're grouping as more similar. Use as many groups as you need." *(Enter after 8 s)*

**What to say:** "You'll see the full grid first, then place each shape one at a time. Click to move, Enter when happy. Things that go together go close."

**Simple version:** "First you'll see all the shapes. Then one by one, put each on the screen. Click to move, Enter when happy. Things that go together go close."

**Experimenter note:** Emphasize "Things that go together go close. Things that are different go far apart."

**TTL:** phase1_instr1–3_onset/enter/offset

#### Before grid (1 screen)

**Display:** "You will see 16 shapes. You do not need to memorize them, recreate this grid, or remember any of the shapes—you will see them altogether just for context."

**TTL:** phase1_before_grid_onset, phase1_before_grid_enter, phase1_before_grid_offset

#### Grid display

ShapeGrid_4x4.png for 5 seconds

**TTL:** phase1_grid_onset, phase1_grid_offset

#### Fixation

Black cross, 1 second

**TTL:** phase1_fixation_onset, phase1_fixation_offset

#### Instruction screens (3 screens)

**Screen 1:** "You'll see the shapes from before, one at a time. Group each where you think it belongs."

**Screen 2:** "Shapes closer together are in the same group. Click to place, press Enter to submit."

**Screen 3:** "Once you've submitted the position of a shape, you can't move it again."

**TTL:** phase1_instruction2a_onset/enter/offset, phase1_instruction2b_onset/enter/offset, phase1_instruction2c_onset/enter/offset

**What to say:** "Place each shape where it belongs. Click to move, Enter when happy. Once you submit, you can't move it."

**Simple version:** "Put each shape where it goes. Click to move, Enter when happy. Once you press Enter, it's set."

#### Task (16 shapes)

Each shape shown 1 s, then clickable. Previously placed shapes visible. Hint: "Click to place. Press Enter to submit."

**What to say:** "Click to move, Enter when happy."

**Simple version:** "Click where you want it. You can click again to move. Enter when happy."

**TTL:** phase1_stimulus_onset/offset, phase1_click_place (each click), phase1_enter_submit, phase1_placements_saved

---

### Phase 2 — Top-Down Context Incorporation

#### Instructions (6 screens, max 2 sentences each; last screen min 5 s)

**Screen 1:** "Now you'll see the shapes again, paired with different pictures. Each shape appears with two pictures."

**Screen 2:** "For each picture, say out loud what the shape could be. For example: planet, ball, or cookie."

**Screen 3:** "Then click which picture the shape fits better with. We need to hear you say it every time."

**Screen 4:** "Do your best since you will be recorded, but don't panic if nothing comes to mind."

**Screen 5:** "You can also re-use answers."

**Screen 6:** "Here's an example to show you how it works." *(Enter after 5 s)*

**TTL:** phase2_instr1–6_onset/enter/offset

**What to say:** "Say out loud what the shape could be in each context—e.g. 'planet' or 'ball.' Then click which picture it fits better with."

**Simple version:** "Say out loud what the shape could be. We need to hear you. Then click which picture it fits better with."

**Experimenter note:** Enforce saying it out loud. If quiet: "What could this shape be? Say it out loud."

#### Tutorial — Single intro screen + demo

**Intro (1 Enter):** "In this example, you'll see a space picture, then a circle, then a circus picture. Say what the shape could be in each, then watch as we pick which fits better."

**Demo:** Fixation 500 ms → practice1 (space) → circle → blank → red dot + "You might say the circle is a 'PLANET'" → practice2 (circus) → circle → blank2 → red dot + "You might say the circle is a 'BALL'" → Question: CIRCUS | SPACE (participant watches; SPACE button highlighted in demo) → Blank 3 s → Ready screen (1 Enter)

**TTL:** phase2_tutorial_intro_onset/enter/offset, phase2_tutorial_fixation_onset/offset, phase2_tutorial_context1/shape/blank/reddot, phase2_tutorial_context2/shape2/blank2/reddot2, phase2_tutorial_question_onset/offset, phase2_tutorial_response, phase2_tutorial_post_blank_onset/offset, phase2_ready_onset/enter/offset

**What to say:** "Circle could be a planet or a ball. You'll pick which fits better."

**Simple version:** "In one picture it's a planet, in the other a ball. Pick which fits better."

#### Ready screen

**Display says:** "Ready to try this with some actual shapes and images?"

**What to say:** "Ready?"

#### Task (48 trials)

**Design:** Each shape has 2 context categories. Four trials per shape: A then B, B then A, A-control then B-control, B-control then A-control. See `csv_documentation.md` for details.

**Trial:** Fixation 500 ms → Context 1 → Shape 1 s → Blank → Red dot 2 s → Context 2 → Shape 1 s → Blank → Red dot 2 s → Question (click A or B) → Blank 500 ms

**Breaks:** Every 12 trials: "Take a break!" (phase2_break_onset/enter/offset)

**TTL:** phase2_fixation, phase2_context1/shape, phase2_blank1, phase2_reddot, phase2_context2/shape2, phase2_blank2, phase2_reddot2, phase2_question_onset, phase2_response, phase2_question_offset, phase2_trial_iti (per trial)

**What to say:** "Say out loud what the shape could be in each context. Then click which fits better. Say it every time."

**Simple version:** "Say what it could be—like 'moon' or 'cookie.' Then click which picture fits better."

---

### Phase 3 — Post-Context Shape Reclassification

#### Instructions (5 screens, max 2 sentences each)

**Screen 1:** "Let's sort some shapes again, like we did in the VERY beginning. Click to place each shape where you think it belongs."

**Screen 2:** "Again, shapes closer together are ones you're grouping as more similar."

**Screen 3:** "You may refer to the Phase 2 associations—the images you saw with each shape—when deciding how to group them."

**Screen 4:** "Feel free to use whatever grouping feels intuitive."

**Screen 5:** "Once you've submitted the position of a shape, you can't move it again."

**TTL:** phase3_instr1–5_onset/enter/offset

**What to say:** "Same as the start. Click to move, Enter when happy. Once you submit, you can't move it. You can use the Phase 2 associations when deciding how to group them."

**Simple version:** "Same as before. Put each where it goes. Once you press Enter, it's set. You can use the pictures from Phase 2 to help you group them."

**Experimenter note:** Emphasize "Things that go together go close." Explicitly say they may refer to Phase 2 associations for their grouping.

#### Task

Identical to Phase 1. Shape order randomized differently. Hint: "Click to place. Press Enter to submit."

**TTL:** phase3_stimulus_onset/offset, phase3_click_place, phase3_enter_submit, phase3_placements_saved

**What to say:** "Click to move, Enter when happy."

**Simple version:** "Same as before. Click to move, Enter when happy."

#### Debrief (3 questions)

1. "Did you use the same grouping strategy as the first time you sorted these shapes?" — Yes / No
2. "Did the images associated with each shape you saw influence your grouping the second time around?" — Yes / No
3. "After thinking about how shapes might fit in different environments, did you find yourself interpreting the shapes differently when you sorted them the second time?" — Yes / No

**TTL:** phase3_debrief_onset, phase3_debrief_response (per question)

**What to say:** "Three questions. Click Yes or No for each."

**Simple version:** "Did you put them together the same way? Did the pictures change how you put them together? Did you see the shapes differently the second time?"

---

### End

**Display:** "Thank you! Task complete." (2 seconds, then closes)

**TTL:** experiment_end, summary_saved, thanks_onset, thanks_offset

---

## Notes for Experimenters

- **ELI5:** Use "Simple version" when needed. Short sentences, no jargon. Check in: "Does that make sense?"
- **ESC** exits. **Click** to move, **Enter** to submit (Phase 1 & 3).
- **Phase 2:** Say it out loud. Nudge if silent: "We need to hear you."
- **Test runs:** Name contains "test" → no files written (TTL file deleted).
- **Placement images:** `phase1_placements_*.png`, `phase3_placements_*.png` in `../LOG_FILES/`
- **Euclidean distance:** Smaller = shapes grouped more similarly (closer categorically).
- **Tutorial video:** `STIMULI/tutorial_video.mp4`; spec in `STIMULI/tutorial_video_spec.md`. Fallback if missing.
- **TTL:** Every screen change and response is logged. See `csv_documentation.md` for full mapping.
- **Mac:** Parallel port not supported; TTL logged to CSV only. Cedrus pyxid2 works if connected.
- **OOM:** Mac uses windowed mode (1280×720) by default. Use `PSYCHOPY_WINDOWED=0` for fullscreen. On Windows/Linux, use `PSYCHOPY_WINDOWED=1` for windowed.
