# Experimenter Script

Full task specs: See README.md. CSV format and TTL trigger mapping: `csv_documentation.md`. Use "Simple version" scripts when participants need plain-language explanations.

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

---

## Full Experiment Script

### Participant Login (fullscreen, like SRT)

**Display**: Fullscreen text prompt: "Enter your first name and last initial with no spaces/capitals: Hit Enter when done."

**Display shows:** Text field for typing; type with keyboard, press Enter when done.

**What to say:** "Enter your first name and last initial, no spaces or capitals. When you're done, press Enter."

**Simple version:** "Type your name. No spaces. When you're finished, press Enter."

*Note: Participant name is appended to all CSV filenames. ESC quits at any time.*

---

### Welcome Screen

**Display says:**
"Welcome to our task! Let's get started. First, watch this example video of how we work on this task."

**Display shows:** "Press Enter to continue."

**What to say:** "Welcome! Read the message. When you're ready, press Enter."

**Simple version:** "Hi! Read what it says. When you're ready, press Enter."

**TTL:** Screen onset, Enter press

---

### Tutorial — Video with subtitles

**Shapes:** Red square, red circle, green circle.

**Option A (video):** Place `STIMULI/tutorial_video.mp4` in the stimuli folder. See `STIMULI/tutorial_video_spec.md` for full production spec. The video shows click-to-place—shapes appearing and being clicked to place. **Subtitles describe what's on screen** (e.g., "Red square appears. Clicking to place on the left."), not instructions read aloud. Include: "There were alternative ways of grouping, but this is what we went with." ESC exits.

**Option B (fallback):** If no video, an animated sequence simulates the tutorial:
- "Three shapes appear."
- Red square appears, animates left: "Red square appears. Clicking to place on the left."
- Red circle appears, animates left: "Red circle appears. Clicking to place on the left."
- Green circle appears, animates right: "Green circle appears. Clicking to place on the right."
- "There were alternative ways of grouping, but this is what we went with."
- "Click to place each shape."

**What to say:** "Watch the tutorial. It shows what clicking to place looks like."

**Simple version:** "Watch this short video. It shows you what to do—you'll click to put shapes where you want them."

**TTL:** tutorial_video_onset/offset or tutorial_fallback_onset/offset

#### Debrief

**Display says:** "In this practice, we sorted all objects by shape!"

**Display shows:** "Press Enter to continue."

**What to say:** "Great! We sorted by shape. Press Enter."

**Simple version:** "Nice! We put the shapes that look alike together. Press Enter."

**TTL:** Screen onset, Enter press

#### Transition

**Display says:** "Let's get started on your task!"

**Display shows:** "Press Enter to continue."

**What to say:** "Ready for the real task. Press Enter."

**Simple version:** "Now we'll do the real thing. Press Enter when you're ready."

**TTL:** Screen onset, Enter press

---

### Phase 1 — Bottom-Up Shape Classification

#### Instructions screen (minimum 10 seconds display)

**Display says:** "Let's sort some shapes. First you will see all of them. Then you will place them one at a time by clicking where you want each to go, grouping them where you think they belong, as in the practice. Shapes you place closer together are ones you're grouping as more similar. Use as many groups as you need. Press Enter when you're ready."

**Display shows:** "Press Enter to continue." (Enter accepted after 10 seconds)

**What to say:** "You'll see the full grid first, then place each shape one at a time. Group them where they belong. Use as many groups as you need. Click to place each shape."

**Simple version:** "First you'll see all the shapes. Then one by one, you'll put each shape on the screen. Put shapes that go together near each other. Shapes that are alike go close. Shapes that are different go far apart. You can make as many groups as you want. Just click where you want each shape to go."

**Experimenter note:** **Emphasize** that shapes placed closer together = more similar. Use simple language: "Things that go together go close. Things that are different go far apart."

**TTL:** Screen onset, Enter press

#### Grid display

**Display:** ShapeGrid_4x4.png for 5 seconds

**TTL:** Onset, offset

#### Fixation

**Display:** Black cross on white screen for 1 second

**TTL:** Onset, offset

#### Instruction screen

**Display says:** "You will now see the shapes from before, one at a time. Group each to where you think it belongs on the screen. Remember: shapes placed closer together are ones you're grouping as more similar. Use as many groups as you need. Click to place each shape."

**Display shows:** "Press Enter to continue."

**What to say:** "Place each shape where it belongs. Click to place each one. Remember: shapes you put closer together are ones you're grouping as more similar."

**Simple version:** "Put each shape where it goes. Click to put it there. Remember: things that go together go close. Things that are different go far apart."

**TTL:** Screen onset, Enter press

#### Sequential click-to-place task (16 shapes)

**Display:** Each shape shown alone 1 second, then clickable. Previously placed shapes remain visible. **Click to place** each shape.

**What to say:** "Place each shape where it belongs. Take your time. **Click** to place each one."

**Simple version:** "One shape will show up. Click where you want to put it. Take your time. There's no wrong answer."

**TTL:** Stimulus onset, offset, click_place

---

### Phase 2 — Top-Down Context Incorporation

#### Instructions screen (minimum 8 seconds display)

**Display says:** "Now, you will see the shapes again, in conjunction with different contexts. Try to think of what the shape might be in that context and say it out loud. Here's an example."

**Display shows:** "Press Enter to continue."

**What to say:** "You'll see shapes with different background images. **Say out loud what the shape might be in each context**—e.g., 'planet' or 'ball.' We want you to verbalize your interpretation. Press Enter when ready."

**Simple version:** "Now you'll see shapes with different pictures behind them. For each one, say out loud what the shape could be—like 'a planet' or 'a ball.' We need to hear you say it. Then you'll pick which picture it fits better with. Press Enter when you're ready."

**Experimenter note:** Enforce that participants say it out loud. If they're quiet: "Remember, we need you to say what you think out loud. What could this shape be?"

#### Tutorial (practice1, practice2, circle, CIRCUS | SPACE)

**Display:** Fixation 500 ms → practice1.png 1000 ms → blue circle 1000 ms → blank 1000 ms → red dot + "PLANET" 2000 ms → practice2.png 1000 ms → same circle 1000 ms → blank 1000 ms → red dot + "BALL" 2000 ms → Question: "Which context fits the object better?" — CIRCUS | SPACE. Participant clicks SPACE. Blank 3000 ms.

**What to say:** "In the example, the circle could be a planet in space or a ball at the circus. You'll pick which context fits better. Press Enter when ready."

**Simple version:** "See the circle? In one picture it could be a planet. In the other it could be a ball. You'll pick which picture it fits better with. Press Enter when ready."

**TTL:** All onsets/offsets, response click

#### Ready screen

**Display says:** "Ready to try this with some actual shapes and images?"

**Display shows:** "Press Enter to continue."

**What to say:** "Ready? Press Enter."

**Simple version:** "Ready to try? Press Enter."

**TTL:** Onset, Enter press

#### Actual Phase 2 Task (48 trials)

**Design:** Each shape has 2 context categories (A and B). Four trials per shape: A then B, B then A, A-control then B-control, B-control then A-control. Control = different image from same category. Same context category can appear with different shapes (e.g. BARK with shape 1 and shape 5); each context *pair* is unique to one shape.

**Trial structure:** Fixation 500 ms → Context 1 → Shape 1000 ms → Blank 1000 ms → Red dot 2000 ms → Context 2 → Same shape 1000 ms → Blank 1000 ms → Red dot 2000 ms → Question: "Which context fits the object better?" — [Category A] | [Category B] (click to choose) → Blank 500 ms

**Breaks:** Every 12 trials: "Take a break! Press Enter when ready to move on."

**What to say (before Phase 2):** "For each trial, say out loud what the shape might be in each context. Then click which context fits the object better. **Remember to say your interpretations out loud.**"

**Simple version:** "Each time you see a shape with two pictures, say out loud what it could be—like 'a moon' or 'a cookie.' Then click which picture it fits better with. Say it out loud every time."

**If participant asks during a break:** "Take a little rest. Press Enter when you're ready to keep going."

**TTL:** All screen onsets, response clicks, break onset/Enter press

---

### Phase 3 — Post-Context Shape Reclassification

#### Instructions screen

**Display says:** "Let's sort some shapes again, like we did in the VERY beginning. Click to place each shape where you think it belongs. Again, shapes placed closer together are ones you're grouping as more similar. Feel free to use whatever grouping feels intuitive."

**Display shows:** "Press Enter to continue."

**What to say:** "Same as the very beginning—place each shape where it belongs. Feel free to use whatever grouping feels intuitive. Click to place each shape. Again, shapes placed closer together are ones you're grouping as more similar."

**Simple version:** "Same as the start—put each shape where you think it goes. Put things that go together close. Things that are different, put far apart. Use whatever feels right to you."

**Experimenter note:** **Emphasize** (as in Phase 1): "Things that go together go close. Things that are different go far apart."

**TTL:** Screen onset, Enter press

#### Task

**Display:** Identical structure to Phase 1. Shape order randomized differently from Phase 1. **Click to place** each shape.

**What to say:** "Place each shape where you think it belongs now. Feel free to use whatever grouping feels intuitive. Click to place each one."

**Simple version:** "Put each shape where it goes. Same as before—things that go together go close. Click to put each one."

**TTL:** Same as Phase 1

#### Debrief questions (2)

**Question 1:** "Did you use the same grouping strategy as the first time you sorted these shapes?" — Yes / No

**Question 2:** "Did the images associated with each shape you saw influence your grouping the second time around?" — Yes / No

**What to say:** "Please answer these two questions. Click Yes or No for each."

**Simple version:** "Two quick questions. Did you put the shapes together the same way as the first time? Did the pictures you saw change how you put them together? Click Yes or No for each."

**TTL:** Onset and response click for each question. Answers, RT, and TTL timestamps saved to `debrief_{participant}_{datetime}.csv`.

---

### End

**Display:** "Thank you! Task complete." (2 seconds, then closes)

---

## Notes for Experimenters

- **Explain like they're 5:** Use the "Simple version" scripts when participants need clearer language. Short sentences, no jargon, one idea at a time. Check in: "Does that make sense?"
- **ESC** exits at any time (no Exit button)
- **Click** to place shapes (Phase 1 & 3); **Enter** to continue through instruction screens (no SUBMIT or CONTINUE buttons)
- **Phase 2**: Emphasize saying it out loud; nudge participants who stay silent: "We need to hear you say what you think."
- **Test runs**: Use a name containing "test" (e.g., "test1", "TestRun") to skip all file saving—no phase, debrief, summary, TTL log, or placement PNG files are written
- **LOG_FILES**: Ensure `../LOG_FILES/` exists (created automatically)
- **Placement images**: Phase 1 and Phase 3 save PNG images of final placements to `../LOG_FILES/` (e.g., `phase1_placements_{participant}_{datetime}.png`)
- **Euclidean distance** (in summary CSV): In layman terms, this shows how close the shapes are categorically to each other—smaller distances mean the participant grouped those shapes more similarly.
- **Emphasize to participants:** Shapes placed closer together = more similar categorically. Experimenters should stress this during Phase 1 and Phase 3 instructions so participants understand that spatial distance reflects their grouping.
- **Tutorial video**: Add `STIMULI/tutorial_video.mp4` for video tutorial; see `STIMULI/tutorial_video_spec.md` for production spec. Otherwise fallback sequence plays.
