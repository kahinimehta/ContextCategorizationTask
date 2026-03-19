# Tutorial Video Production Spec

**File:** `STIMULI/tutorial_video.mp4`  
**Purpose:** Demonstration of the click-to-place task for Phase 1 & 3.  
**Shapes:** Red square, red circle, green circle.

See `../README.md` and `../script.md` for task documentation.

**Click to place** (not drag). Multiple clicks allowed; Enter to submit. Subtitles describe what's on screen.

---

## Content & Timing

| Step | Duration | Visual | Subtitle |
|------|----------|--------|----------|
| 1 | ~2.5 s | Three shapes on screen: red square (left), red circle (center), green circle (right) | "Three shapes appear." |
| 2 | ~1.6 s | Red square appears at center, then appears at left (click-to-place, no dragging) | "Red square appears. Clicking to place on the left." |
| 3 | ~1.6 s | Red circle appears at center, then appears at left next to square (spaced apart, no overlap) | "Red circle appears. Clicking to place on the left." |
| 4 | ~1.6 s | Green circle appears at center, then appears at right | "Green circle appears. Clicking to place on the right." |
| 5a | ~2.5 s | Final layout: red square and red circle side-by-side on left (spaced apart), green on right | "We sorted by shapes but could have sorted by color." |
| 5b | ~3 s | Same layout | "Shapes closer together are in the same group. Objects in a group can still be slightly further apart than from objects in another group." |
| 6 | ~2 s | Same layout with new subtitle | "Click to place. Press Enter to submit." |

**Total:** ~13–15 seconds

---

## Key Requirements

1. **Click-to-place, not drag:** Show shapes being placed by a single click at the target location. Do not show dragging.
2. **Subtitle style:** Black text, centered at bottom of screen. Describe what's happening (e.g., "Clicking to place on the left").
3. **Required subtitles (steps 5a, 5b):** Step 5a: "We sorted by shapes but could have sorted by color." Step 5b: "Shapes closer together are in the same group. Objects in a group can still be slightly further apart than from objects in another group."
4. **Layout:** Red square and red circle side-by-side on the left (spaced apart, no overlap); green circle on the right.
5. **Resolution:** 1920×1080 recommended (matches task display).

---

## Fallback

If `tutorial_video.mp4` is missing, the task plays an animated fallback with the same sequence and subtitles.
