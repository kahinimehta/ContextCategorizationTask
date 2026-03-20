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
| 2 | ~3 s | Red square appears at center, then appears at left (click-to-place, no dragging) | "Red square appears. Clicking to place on the left." |
| 3 | ~3 s | Red circle appears at center, then appears at right (click-to-place) | "Red circle appears. Clicking to place on the right." |
| 4 | ~3 s | Green circle appears at center, then appears at right next to red circle (spaced apart, no overlap) | "Green circle appears. Clicking to place on the right." |
| 5a | ~3 s | Final layout: square on left, both circles on right (sorted by shape) | "We sorted by shapes but could have sorted by color." |
| 5b | ~4 s | Same layout | "You're grouping into groups—not arranging on a line or spectrum. Shapes closer together are in the same group." |
| 6 | ~2.5 s | Same layout with new subtitle | "Objects in a group can still be slightly further apart than from objects in another group." + "Click to place. Press Enter to submit." |

**Total:** ~21 seconds. All text on screen for at least 2 seconds.

---

## Key Requirements

1. **Click-to-place, not drag:** Show shapes being placed by a single click at the target location. Do not show dragging.
2. **Subtitle style:** Black text, centered at bottom of screen. Describe what's happening (e.g., "Clicking to place on the left").
3. **Required subtitles (steps 5a, 5b, 6):** Step 5a: "We sorted by shapes but could have sorted by color." Step 5b: "You're grouping into groups—not arranging on a line or spectrum. Shapes closer together are in the same group." Step 6: "Objects in a group can still be slightly further apart than from objects in another group." + "Click to place. Press Enter to submit."
4. **Layout:** Square on the left; both circles (red and green) side-by-side on the right (spaced apart, no overlap). Sorted by shape. Emphasize grouping into groups—not arranging on a line or spectrum.
5. **Resolution:** 1920×1080 recommended (matches task display).

---

## Fallback

If `tutorial_video.mp4` is missing, the task plays an animated fallback with the same sequence and subtitles.
