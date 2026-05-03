# Experimenter Script — run sheet


---

## Full Experiment Script

### Participant login

**Display copy:** **"Enter your name"** (upper); centered entry line. **Enter** submits; **ESC** quits. Key handling: **`TASK_DESCRIPTION.md`** (macOS / unrestricted poll).

---

### Welcome copy

**Display:** **"Welcome to your task! Hit Enter to watch the tutorial video."**  


---

### Tutorial (Phase 1 training) copy

**Paths:** **`STIMULI/tutorial_video.mp4`** when playback succeeds — **no** `tutorial_fallback_*` TTL steps inside the tutorial. **Animated fallback** when the file is absent or playback fails: paired **`tutorial_fallback_onset`** / **`tutorial_fallback_offset`** with **`trial_info: step=`** **`1`**, **`2`**, **`3`**, **`4`**, **`5a`**, **`5b`** (see **`csv_documentation.md`**).

**Demo-only wording:** **`PHASE13_CLICK_ENTER_INSTRUCTION`** (*click to place, Enter to confirm*) appears **once** in the fallback, as the subtitle during **`step=2`** (simulated square placement). **Phase 1 & Phase 3** still show that sentence on **`phase1_instr3`** / **`phase3_instruction2c`** and as the gray sorting hint — unchanged.

1.  **"The first part of the task is about sorting objects. Watch how we sort these objects!"** — **square**, **red circle**, and **green circle** visible **at once** for **`TUTORIAL_FB_OVERVIEW_SEC`** (spread layout). 

2.  **"Click where you want to place each object, then press Enter to confirm."** 

3.  **"Now, let's group the red circle with the red square on the left."** 

4.  **"Let's place the green circle to the right (in a different group)."** 

5.  **"See how we ended up sorting by color? We could have sorted by shape too — there are no wrong answers here!"** 

6.  **"We created groups, not a spectrum — nearby objects share a group."** 
**Transition:** **"Your turn to group some objects! Remember the same rules."**

---

### Phase 1 — Object sorting copy (click & enter controls)

**Instructions (before grid):**  
1. **"Ask the experimenter if you have any questions!"** · `phase1_questions`

**After fixation (in order):**  
1. **"Now, group these objects like in the demo."** · `phase1_instr1` (mini-grid inset)  
2. **"Use as many groups as you want, and group objects however feels intuitive."** · `phase1_instr2` (full screen, no inset)  
3. **"Click where you want to place each object, then press Enter to confirm."** · `phase1_instr3` (mini-grid inset)

---

### Phase 2 — Context incorporation copy (left & right keyboard controls)

1. **"Ask the experimenter if you have any questions!"** · `phase2_questions`  
2. **"For the next part of the task, we will show you a demo first. For this part, you will see each object paired with two contexts."** · `phase2_instr1`  
3. **"You will see: a context → object → question asking what the object is."** · `phase2_instr2`  
4. **"When you see that question, say aloud what the object might be in that context. Then, use the left/right keys to choose which context fits best."** · `phase2_instr3`  
5. **"The experimenter will record your responses, but don't panic. Just do your best and feel free to re-use answers."** · `phase2_instr4`


**Tutorial:** **"Watch this demo before you start the task!"** 

1. **"What is the object?" / "You might say the circle is a 'PLANET'"**
2. **""What is the object?" / "You might say the circle is a 'BALL'"**"
3. **""Which context fits best? Use the left/right keys to choose." + SPACE | CIRCUS**"
4. **""You might think 'CIRCUS' (right key) is the better context"**"
5. **""Ready to start?"**"

**Experimenter:** remind them to say their choices out loud and clearly so recordings can be transcribed. They should only speak when prompted by the screen. They have breaks every 16 trials where you can check in with them. 

---

### Phase 3 — Re-sort post-context (click & enter controls)

**Instructions:**  
1. **"Ask the experimenter if you have any questions!"** · `phase3_questions`  
2. **"Now you will sort the objects again — like you did right in the beginning. See all the objects first."** · `phase3_instr1`  
3. **"Use whatever grouping method feels intuitive to you."** · `phase3_instr2`

**Before grid:** **"You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize."** · `phase3_before_grid` · **Enter** ignored until **`PHASE13_BEFORE_GRID_MIN_SEC`** (**`TASK_DESCRIPTION.md`** timings).

---

###  Debrief (3 questions): (left & right keyboard controls)

1. **"Did you group the objects differently the second time around?"**  
2. **"Did the contexts you saw change your grouping the second time?"**  
3. **"Did you see the objects differently the second time grouping them than you did when you first saw them?"**

---

### End

**Display:** **"You did an amazing job with these objects. Thank you!"** (**`THANKS_SCREEN_SEC`** s)

---
### Notes

Use `ESC` or `CMD+Q` to quit early. Task files are written out incrementally.

