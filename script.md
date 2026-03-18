# Experimenter Script

Full task specs: See README.md. CSV format: `csv_documentation.md`.

## Quick Start

1. Open terminal in the task directory
2. Run: `python context_shape_task.py`
3. Enter participant name when prompted (dialog appears before fullscreen)
4. **ESC** exits at any time

**Data saved to**: `../LOG_FILES/` (one level up from task folder)

---

## Full Experiment Script

### Participant Login (before fullscreen)

**Display**: Dialog box: "Please enter your name:"

**What to say**: "Enter your first name and last initial. When done, click OK."

*Note: Participant name is appended to all CSV filenames.*

---

### Welcome Screen

**Display says:**
"Welcome to our task! Let's get started. First, watch this example video of how we work on this task."

**Display shows:** CONTINUE button

**What to say:** "Welcome! Read the message. When you're ready, click CONTINUE."

**TTL:** Screen onset, CONTINUE click

---

### Tutorial — Phase 1 Practice

#### Step 1 — Overview display

**Display shows:** Two red circles and one green square arranged in a horizontal line (5 seconds)

**What to say:** "Look at these shapes."

**TTL:** Onset, offset

#### Step 2 — Instruction screen

**Display says:**
"You will see one of the shapes from before. Group all shapes by dragging them to where you think it belongs on the screen."

**Display:** 2 seconds (no response needed)

**What to say:** "You'll drag each shape to where you think it belongs. Group similar shapes together."

**TTL:** Onset, offset

#### Step 3 — Sequential drag practice (3 shapes: circle, square, circle)

**Display:** Each shape shown alone for 1 second, then becomes draggable. Previously placed shapes remain visible as anchors. SUBMIT to confirm each placement.

**What to say:** "Drag each shape to where it belongs. Circles go together on one side, the square on the other. Click SUBMIT when you're happy with the position."

**TTL:** Stimulus onset, offset, drag start, SUBMIT click

#### Step 3.5 — Debrief

**Display says:** "In this practice, we sorted all objects by shape!"

**Display shows:** CONTINUE button

**What to say:** "Great! We sorted by shape. Click CONTINUE."

**TTL:** Screen onset, CONTINUE click

#### Step 4 — Transition

**Display says:** "Let's get started on your task!"

**Display shows:** CONTINUE button

**What to say:** "Ready for the real task. Click CONTINUE."

**TTL:** Screen onset, CONTINUE click

---

### Phase 1 — Bottom-Up Shape Classification

#### Instructions screen

**Display says:** "Let's sort some shapes. First you will see all of them. Then you will place them one at a time and group them where you think they belong, as in the practice."

**Display shows:** SUBMIT button

**What to say:** "You'll see the full grid first, then place each shape one at a time. Group them where they belong."

**TTL:** Screen onset, SUBMIT click

#### Grid display

**Display:** ShapeGrid_4x4.png for 5 seconds

**TTL:** Onset, offset

#### Fixation

**Display:** Black cross on white screen for 1 second

**TTL:** Onset, offset

#### Instruction screen

**Display says:** "You will now see the shapes from before, one at a time. Group each to where you think it belongs on the screen."

**Display:** 2 seconds

**TTL:** Onset, offset

#### Sequential drag task (16 shapes)

**Display:** Each shape shown alone 1 second (not draggable), then draggable. Previously placed shapes remain visible. SUBMIT to confirm.

**What to say:** "Place each shape where it belongs. Take your time. Click SUBMIT when done with each one."

**TTL:** Stimulus onset, offset, drag start, SUBMIT click

---

### Phase 2 — Top-Down Context Incorporation

#### Instructions screen

**Display says:** "Now, you will see the shapes again, in conjunction with different contexts. Try to think of what the shape might be in that context and say it out loud. Here's an example."

**Display shows:** CONTINUE button

**What to say:** "You'll see shapes with different background images. **Say out loud what the shape might be in each context**—e.g., 'planet' or 'ball.' We want you to verbalize your interpretation. Click CONTINUE."

**TTL:** Screen onset, CONTINUE click

**Experimenter note:** Enforce that participants say categories out loud. Nudge them if they stay silent.

#### Tutorial (practice1, practice2, circle, CIRCUS | SPACE)

**Display:** Fixation 500 ms → practice1.png 1000 ms → blue circle 1000 ms → blank 1000 ms → red dot + "PLANET" 2000 ms → practice2.png 1000 ms → same circle 1000 ms → blank 1000 ms → red dot + "BALL" 2000 ms → Question: "Which context fits the object better?" — CIRCUS | SPACE. Participant clicks SPACE (example). Blank 3000 ms.

**What to say:** "In the example, the circle could be a planet in space or a ball at the circus. You'll pick which context fits better. Click CONTINUE when ready."

**TTL:** All onsets/offsets, response click

#### Ready screen

**Display says:** "Ready to try this with some actual shapes and images?"

**Display shows:** CONTINUE button

**What to say:** "Ready? Click CONTINUE."

**TTL:** Onset, CONTINUE click

#### Actual Phase 2 Task (48 trials)

**Trial structure:** Fixation 500 ms → Context 1 → Shape 1000 ms → Blank 1000 ms → Red dot 2000 ms → Context 2 → Same shape 1000 ms → Blank 1000 ms → Red dot 2000 ms → Question: "Which context fits the object better?" — [Category A] | [Category B] → Blank 500 ms

**Breaks:** Every 12 trials: "Take a break! Click CONTINUE when ready to move on."

**What to say:** "For each trial, say out loud what the shape might be in each context. Then pick which context fits the object better. **Remember to say your interpretations out loud.**"

**TTL:** All screen onsets, response clicks, break onset/click

---

### Phase 3 — Post-Context Shape Reclassification

#### Instructions screen

**Display says:** "Let's sort some shapes again, like we did in the VERY beginning."

**Display shows:** SUBMIT button

**What to say:** "Same as the very beginning—place each shape where it belongs. Click SUBMIT to continue."

**TTL:** Screen onset, SUBMIT click

#### Task

**Display:** Identical structure to Phase 1. Shape order randomized differently from Phase 1.

**What to say:** "Place each shape where you think it belongs now."

**TTL:** Same as Phase 1

---

### End

**Display:** "Thank you! Task complete." (2 seconds, then closes)

---

## Notes for Experimenters

- **ESC** exits at any time
- **Phase 2**: Emphasize saying categories out loud; nudge participants who stay silent
- **Test runs**: Use a name containing "test" to skip file saving
- **LOG_FILES**: Ensure `../LOG_FILES/` exists (created automatically)
