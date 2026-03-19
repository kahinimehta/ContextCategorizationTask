# Experimenter Script

Full task specs: See README.md. CSV format: `csv_documentation.md`.

## Quick Start

1. Open terminal in the task directory
2. Run: `python context_shape_task.py`
3. Enter participant name on the fullscreen prompt (like Social Recognition Task)
4. **ESC** exits at any time (no Exit button)

**Data saved to**: `../LOG_FILES/` (one level up from task folder)

---

## Full Experiment Script

### Participant Login (fullscreen, like SRT)

**Display**: Fullscreen text prompt: "Enter your first name and last initial with no spaces/capitals: Hit Enter when done."

**Display shows:** Text field for typing; type with keyboard, press Enter when done.

**What to say:** "Enter your first name and last initial, no spaces or capitals. When you're done, press Enter."

*Note: Participant name is appended to all CSV filenames. ESC quits at any time.*

---

### Welcome Screen

**Display says:**
"Welcome to our task! Let's get started. First, watch this example video of how we work on this task."

**Display shows:** "Press Enter to continue."

**What to say:** "Welcome! Read the message. When you're ready, press Enter."

**TTL:** Screen onset, Enter press

---

### Tutorial — Video with text overlay

**Shapes:** Red square, red circle, green circle.

**Option A (video):** Place `STIMULI/tutorial_video.mp4` in the stimuli folder. The video plays with text explaining what's happening. ESC exits.

**Option B (fallback):** If no video, a timed sequence shows the three shapes with explanatory text:
- "Here are the three shapes: a red square, a red circle, and a green circle."
- "You will see each shape one at a time. Drag it to where you think it belongs."
- "Group similar shapes together. The red shapes go together; the green circle is different."
- "When you're happy with the position, press Enter to submit."

**What to say:** "Watch the tutorial. It shows how to drag shapes and press Enter to submit."

**TTL:** tutorial_video_onset/offset or tutorial_fallback_onset/offset

#### Debrief

**Display says:** "In this practice, we sorted all objects by shape!"

**Display shows:** "Press Enter to continue."

**What to say:** "Great! We sorted by shape. Press Enter."

**TTL:** Screen onset, Enter press

#### Transition

**Display says:** "Let's get started on your task!"

**Display shows:** "Press Enter to continue."

**What to say:** "Ready for the real task. Press Enter."

**TTL:** Screen onset, Enter press

---

### Phase 1 — Bottom-Up Shape Classification

#### Instructions screen (minimum 10 seconds display)

**Display says:** "Let's sort some shapes. First you will see all of them. Then you will place them one at a time and group them where you think they belong, as in the practice. Press Enter when you're ready."

**Display shows:** "Press Enter to continue." (Enter accepted after 10 seconds)

**What to say:** "You'll see the full grid first, then place each shape one at a time. Group them where they belong. Press Enter to submit each placement."

**TTL:** Screen onset, Enter press

#### Grid display

**Display:** ShapeGrid_4x4.png for 5 seconds

**TTL:** Onset, offset

#### Fixation

**Display:** Black cross on white screen for 1 second

**TTL:** Onset, offset

#### Instruction screen

**Display says:** "You will now see the shapes from before, one at a time. Group each to where you think it belongs on the screen. Press Enter to submit each placement."

**Display shows:** "Press Enter to continue."

**What to say:** "Place each shape where it belongs. Press Enter when you're happy with each position."

**TTL:** Screen onset, Enter press

#### Sequential drag task (16 shapes)

**Display:** Each shape shown alone 1 second (not draggable), then draggable. Previously placed shapes remain visible. **Press Enter to submit** (no SUBMIT button).

**What to say:** "Place each shape where it belongs. Take your time. **Press Enter to submit** when done with each one."

**TTL:** Stimulus onset, offset, drag start, Enter submit

---

### Phase 2 — Top-Down Context Incorporation

#### Instructions screen (minimum 8 seconds display)

**Display says:** "Now, you will see the shapes again, in conjunction with different contexts. Try to think of what the shape might be in that context and say it out loud. Here's an example."

**Display shows:** "Press Enter to continue."

**What to say:** "You'll see shapes with different background images. **Say out loud what the shape might be in each context**—e.g., 'planet' or 'ball.' We want you to verbalize your interpretation. Press Enter when ready."

**TTL:** Screen onset, Enter press

**Experimenter note:** Enforce that participants say categories out loud. Nudge them if they stay silent.

#### Tutorial (practice1, practice2, circle, CIRCUS | SPACE)

**Display:** Fixation 500 ms → practice1.png 1000 ms → blue circle 1000 ms → blank 1000 ms → red dot + "PLANET" 2000 ms → practice2.png 1000 ms → same circle 1000 ms → blank 1000 ms → red dot + "BALL" 2000 ms → Question: "Which context fits the object better?" — CIRCUS | SPACE. Participant clicks SPACE. Blank 3000 ms.

**What to say:** "In the example, the circle could be a planet in space or a ball at the circus. You'll pick which context fits better. Press Enter when ready."

**TTL:** All onsets/offsets, response click

#### Ready screen

**Display says:** "Ready to try this with some actual shapes and images?"

**Display shows:** "Press Enter to continue."

**What to say:** "Ready? Press Enter."

**TTL:** Onset, Enter press

#### Actual Phase 2 Task (48 trials)

**Trial structure:** Fixation 500 ms → Context 1 → Shape 1000 ms → Blank 1000 ms → Red dot 2000 ms → Context 2 → Same shape 1000 ms → Blank 1000 ms → Red dot 2000 ms → Question: "Which context fits the object better?" — [Category A] | [Category B] (click to choose) → Blank 500 ms

**Breaks:** Every 12 trials: "Take a break! Press Enter when ready to move on."

**What to say:** "For each trial, say out loud what the shape might be in each context. Then click which context fits the object better. **Remember to say your interpretations out loud.**"

**TTL:** All screen onsets, response clicks, break onset/Enter press

---

### Phase 3 — Post-Context Shape Reclassification

#### Instructions screen

**Display says:** "Let's sort some shapes again, like we did in the VERY beginning."

**Display shows:** "Press Enter to continue."

**What to say:** "Same as the very beginning—place each shape where it belongs. Press Enter to submit each placement."

**TTL:** Screen onset, Enter press

#### Task

**Display:** Identical structure to Phase 1. Shape order randomized differently from Phase 1. **Press Enter to submit** each placement.

**What to say:** "Place each shape where you think it belongs now. Press Enter to submit."

**TTL:** Same as Phase 1

---

### End

**Display:** "Thank you! Task complete." (2 seconds, then closes)

---

## Notes for Experimenters

- **ESC** exits at any time (no Exit button)
- **Enter** submits/continues throughout (no SUBMIT or CONTINUE buttons)
- **Phase 2**: Emphasize saying categories out loud; nudge participants who stay silent
- **Test runs**: Use a name containing "test" to skip file saving
- **LOG_FILES**: Ensure `../LOG_FILES/` exists (created automatically)
- **Tutorial video**: Add `STIMULI/tutorial_video.mp4` for video tutorial; otherwise fallback sequence plays
