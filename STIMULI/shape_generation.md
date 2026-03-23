# Shape Generation Pipeline

The 16 shapes used in Phase 1 and Phase 3 were created via the following pipeline.

## Overview

1. **Anchor**: The bunny shape from Henderson et al. 2025 was used as the top-left anchor.
2. **OpenAI modifications**: OpenAI (DALL·E or similar) was used to generate the other three anchor shapes—duck, bird, and squirrel—from the bunny as a reference.
3. **Morphing**: A Python script performs contour interpolation to morph between the four anchors and produce a 4×4 grid of intermediate shapes.

## Anchor Layout

| Corner       | Anchor   |
|-------------|----------|
| Top-left    | bunny    |
| Top-right   | duck     |
| Bottom-left | bird     |
| Bottom-right| squirrel |

## Morphing Algorithm

The script uses contour extraction (OpenCV), resampling to a fixed number of points (512), and linear interpolation in parameter space to morph between corners:

1. **Extract contour** from each anchor (threshold → findContours → resample to N_CONTOUR points).
2. **Bilinear interpolation**: For grid position (i, j) with t = i/(N−1), s = j/(N−1):
   - `top = morph(bunny, duck, s)`
   - `bottom = morph(bird, squirrel, s)`
   - `final = morph(top, bottom, t)`
3. **Render** the morphed contour as a filled shape on a gray background.

## Output

- **Shape_X_Y.png** — Individual morphed shapes (X, Y = 0..3 in grid coordinates).
- **ShapeGrid_4x4.png** — Ordered 4×4 grid of all shapes.
- **ShapeGrid_4x4_scrambled.png** — Same shapes in randomized positions. Used for Phase 1 display (5 s preview before placement).

## Script

The morphing script is provided inline below (save as `morph_shapes.py` to run). Update the `ANCHORS` and `SAVEDIR` paths for your setup.

**Dependencies:**
```bash
pip install numpy scipy scikit-image pillow opencv-python
```

**Usage:**
```bash
python morph_shapes.py
```

```python
 #!/usr/bin/env python3
"""
Morphs 4 anchor shapes into a 4x4 grid using contour interpolation.
Corners: top-left=bunny, top-right=duck, bottom-left=bird, bottom-right=squirrel

Usage:
    python morph_shapes.py

Dependencies:
    pip install numpy scipy scikit-image pillow opencv-python
"""

import numpy as np
import cv2
from PIL import Image
from scipy.interpolate import interp1d
import os

# ── config ────────────────────────────────────────────────────────────────────
ANCHORS = {
    'top_left':     '/Users/mehtaka/Desktop/bunny.png',
    'top_right':    '/Users/mehtaka/Desktop/duck.png',
    'bottom_left':  '/Users/mehtaka/Desktop/bird.png',
    'bottom_right': '/Users/mehtaka/Desktop/squirrel.png',
}
SAVEDIR         = '/Users/mehtaka/Desktop/Stimuli/MorphGrid/'
GRID_PATH       = '/Users/mehtaka/Desktop/Stimuli/MorphGrid/ShapeGrid_4x4.png'
SCRAMBLED_PATH  = '/Users/mehtaka/Desktop/Stimuli/MorphGrid/ShapeGrid_4x4_scrambled.png'
MYSIZE          = 500
N_CONTOUR       = 512
N_GRID          = 4
BACK_COLOR      = 76
SHAPE_COLOR     = 230
THUMB           = 300
CANVAS_SIZE     = 1200   # scrambled display canvas size in px
RANDOM_SEED     = 42     # set to None for different scramble each run

os.makedirs(SAVEDIR, exist_ok=True)


def extract_contour(path, n_points, size):
    img = np.array(Image.open(path).convert('L').resize((size, size)))
    _, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour = max(contours, key=cv2.contourArea).squeeze()
    start_idx = np.argmax(contour[:, 0])
    contour = np.roll(contour, -start_idx, axis=0)
    dists = np.sqrt(np.sum(np.diff(contour, axis=0)**2, axis=1))
    cumlen = np.concatenate([[0], np.cumsum(dists)])
    cumlen_norm = cumlen / cumlen[-1]
    t_new = np.linspace(0, 1, n_points, endpoint=False)
    fx = interp1d(cumlen_norm, contour[:, 0], kind='linear')
    fy = interp1d(cumlen_norm, contour[:, 1], kind='linear')
    return np.stack([fx(t_new), fy(t_new)], axis=1)


def center_and_scale(contour, size):
    cx, cy = contour.mean(axis=0)
    contour = contour - [cx, cy]
    scale = (size * 0.35) / np.abs(contour).max()
    contour = contour * scale + [size / 2, size / 2]
    return contour


def contour_to_image(contour, size):
    img = np.full((size, size), BACK_COLOR, dtype=np.uint8)
    pts = contour.astype(np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], SHAPE_COLOR)
    return img


def morph(c1, c2, t):
    return (1 - t) * c1 + t * c2


def place_shapes_no_overlap(positions, thumb, canvas_size, rng):
    """Generate non-overlapping random positions for all shapes."""
    placed = []
    margin = 10
    max_attempts = 1000
    for _ in range(len(positions)):
        for attempt in range(max_attempts):
            x = rng.integers(margin, canvas_size - thumb - margin)
            y = rng.integers(margin, canvas_size - thumb - margin)
            overlap = False
            for px, py in placed:
                if abs(x - px) < thumb + margin and abs(y - py) < thumb + margin:
                    overlap = True
                    break
            if not overlap:
                placed.append((x, y))
                break
        else:
            # fallback: just place it even if overlapping
            placed.append((
                rng.integers(margin, canvas_size - thumb - margin),
                rng.integers(margin, canvas_size - thumb - margin)
            ))
    return placed


def main():
    print("Loading and processing anchor shapes...")
    anchors = {}
    for key, path in ANCHORS.items():
        c = extract_contour(path, N_CONTOUR, MYSIZE)
        c = center_and_scale(c, MYSIZE)
        anchors[key] = c
        print(f"  loaded {key}")

    tl = anchors['top_left']
    tr = anchors['top_right']
    bl = anchors['bottom_left']
    br = anchors['bottom_right']

    print(f"\nGenerating {N_GRID}x{N_GRID} morphed grid...")
    grid_images = []
    all_images  = []
    ts = np.linspace(0, 1, N_GRID)

    for i, ty in enumerate(ts):
        row_images = []
        for j, tx in enumerate(ts):
            top   = morph(tl, tr, tx)
            bottom = morph(bl, br, tx)
            final  = morph(top, bottom, ty)
            img = contour_to_image(final, MYSIZE)
            savepath = os.path.join(SAVEDIR, f'Shape_{i}_{j}.png')
            Image.fromarray(img).save(savepath)
            row_images.append(img)
            all_images.append((img, i, j))
            print(f"  saved Shape_{i}_{j}.png")
        grid_images.append(row_images)

    # ── ordered 4x4 grid ──────────────────────────────────────────────────────
    print("\nBuilding ordered grid image...")
    canvas = np.full((THUMB * N_GRID, THUMB * N_GRID), BACK_COLOR, dtype=np.uint8)
    for i in range(N_GRID):
        for j in range(N_GRID):
            img     = grid_images[i][j]
            resized = np.array(Image.fromarray(img).resize((THUMB, THUMB)))
            r = slice(i * THUMB, (i + 1) * THUMB)
            c = slice(j * THUMB, (j + 1) * THUMB)
            canvas[r, c] = resized
    Image.fromarray(canvas).save(GRID_PATH)
    print(f"  saved → {GRID_PATH}")

# ── scrambled 4x4 grid ────────────────────────────────────────────────────
    print("\nBuilding scrambled grid image...")
    rng = np.random.default_rng(RANDOM_SEED)

    # flatten, shuffle, reshape back to 4x4
    flat_images = [grid_images[i][j] for i in range(N_GRID) for j in range(N_GRID)]
    indices = list(range(len(flat_images)))
    rng.shuffle(indices)
    shuffled = [flat_images[k] for k in indices]

    scrambled_canvas = np.full((THUMB * N_GRID, THUMB * N_GRID), BACK_COLOR, dtype=np.uint8)
    for idx, img in enumerate(shuffled):
        i = idx // N_GRID
        j = idx % N_GRID
        resized = np.array(Image.fromarray(img).resize((THUMB, THUMB)))
        r = slice(i * THUMB, (i + 1) * THUMB)
        c = slice(j * THUMB, (j + 1) * THUMB)
        scrambled_canvas[r, c] = resized

    Image.fromarray(scrambled_canvas).save(SCRAMBLED_PATH)
    print(f"  saved → {SCRAMBLED_PATH}")


if __name__ == '__main__':
    main()
```

## Naming Convention

The task uses filenames `Shape_X_Y.png` where X and Y correspond to grid row and column (0–3). The code maps these to latent coordinates 0.10, 1.70, 3.30, 4.90 for Euclidean distance calculations. See `_parse_shape_grid_position` in `context_shape_task.py`.
