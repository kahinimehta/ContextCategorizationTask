#!/usr/bin/env python3
"""
ContextShape Task — PsychoPy Implementation
Environment: Python (Anaconda), PsychoPy v2025.1.1
Fullscreen with DPI scaling. ESC exits at any time.
TTL triggers via Blackrock parallel port for every screen change and response.
"""

import os
import sys
import gc
import csv
import random
import time
import math
from datetime import datetime
from pathlib import Path

# Paths relative to script location
SCRIPT_DIR = Path(__file__).resolve().parent
STIMULI_DIR = SCRIPT_DIR / "STIMULI"
SHAPES_DIR = STIMULI_DIR / "Shapes"
CONTEXT_DIR = STIMULI_DIR / "Context_Images"
LOG_DIR = SCRIPT_DIR.parent / "LOG_FILES"
PHASE2_TRIAL_ORDER_CSV = SCRIPT_DIR / "phase2_trial_order.csv"

# Ensure LOG_FILES exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Suppress iohub if needed
os.environ.setdefault('PSYCHOPY_IOHUB', '0')

from psychopy import visual, core, event

# =========================
#  TTL / Parallel Port
# =========================
_ttl_backend = None
_ttl_line = int(os.environ.get('CEDRUS_TTL_LINE', '1'))
_ttl_pulse_ms = int(os.environ.get('CEDRUS_TTL_PULSE_MS', '10'))
_ttl_file_ref = [None]
_ttl_writer_ref = [None]
_last_ttl_timestamp = [None]


def _probe_ttl():
    """Initialize TTL backend (Cedrus pyxid2 or parallel port)."""
    global _ttl_backend
    if _ttl_backend is not None:
        return
    try:
        import pyxid2
        devices = pyxid2.get_xid_devices()
        if devices:
            dev = devices[0]
            dev.set_pulse_duration(_ttl_pulse_ms)
            _ttl_backend = ('cedrus', dev)
            print("TTL: Using Cedrus pyxid2", file=sys.stderr)
    except Exception:
        pass
    if _ttl_backend is None and sys.platform != 'darwin':
        try:
            from psychopy import parallel
            addr = int(os.environ.get('PARALLEL_PORT_ADDRESS', '0x0378'), 16)
            parallel.setPortAddress(addr)
            _ttl_backend = ('parallel', parallel)
            print("TTL: Using parallel port", file=sys.stderr)
        except Exception:
            _ttl_backend = False
            print("TTL WARNING: No backend. Triggers will NOT be sent.", file=sys.stderr)
    elif _ttl_backend is None and sys.platform == 'darwin':
        _ttl_backend = False
        print("TTL: Mac—no parallel port. Triggers logged only.", file=sys.stderr)


def _send_ttl():
    """Send TTL pulse."""
    try:
        if _ttl_backend is False:
            return
        if _ttl_backend is None:
            _probe_ttl()
        if _ttl_backend is False:
            return
        backend_type, backend = _ttl_backend
        if backend_type == 'cedrus':
            backend.activate_line(lines=_ttl_line)
        elif backend_type == 'parallel':
            backend.setData(255)
            core.wait(0.01)
            backend.setData(0)
    except Exception:
        pass


def _log_ttl_event(event_label, trigger_code=None, trial_info=None, participant=None):
    """Log TTL to CSV and send pulse. trigger_code defaults to event_label."""
    ts = time.time()
    _last_ttl_timestamp[0] = ts
    _send_ttl()
    code = trigger_code if trigger_code is not None else event_label
    row = {
        'timestamp': f"{ts:.9f}",
        'trigger_code': code,
        'event_label': event_label,
        'trial_info': trial_info if trial_info is not None else ''
    }
    if _ttl_writer_ref[0] is not None and _ttl_file_ref[0] is not None:
        try:
            _ttl_writer_ref[0].writerow(row)
            _ttl_file_ref[0].flush()
            try:
                os.fsync(_ttl_file_ref[0].fileno())
            except (AttributeError, OSError):
                pass
        except Exception as e:
            print(f"Warning: TTL log write failed: {e}", file=sys.stderr)


def is_test_participant(name):
    return name and 'test' in name.lower()


# =========================
#  Stimulus Helpers
# =========================
def get_shape_paths():
    """Return list of Shape_X_Y.png paths (exclude ShapeGrid)."""
    paths = []
    for f in SHAPES_DIR.glob("Shape_*.png"):
        if "ShapeGrid" not in f.name:
            paths.append(str(f))
    return sorted(paths)


def get_phase2_shapes():
    """12 shapes: exclude middle 4 (1_1, 1_2, 2_1, 2_2)."""
    all_shapes = get_shape_paths()
    exclude = {'Shape_1_1.png', 'Shape_1_2.png', 'Shape_2_1.png', 'Shape_2_2.png'}
    return [p for p in all_shapes if Path(p).name not in exclude]


def get_context_categories():
    """Return list of context category names from flat PNG filenames. Exclude practice1, practice2.
    Filenames: {name}1.png, {name}2.png or {name}_1.png, {name}_2.png. Category = name."""
    cats = set()
    for f in CONTEXT_DIR.glob("*.png"):
        if f.name in ('practice1.png', 'practice2.png'):
            continue
        name = f.stem
        if '_1' in name or '_2' in name:
            cats.add(name.rsplit('_', 1)[0])  # bookstore_1 -> bookstore, wall_1 -> wall
        elif name.endswith('1') or name.endswith('2'):
            cats.add(name[:-1])  # bedroom1 -> bedroom, pond1 -> pond
    return sorted(cats)


def get_context_image(category, variant):
    """
    Get context image path for a category. Flat structure: {category}1.png / {category}2.png
    or {category}_1.png / {category}_2.png. variant 'original' -> 1, 'control' -> 2.
    """
    suffix = '1' if variant == 'original' else '2'
    for stem in [f"{category}{suffix}", f"{category}_{suffix}"]:
        p = CONTEXT_DIR / f"{stem}.png"
        if p.exists():
            return str(p)
    return None


def get_shape_grid_path():
    """Return scrambled grid for Phase 1/3 display (shapes in randomized positions)."""
    return str(SHAPES_DIR / "ShapeGrid_4x4_scrambled.png")


def get_practice_context_paths():
    return [
        str(CONTEXT_DIR / "practice1.png"),
        str(CONTEXT_DIR / "practice2.png")
    ]


# =========================
#  Button / Wait Helpers — Enter only, no buttons, ESC exits
# =========================
def wait_for_continue(win, text_stim, event_label, log_ttl=True, min_display_sec=0, extra_drawables=None):
    """Wait for Enter. No buttons—Enter only. min_display_sec: minimum time before Enter is accepted.
    extra_drawables: optional list of stimuli to draw in addition to text_stim (e.g. progress bar)."""
    event.clearEvents()
    hint = visual.TextStim(win, text="Press Enter to continue.", color='gray', height=0.03, pos=(0, -0.35), units='height')
    extras = extra_drawables or []

    def draw():
        text_stim.draw()
        for s in extras:
            s.draw()
        hint.draw()

    if log_ttl:
        _log_ttl_event(f"{event_label}_onset")
    draw()
    win.flip()
    event.clearEvents()  # clear any key from previous screen
    core.wait(0.08)  # brief debounce so carried-over key isn't registered
    event.clearEvents()
    clock = core.Clock()
    clock.reset()
    return_pressed = False  # remember early Enter so user only needs to press once
    enter_keys = ['return', 'enter']  # return = main Enter; enter = numpad on some systems

    def accept_and_exit():
        if log_ttl:
            _log_ttl_event(f"{event_label}_enter")
            _log_ttl_event(f"{event_label}_offset")
        event.clearEvents()
        core.wait(0.15)  # debounce before returning to avoid carry-over to next screen
        return True

    while True:
        try:
            keys = event.getKeys(keyList=['escape'] + enter_keys, timeStamped=False)
        except (AttributeError, RuntimeError):
            keys = []
        if keys:
            if 'escape' in keys:
                core.quit()
            if any(k in keys for k in enter_keys):
                if clock.getTime() >= min_display_sec:
                    return accept_and_exit()
                return_pressed = True  # advance as soon as min time elapses
        if return_pressed and clock.getTime() >= min_display_sec:
            return accept_and_exit()
        draw()
        win.flip()
        core.wait(0.016)




# =========================
#  Phase 0: Participant Login — SRT-style fullscreen
# =========================
def get_participant_name(win):
    """Fullscreen text input like Social Recognition Task. Returns name or None if ESC."""
    _log_ttl_event("participant_name_onset")
    input_id = ""
    key_list = ['return', 'backspace'] + [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(48, 58)]
    id_prompt = visual.TextStim(win, text="Enter your first name and last initial with no spaces/capitals:\n\nHit Enter when done.",
                                color='black', height=0.045, wrapWidth=1.4, pos=(0, 0.25), units='height')
    input_display = visual.TextStim(win, text="", color='black', height=0.06, pos=(0, 0), units='height')

    def redraw():
        id_prompt.draw()
        input_display.text = f"{input_id}_"
        input_display.draw()
        win.flip()

    redraw()
    event.clearEvents()

    while True:
        try:
            keys = event.getKeys(keyList=key_list + ['escape'], timeStamped=False)
        except (AttributeError, RuntimeError):
            keys = []
        if keys:
            if 'escape' in keys:
                core.quit()
            key = keys[0]
            if key == 'return':
                if input_id.strip():
                    _log_ttl_event("participant_name_offset")
                    return input_id.strip() or 'anonymous'
            elif key == 'backspace':
                input_id = input_id[:-1] if input_id else ""
            elif len(key) == 1:
                input_id += key
        redraw()
        core.wait(0.016)


# =========================
#  Phase 1 & 3: Click-to-Place Task
# =========================
def _save_placement_image(results, output_path, win_size=(1920, 1080)):
    """Save placement visualization as PNG. results: list of {shape_path, final_x, final_y}."""
    try:
        from PIL import Image
    except ImportError:
        return
    w, h = win_size
    aspect = w / h
    # PsychoPy height units: y from -1 to 1, x from -aspect to aspect
    img = Image.new('RGB', (w, h), color='white')
    shape_size_px = int(0.1 * h)  # 0.1 height units
    for r in results:
        try:
            x = float(r.get('final_x', 0))
            y = float(r.get('final_y', 0))
        except (TypeError, ValueError):
            continue
        x_px = int((x / aspect + 1) / 2 * w)
        y_px = int((1 - y) / 2 * h)
        try:
            shape_img = Image.open(r['shape_path']).convert('RGBA')
            shape_img = shape_img.resize((shape_size_px, shape_size_px), Image.Resampling.LANCZOS)
            paste_x = x_px - shape_size_px // 2
            paste_y = y_px - shape_size_px // 2
            img.paste(shape_img, (paste_x, paste_y), shape_img)
        except Exception:
            pass
    img.save(output_path)


def run_drag_phase(win, mouse, shape_paths, phase_name, phase_num, participant, anchors=None, timestamp_str=None):
    """
    Sequential click-to-place task. shape_paths: list of shape file paths.
    anchors: dict {path: (x,y)} of previously placed shapes to show.
    Returns list of dicts: shape_path, final_x, final_y, rt, ttl timestamps.
    """
    if anchors is None:
        anchors = {}
    results = []
    fieldnames = ['shape_path', 'final_x', 'final_y', 'rt', 'stimulus_onset_ttl', 'stimulus_offset_ttl',
                  'click_ttl', 'all_click_ttl', 'submit_ttl']
    ts = timestamp_str or datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = LOG_DIR / f"phase{phase_num}_{participant}_{ts}.csv"
    if not is_test_participant(participant):
        f = open(csv_path, 'w', newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()
    else:
        f = None
        writer = None

    for idx, shape_path in enumerate(shape_paths):
        # 1 second: shape alone (screen cleared per spec)
        img = visual.ImageStim(win, image=shape_path, units='height', size=(0.15, 0.15))
        img.setPos((0, 0))
        _log_ttl_event(f"{phase_name}_stimulus_onset", trial_info=f"trial={idx+1}")
        img.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event(f"{phase_name}_stimulus_offset", trial_info=f"trial={idx+1}")
        del img  # free texture before creating more stims

        # Now clickable: click anywhere to place
        shape_name = Path(shape_path).name
        stim = visual.ImageStim(win, image=shape_path, units='height', size=(0.15, 0.15))
        stim.setPos((0, 0))

        # Pre-create anchor stims and hint once (avoids per-frame allocation lag)
        anchor_stims = [(visual.ImageStim(win, image=p, units='height', size=(0.1, 0.1)), ax, ay)
                       for p, (ax, ay) in anchors.items()]
        hint = visual.TextStim(win, text="Click to place. Press Enter to submit.", color='gray', height=0.028, pos=(0, -0.38), units='height')

        rt_start = time.time()
        submitted = False
        prev_pressed = False
        click_times = []  # all click timestamps (Unix)
        while not submitted:
            try:
                keys = event.getKeys(keyList=['escape', 'return'], timeStamped=False)
            except (AttributeError, RuntimeError):
                keys = []
            if keys:
                if 'escape' in keys:
                    core.quit()
                if 'return' in keys:
                    # RT = time from onset to last click (or Enter if no clicks)
                    last_click_time = click_times[-1] if click_times else time.time()
                    rt = last_click_time - rt_start
                    _log_ttl_event(f"{phase_name}_enter_submit", trial_info=f"trial={idx+1} shape={shape_name}")
                    submitted = True
            pressed = mouse.getPressed()[0]
            if pressed and not prev_pressed:
                mpos = mouse.getPos()
                stim.setPos(mpos)
                click_ts = time.time()
                click_times.append(click_ts)
                _log_ttl_event(f"{phase_name}_click_place", trial_info=f"trial={idx+1} shape={shape_name} click={len(click_times)}")
            prev_pressed = pressed
            for a, ax, ay in anchor_stims:
                a.setPos((ax, ay))
                a.draw()
            stim.draw()
            hint.draw()
            win.flip()

        fx, fy = stim.pos
        first_click_ttl = click_times[0] if click_times else None
        all_click_ttl_str = ';'.join(f"{t:.9f}" for t in click_times) if click_times else ''
        row = {
            'shape_path': shape_path,
            'final_x': f"{fx:.6f}",
            'final_y': f"{fy:.6f}",
            'rt': f"{rt:.4f}",
            'stimulus_onset_ttl': '',
            'stimulus_offset_ttl': '',
            'click_ttl': f"{first_click_ttl:.9f}" if first_click_ttl else '',
            'all_click_ttl': all_click_ttl_str,
            'submit_ttl': f"{_last_ttl_timestamp[0]:.9f}" if _last_ttl_timestamp[0] else ''
        }
        results.append(row)
        anchors[shape_path] = (float(fx), float(fy))
        del stim
        del anchor_stims

        if idx > 0 and (idx + 1) % 4 == 0:
            gc.collect()

        if writer:
            writer.writerow(row)
            f.flush()
            try:
                os.fsync(f.fileno())
            except (AttributeError, OSError):
                pass

        # Save placement image incrementally (overwrites each time; preserves progress if task crashes)
        if not is_test_participant(participant) and results:
            try:
                win_size = win.size if hasattr(win, 'size') else (1920, 1080)
                png_path = LOG_DIR / f"phase{phase_num}_placements_{participant}_{ts}.png"
                _save_placement_image(results, png_path, win_size)
                _log_ttl_event(f"phase{phase_num}_placements_saved", trial_info=f"{png_path.name} trial={idx+1}")
            except Exception as e:
                print(f"Warning: Could not save placement image: {e}", file=sys.stderr)

    if f:
        f.close()

    return results


# =========================
#  Tutorial — Video with subtitles (red square, red circle, green circle)
# =========================
# Place tutorial video at STIMULI/tutorial_video.mp4. Video should show clicking to place;
# subtitles describe what's on screen (not instructions read aloud).
# If missing, plays animated fallback simulating the click-to-place sequence.
TUTORIAL_VIDEO = STIMULI_DIR / "tutorial_video.mp4"


def _show_click_place(win, shape_stim, start_pos, end_pos, subtitle, anchors=None):
    """Show click-to-place: shape at center briefly, then at target (no dragging). Text on screen at least 2 s.
    anchors: optional list of (stim, (x,y)) for previously placed shapes to keep visible (like actual task)."""
    sub = visual.TextStim(win, text=subtitle, color='black', height=0.032, pos=(0, -0.42),
                          wrapWidth=1.3, units='height', alignText='center')
    anchor_list = anchors or []

    def draw_all():
        for a_stim, a_pos in anchor_list:
            a_stim.setPos(a_pos)
            a_stim.draw()
        shape_stim.draw()
        sub.draw()

    shape_stim.setPos(start_pos)
    draw_all()
    win.flip()
    core.wait(1.0)
    shape_stim.setPos(end_pos)
    draw_all()
    win.flip()
    core.wait(2.0)


def run_tutorial_phase1(win, mouse, participant):
    """Tutorial: video with subtitles, or animated fallback showing click-to-place. Shapes: red square, red circle, green circle."""
    used_fallback = True
    if TUTORIAL_VIDEO.exists():
        try:
            movie = visual.MovieStim(win, str(TUTORIAL_VIDEO), play=True)
            _log_ttl_event("tutorial_video_onset")
            while movie.status != visual.FINISHED:
                try:
                    keys = event.getKeys(keyList=['escape'], timeStamped=False)
                except (AttributeError, RuntimeError):
                    keys = []
                if keys and 'escape' in keys:
                    core.quit()
                movie.draw()
                win.flip()
            _log_ttl_event("tutorial_video_offset")
            used_fallback = False
        except Exception as e:
            print(f"Video playback failed, using fallback: {e}", file=sys.stderr)

    if used_fallback:
        # Click-to-place sequence (no dragging): shape appears at center, then at target
        sq = visual.Rect(win, width=0.16, height=0.16, fillColor='red', lineColor=None)
        circ_red = visual.Circle(win, radius=0.08, fillColor='red', lineColor=None)
        circ_green = visual.Circle(win, radius=0.08, fillColor='green', lineColor=None)

        # Positions: square on left, circles on right (sorted by shape)
        sq_pos = (-0.45, 0.08)
        circ_red_pos = (0.2, 0.08)
        circ_green_pos = (0.45, 0.08)

        # Step 1: Three shapes overview
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=1")
        sq.setPos((-0.35, 0))
        circ_red.setPos((0, 0))
        circ_green.setPos((0.35, 0))
        sub1 = visual.TextStim(win, text="Three shapes appear.", color='black', height=0.032, pos=(0, -0.42),
                              wrapWidth=1.3, units='height', alignText='center')
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        sub1.draw()
        win.flip()
        core.wait(2.5)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=1")

        # Step 2: Red square appears at center, clicks to place on left (no anchors yet)
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=2")
        _show_click_place(win, sq, (0, 0), sq_pos, "Red square appears. Clicking to place on the left.")
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=2")

        # Step 3: Red circle appears at center, clicks to place on right (square stays visible)
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=3")
        circ_red.setPos((0, 0))
        _show_click_place(win, circ_red, (0, 0), circ_red_pos, "Red circle appears. Clicking to place on the right.",
                          anchors=[(sq, sq_pos)])
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=3")

        # Step 4: Green circle appears at center, clicks to place on right (square and red circle stay visible)
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=4")
        circ_green.setPos((0, 0))
        _show_click_place(win, circ_green, (0, 0), circ_green_pos, "Green circle appears. Clicking to place on the right.",
                          anchors=[(sq, sq_pos), (circ_red, circ_red_pos)])
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=4")

        # Step 5a: Shape vs color
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=5a")
        sq.setPos(sq_pos)
        circ_red.setPos(circ_red_pos)
        circ_green.setPos(circ_green_pos)
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        sub_5a = visual.TextStim(win, text="We sorted by shapes but could have sorted by color.",
                                color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
        sub_5a.draw()
        win.flip()
        core.wait(3.0)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=5a")

        # Step 5b: Distance denotes group
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=5b")
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        sub_5b = visual.TextStim(win, text="You're grouping into groups—not arranging on a line or spectrum. Shapes closer together are in the same group.",
                                color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
        sub_5b.draw()
        win.flip()
        core.wait(4.0)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=5b")

        # Step 6: Press Enter subtitle
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=6")
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        sub_5c = visual.TextStim(win, text="Objects in a group can still be slightly further apart than from objects in another group.",
                                color='black', height=0.028, pos=(0, -0.35), wrapWidth=1.3, units='height', alignText='center')
        sub_enter = visual.TextStim(win, text="Click to place. Press Enter to submit.",
                                   color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
        sub_5c.draw()
        sub_enter.draw()
        win.flip()
        core.wait(2.5)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=6")

    # Debrief
    debrief = visual.TextStim(win, text="In this practice, we sorted all objects by shape!",
                              color='black', height=0.04, pos=(0, 0), wrapWidth=1.2, units='height')
    if not wait_for_continue(win, debrief, "tutorial_debrief"):
        return False

    # Transition
    trans = visual.TextStim(win, text="Let's get started on your task!", color='black', height=0.04, pos=(0, 0),
                           wrapWidth=1.2, units='height')
    return wait_for_continue(win, trans, "tutorial_transition")


# =========================
#  Phase 2: Context Task
# =========================
def load_phase2_trials():
    """
    Load Phase 2 trial order from phase2_trial_order.csv. Same fixed order for all participants.
    CSV columns: trial_number, shape, shape_path, strong_context, neutral_context,
    context1, context1_image, context2, context2_image, variant.
    Paths in CSV are relative to STIMULI_DIR.
    """
    if not PHASE2_TRIAL_ORDER_CSV.exists():
        raise FileNotFoundError(f"Phase 2 trial order file not found: {PHASE2_TRIAL_ORDER_CSV}")
    trials = []
    with open(PHASE2_TRIAL_ORDER_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shape_path = str(STIMULI_DIR / row['shape_path'].strip())
            ctx1_path = str(STIMULI_DIR / row['context1_image'].strip())
            ctx2_path = str(STIMULI_DIR / row['context2_image'].strip())
            trials.append({
                'shape_path': shape_path,
                'context_1': ctx1_path,
                'context_2': ctx2_path,
                'cat_a': row['context1'].strip(),
                'cat_b': row['context2'].strip(),
                'variant': row['variant'].strip(),
            })
    return trials


def run_phase2_tutorial(win, mouse, participant):
    """Phase 2 tutorial: explicit intro screens, then practice1, practice2, circle, CIRCUS | SPACE."""
    # Single intro screen (max 2 sentences) — one Enter before demo
    intro = visual.TextStim(win, text="In this example, you'll see a space picture, then a circle, then a circus picture. Say what the shape could be in each, then watch as we pick which fits better.",
                            color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, intro, "phase2_tutorial_intro"):
        return False

    p1, p2 = get_practice_context_paths()
    circ = visual.Circle(win, radius=0.2, fillColor='blue', lineColor=None)
    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    blank = visual.Rect(win, width=3, height=3, fillColor='white', lineColor=None, pos=(0, 0), units='height')
    dot = visual.Circle(win, radius=0.006, fillColor='red', lineColor=None, pos=(0, 0))
    img1 = visual.ImageStim(win, image=p1, units='height', size=(0.5, 0.5))
    img2 = visual.ImageStim(win, image=p2, units='height', size=(0.5, 0.5))

    # Fixation 500ms
    _log_ttl_event("phase2_tutorial_fixation_onset")
    fix.draw()
    win.flip()
    core.wait(0.5)
    _log_ttl_event("phase2_tutorial_fixation_offset")

    # Practice context 1 - 1000ms
    _log_ttl_event("phase2_tutorial_context1_onset")
    img1.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_context1_offset")

    # Big blue circle - 1000ms
    _log_ttl_event("phase2_tutorial_shape_onset")
    circ.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_shape_offset")

    # Blank 1000ms
    _log_ttl_event("phase2_tutorial_blank_onset")
    blank.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_blank_offset")

    # Red dot + "PLANET" 3000ms
    _log_ttl_event("phase2_tutorial_reddot_onset")
    dot.draw()
    txt1 = visual.TextStim(win, text="You might say the circle is a 'PLANET'", color='black', height=0.04, pos=(0, -0.2))
    txt1.draw()
    win.flip()
    core.wait(3.0)
    _log_ttl_event("phase2_tutorial_reddot_offset")

    # Practice context 2 - 1000ms
    _log_ttl_event("phase2_tutorial_context2_onset")
    img2.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_context2_offset")

    # Same circle - 1000ms
    _log_ttl_event("phase2_tutorial_shape2_onset")
    circ.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_shape2_offset")

    # Blank 1000ms
    _log_ttl_event("phase2_tutorial_blank2_onset")
    blank.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_blank2_offset")

    # Red dot + "BALL" 3000ms
    _log_ttl_event("phase2_tutorial_reddot2_onset")
    dot.draw()
    txt2 = visual.TextStim(win, text="You might say the circle is a 'BALL'", color='black', height=0.04, pos=(0, -0.2))
    txt2.draw()
    win.flip()
    core.wait(3.0)
    _log_ttl_event("phase2_tutorial_reddot2_offset")

    # Question: CIRCUS | SPACE — demo only (participant watches, no click)
    q = visual.TextStim(win, text="Which context fits the object better?", color='black', height=0.04, pos=(0, 0.1))
    btn_circus = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', pos=(-0.2, -0.2), units='height')
    btn_space = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', pos=(0.2, -0.2), units='height')
    txt_c = visual.TextStim(win, text="CIRCUS", color='black', height=0.03, pos=(-0.2, -0.2), units='height')
    txt_s = visual.TextStim(win, text="SPACE", color='black', height=0.03, pos=(0.2, -0.2), units='height')
    _log_ttl_event("phase2_tutorial_question_onset")
    # Show question + buttons for ~1.5 s
    q.draw()
    btn_circus.draw()
    btn_space.draw()
    txt_c.draw()
    txt_s.draw()
    win.flip()
    core.wait(1.5)
    # Animate SPACE button being pressed (highlight/darken)
    btn_space_pressed = visual.Rect(win, width=0.2, height=0.06, fillColor='steelblue', lineColor='black', pos=(0.2, -0.2), units='height')
    q.draw()
    btn_circus.draw()
    btn_space_pressed.draw()  # darker = "pressed"
    txt_c.draw()
    txt_s.draw()
    win.flip()
    _log_ttl_event("phase2_tutorial_response", trial_info="SPACE")
    core.wait(1.0)
    _log_ttl_event("phase2_tutorial_question_offset")
    _log_ttl_event("phase2_tutorial_post_blank_onset")
    blank.draw()
    win.flip()
    core.wait(3.0)
    _log_ttl_event("phase2_tutorial_post_blank_offset")

    # Ready screen
    ready = visual.TextStim(win, text="Ready to try this with some actual shapes and images?",
                            color='black', height=0.04, pos=(0, 0), wrapWidth=1.2, units='height')
    cont_btn = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', lineColor='black', pos=(0, -0.3), units='height')
    cont_txt = visual.TextStim(win, text="CONTINUE", color='black', height=0.03, pos=(0, -0.3), units='height')
    return wait_for_continue(win, ready, "phase2_ready")


def run_phase2_trials(win, mouse, trials, participant, timestamp_str=None):
    """Run Phase 2 trials from phase2_trial_order.csv with breaks every 12."""
    fieldnames = ['trial', 'shape_path', 'context_1_path', 'context_2_path', 'trial_variant', 'response',
                   'rt', 'fixation_onset_ttl', 'context1_onset_ttl', 'shape_onset_ttl', 'reddot_onset_ttl',
                   'context2_onset_ttl', 'shape2_onset_ttl', 'reddot2_onset_ttl', 'question_onset_ttl', 'response_ttl']
    ts = timestamp_str or datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = LOG_DIR / f"phase2_{participant}_{ts}.csv"
    if not is_test_participant(participant):
        f = open(csv_path, 'w', newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()
    else:
        f = None
        writer = None

    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    blank = visual.Rect(win, width=3, height=3, fillColor='white', lineColor=None, pos=(0, 0), units='height')
    dot = visual.Circle(win, radius=0.006, fillColor='red', lineColor=None, pos=(0, 0))

    total_trials = len(trials)
    for t_idx, trial in enumerate(trials):
        if t_idx > 0 and t_idx % 12 == 0:
            pct = int(100 * t_idx / total_trials)
            break_text = visual.TextStim(win, text="Take a break!",
                                        color='black', height=0.04, pos=(0, 0.1), wrapWidth=1.2, units='height')
            bar_w, bar_h = 0.8, 0.04
            bar_bg = visual.Rect(win, width=bar_w, height=bar_h, fillColor='lightgray', lineColor='gray',
                                pos=(0, -0.15), units='height')
            fill_w = (t_idx / total_trials) * bar_w
            bar_fill = visual.Rect(win, width=max(fill_w, 0.01), height=bar_h * 0.9, fillColor='steelblue', lineColor=None,
                                  pos=(-bar_w / 2 + max(fill_w, 0.01) / 2, -0.15), units='height')
            pct_text = visual.TextStim(win, text=f"{pct}%", color='black', height=0.03, pos=(0, -0.25), units='height')
            _log_ttl_event("phase2_break_onset", trial_info=f"after_trial={t_idx}")
            wait_for_continue(win, break_text, "phase2_break", extra_drawables=[bar_bg, bar_fill, pct_text])

        # Fixation 500ms
        _log_ttl_event("phase2_fixation_onset", trial_info=f"trial={t_idx+1}")
        fix.draw()
        win.flip()
        core.wait(0.5)
        _log_ttl_event("phase2_fixation_offset", trial_info=f"trial={t_idx+1}")

        ctx1 = visual.ImageStim(win, image=trial['context_1'], units='height', size=(0.5, 0.5))
        ctx2 = visual.ImageStim(win, image=trial['context_2'], units='height', size=(0.5, 0.5))
        shape_img = visual.ImageStim(win, image=trial['shape_path'], units='height', size=(0.2, 0.2))
        cat_a = trial['cat_a'].upper()
        cat_b = trial['cat_b'].upper()

        _log_ttl_event("phase2_context1_onset", trial_info=f"trial={t_idx+1}")
        ctx1.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event("phase2_context1_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_shape_onset", trial_info=f"trial={t_idx+1}")
        shape_img.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event("phase2_shape_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_blank1_onset", trial_info=f"trial={t_idx+1}")
        blank.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event("phase2_blank1_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_reddot_onset", trial_info=f"trial={t_idx+1}")
        dot.draw()
        win.flip()
        core.wait(3.0)
        _log_ttl_event("phase2_reddot_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_context2_onset", trial_info=f"trial={t_idx+1}")
        ctx2.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event("phase2_context2_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_shape2_onset", trial_info=f"trial={t_idx+1}")
        shape_img.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event("phase2_shape2_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_blank2_onset", trial_info=f"trial={t_idx+1}")
        blank.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event("phase2_blank2_offset", trial_info=f"trial={t_idx+1}")

        _log_ttl_event("phase2_reddot2_onset", trial_info=f"trial={t_idx+1}")
        dot.draw()
        win.flip()
        core.wait(3.0)
        _log_ttl_event("phase2_reddot2_offset", trial_info=f"trial={t_idx+1}")

        # Question
        q = visual.TextStim(win, text="Which context fits the object better?", color='black', height=0.04, pos=(0, 0.1))
        btn_a = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', pos=(-0.2, -0.2), units='height')
        btn_b = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', pos=(0.2, -0.2), units='height')
        txt_a = visual.TextStim(win, text=cat_a, color='black', height=0.03, pos=(-0.2, -0.2), units='height')
        txt_b = visual.TextStim(win, text=cat_b, color='black', height=0.03, pos=(0.2, -0.2), units='height')
        _log_ttl_event("phase2_question_onset", trial_info=f"trial={t_idx+1}")
        rt_clock = core.Clock()
        rt_clock.reset()
        response = None
        while response is None:
            try:
                keys = event.getKeys(keyList=['escape'], timeStamped=False)
            except (AttributeError, RuntimeError):
                keys = []
            if keys and 'escape' in keys:
                core.quit()
            mpos = mouse.getPos()
            mbuttons = mouse.getPressed()
            if mbuttons[0]:
                if -0.3 <= mpos[0] <= -0.1 and -0.23 <= mpos[1] <= -0.17:
                    response = cat_a
                    break
                if 0.1 <= mpos[0] <= 0.3 and -0.23 <= mpos[1] <= -0.17:
                    response = cat_b
                    break
            q.draw()
            btn_a.draw()
            btn_b.draw()
            txt_a.draw()
            txt_b.draw()
            win.flip()
            core.wait(0.02)
        rt = rt_clock.getTime()
        _log_ttl_event("phase2_response", trial_info=f"trial={t_idx+1} response={response}")
        _log_ttl_event("phase2_question_offset", trial_info=f"trial={t_idx+1}")

        row = {
            'trial': t_idx + 1,
            'shape_path': trial['shape_path'],
            'context_1_path': trial['context_1'],
            'context_2_path': trial['context_2'],
            'trial_variant': trial['variant'],
            'response': response,
            'rt': f"{rt:.4f}",
            'fixation_onset_ttl': '',
            'context1_onset_ttl': '',
            'shape_onset_ttl': '',
            'reddot_onset_ttl': '',
            'context2_onset_ttl': '',
            'shape2_onset_ttl': '',
            'reddot2_onset_ttl': '',
            'question_onset_ttl': '',
            'response_ttl': f"{_last_ttl_timestamp[0]:.9f}" if _last_ttl_timestamp[0] else ''
        }
        if writer:
            writer.writerow(row)
            f.flush()
            try:
                os.fsync(f.fileno())
            except (AttributeError, OSError):
                pass

        _log_ttl_event("phase2_trial_iti_onset", trial_info=f"trial={t_idx+1}")
        blank.draw()
        win.flip()
        core.wait(0.5)
        _log_ttl_event("phase2_trial_iti_offset", trial_info=f"trial={t_idx+1}")

        del ctx1, ctx2, shape_img
        if (t_idx + 1) % 12 == 0:
            gc.collect()

    if f:
        f.close()


# =========================
#  Summary CSV
# =========================
def run_phase3_debrief(win, mouse, participant, timestamp_str=None):
    """Three Yes/No questions at end of Phase 3. Returns list of dicts or None if ESC."""
    questions = [
        "Did you use the same grouping strategy as the first time you sorted these shapes?",
        "Did the images associated with each shape you saw influence your grouping the second time around?",
        "After thinking about how shapes might fit in different environments, did you find yourself interpreting the shapes differently when you sorted them the second time?",
    ]
    fieldnames = ['question', 'question_text', 'answer', 'rt', 'onset_ttl', 'response_ttl']
    ts = timestamp_str or datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = LOG_DIR / f"debrief_{participant}_{ts}.csv"
    if not is_test_participant(participant):
        f = open(csv_path, 'w', newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()
    else:
        f = None
        writer = None

    results = []
    for i, qtext in enumerate(questions):
        q = visual.TextStim(win, text=qtext, color='black', height=0.04, pos=(0, 0.1), wrapWidth=1.3, units='height')
        btn_yes = visual.Rect(win, width=0.18, height=0.06, fillColor='lightgreen', lineColor='black', pos=(-0.22, -0.25), units='height')
        btn_no = visual.Rect(win, width=0.18, height=0.06, fillColor='lightcoral', lineColor='black', pos=(0.22, -0.25), units='height')
        txt_yes = visual.TextStim(win, text="Yes", color='black', height=0.03, pos=(-0.22, -0.25), units='height')
        txt_no = visual.TextStim(win, text="No", color='black', height=0.03, pos=(0.22, -0.25), units='height')

        _log_ttl_event("phase3_debrief_onset", trial_info=f"question={i+1}")
        onset_ttl = _last_ttl_timestamp[0]
        rt_clock = core.Clock()
        rt_clock.reset()
        answer = None

        while answer is None:
            try:
                keys = event.getKeys(keyList=['escape'], timeStamped=False)
            except (AttributeError, RuntimeError):
                keys = []
            if keys and 'escape' in keys:
                if f:
                    f.close()
                return None
            mpos = mouse.getPos()
            mbuttons = mouse.getPressed()
            if mbuttons[0]:
                if -0.31 <= mpos[0] <= -0.13 and -0.28 <= mpos[1] <= -0.22:
                    answer = "Yes"
                    break
                if 0.13 <= mpos[0] <= 0.31 and -0.28 <= mpos[1] <= -0.22:
                    answer = "No"
                    break
            q.draw()
            btn_yes.draw()
            btn_no.draw()
            txt_yes.draw()
            txt_no.draw()
            win.flip()
            core.wait(0.016)

        rt = rt_clock.getTime()
        _log_ttl_event("phase3_debrief_response", trial_info=f"question={i+1} answer={answer}")
        response_ttl = _last_ttl_timestamp[0]

        row = {
            'question': i + 1,
            'question_text': qtext,
            'answer': answer,
            'rt': f"{rt:.4f}",
            'onset_ttl': f"{onset_ttl:.9f}" if onset_ttl else '',
            'response_ttl': f"{response_ttl:.9f}" if response_ttl else ''
        }
        results.append(row)
        if writer:
            writer.writerow(row)
            f.flush()
            try:
                os.fsync(f.fileno())
            except (AttributeError, OSError):
                pass

    if f:
        f.close()
    return results


def _euclidean_distances(positions):
    """positions: list of (x,y). Return list of pairwise distances (i,j) for i<j."""
    n = len(positions)
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            xi, yi = float(positions[i][0]), float(positions[i][1])
            xj, yj = float(positions[j][0]), float(positions[j][1])
            d = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            dists.append(f"{i}-{j}:{d:.4f}")
    return ";".join(dists)


def _parse_shape_grid_position(shape_path):
    """Extract (row, col, gx, gy) from Shape_X_Y.png. X,Y are integer indices 0-3.
    Grid centers: row/col 0->0.10, 1->1.70, 2->3.30, 3->4.90."""
    name = Path(shape_path).stem
    row_to_g = {0: 0.10, 1: 1.70, 2: 3.30, 3: 4.90}
    try:
        parts = name.replace('Shape_', '').split('_')
        if len(parts) >= 2:
            row, col = int(parts[0]), int(parts[1])
            if 0 <= row <= 3 and 0 <= col <= 3:
                return row, col, row_to_g[row], row_to_g[col]
    except (ValueError, IndexError):
        pass
    return -1, -1, 0, 0


def write_summary(participant, experiment_start, experiment_end, phase1_results, phase3_results, timestamp_str=None):
    """Write summary_{participant}_{timestamp}.csv. Skipped if 'test' in participant name."""
    if is_test_participant(participant):
        return
    grid_path = get_shape_grid_path()
    try:
        from PIL import Image
        img = Image.open(grid_path)
        w, h = img.size
    except Exception:
        w, h = 0, 0
    total_time = experiment_end - experiment_start
    fieldnames = ['participant_id', 'total_task_time_seconds', 'shapegrid_width_px', 'shapegrid_height_px',
                  'grid_border_coords', 'per_shape_ground_truth', 'scaling_factor', 'phase3_euclidean_distances']
    ts = timestamp_str or datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = LOG_DIR / f"summary_{participant}_{ts}.csv"
    phase3_dists = ''
    if phase3_results:
        positions = []
        for r in phase3_results:
            try:
                x = float(r.get('final_x', 0))
                y = float(r.get('final_y', 0))
            except (TypeError, ValueError):
                x, y = 0, 0
            positions.append((x, y))
        phase3_dists = _euclidean_distances(positions)
    per_shape_gt = []
    for p in get_shape_paths():
        row, col, gx, gy = _parse_shape_grid_position(p)
        per_shape_gt.append(f"{Path(p).name}:row={row},col={col},center_x={gx},center_y={gy}")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'participant_id': participant,
            'total_task_time_seconds': f"{total_time:.2f}",
            'shapegrid_width_px': w,
            'shapegrid_height_px': h,
            'grid_border_coords': '',
            'per_shape_ground_truth': '|'.join(per_shape_gt),
            'scaling_factor': '',
            'phase3_euclidean_distances': phase3_dists
        })
        f.flush()
    _log_ttl_event("summary_saved", trial_info=str(csv_path.name))


# =========================
#  Main
# =========================
def main():
    global _ttl_file_ref, _ttl_writer_ref
    gc.collect()
    # Do NOT use event.globalKeys for escape (like Social Recognition Task).
    # globalKeys can cause random quits from key repeat or during transitions.
    # Escape is checked explicitly in each input loop instead.

    # Dummy window (helps stability/OOM on some systems, e.g. Social Recognition Task). Disable: PSYCHOPY_DUMMY_WINDOW=0
    use_dummy = os.environ.get('PSYCHOPY_DUMMY_WINDOW', '1').lower() not in ('0', 'false', 'no')
    dummy_win = None
    if use_dummy:
        try:
            dummy_win = visual.Window(size=(100, 100), pos=(0, 0), color='white', allowGUI=False)
        except Exception:
            pass

    # Fullscreen by default. Override with PSYCHOPY_WINDOWED=1 for windowed mode (1280×720).
    _default_windowed = '0'
    use_windowed = os.environ.get('PSYCHOPY_WINDOWED', _default_windowed).lower() in ('1', 'true', 'yes')
    win_size = (1280, 720) if use_windowed else (1920, 1080)
    win = visual.Window(
        size=win_size,
        fullscr=not use_windowed,
        color='white',
        units='height',
        allowGUI=False
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    def _close_dummy():
        if dummy_win is not None:
            try:
                dummy_win.close()
            except Exception:
                pass

    _probe_ttl()
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    ttl_path = LOG_DIR / f"ttl_log_{timestamp_str}.csv"
    _ttl_file_ref[0] = open(ttl_path, 'w', newline='')
    _ttl_writer_ref[0] = csv.DictWriter(_ttl_file_ref[0], fieldnames=['timestamp', 'trigger_code', 'event_label', 'trial_info'])
    _ttl_writer_ref[0].writeheader()
    _ttl_file_ref[0].flush()

    participant = get_participant_name(win)
    participant = participant.strip() or 'anonymous'

    experiment_start = time.time()
    _log_ttl_event("experiment_start", trial_info=f"participant={participant}")

    # Welcome
    welcome = visual.TextStim(win, text="Welcome! Let's get started. First, watch this example video of how we work on this task.",
                              color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    cont_btn = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', lineColor='black', pos=(0, -0.3), units='height')
    cont_txt = visual.TextStim(win, text="CONTINUE", color='black', height=0.03, pos=(0, -0.3), units='height')
    if not wait_for_continue(win, welcome, "welcome"):
        win.close()
        _close_dummy()
        return

    # Tutorial Phase 1
    if not run_tutorial_phase1(win, mouse, participant):
        win.close()
        _close_dummy()
        return

    # Phase 1 — split instructions (max 2 sentences per screen)
    p1_screens = [
        ("Let's sort some shapes. First you will see all of them.", "phase1_instr1", 0),
        ("Then place them one at a time by clicking where you want each to go, as in the practice.", "phase1_instr2", 0),
        ("Group them into groups—not on a spectrum or line. Shapes closer together are in the same group.", "phase1_instr3", 0),
        ("Use as many groups as you need.", "phase1_instr4", 8.0),
    ]
    for text, label, min_sec in p1_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label, min_display_sec=min_sec):
            win.close()
            _close_dummy()
            return

    # Before grid: 16 shapes, no need to memorize
    p1_before_grid = [
        ("You will see 16 shapes. You do not need to memorize them, recreate this grid, or remember any of the shapes—you will see them all together just for context.", "phase1_before_grid", 0),
    ]
    for text, label, _ in p1_before_grid:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label):
            win.close()
            _close_dummy()
            return

    # Grid 5 sec
    grid_path = get_shape_grid_path()
    grid_img = visual.ImageStim(win, image=grid_path, units='height', size=(0.8, 0.8))
    _log_ttl_event("phase1_grid_onset")
    grid_img.draw()
    win.flip()
    core.wait(5.0)
    _log_ttl_event("phase1_grid_offset")

    # Fixation 1 sec
    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    _log_ttl_event("phase1_fixation_onset")
    fix.draw()
    win.flip()
    core.wait(1.0)
    _log_ttl_event("phase1_fixation_offset")

    p1_instr2_screens = [
        ("You'll see the shapes from before, one at a time. Group each where you think it belongs.", "phase1_instruction2a", 0),
        ("Group into groups—not on a spectrum or line. Shapes closer together are in the same group.", "phase1_instruction2b", 0),
        ("Click to place, press Enter to submit. Once you've submitted the position of a shape, you can't move it again.", "phase1_instruction2c", 0),
    ]
    for text, label, _ in p1_instr2_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label):
            win.close()
            _close_dummy()
            return

    shapes = get_shape_paths()
    random.shuffle(shapes)
    if Path(shapes[0]).name == "Shape_0_0.png":
        shapes.append(shapes.pop(0))
    phase1_results = run_drag_phase(win, mouse, shapes, "phase1", 1, participant, timestamp_str=timestamp_str)
    if phase1_results is None:
        win.close()
        _close_dummy()
        return
    gc.collect()

    # Phase 2 — split instructions (max 2 sentences per screen), explicit explanation
    p2_screens = [
        ("Now you'll see the shapes again, paired with different pictures. Each shape appears with two pictures.", "phase2_instr1", 0),
        ("For each picture, say out loud what the shape could be. For example: planet, ball, or cookie.", "phase2_instr2", 0),
        ("Then click which picture the shape fits better with. We need to hear you say it every time.", "phase2_instr3", 0),
        ("Do your best since you will be recorded, but don't panic if nothing comes to mind.", "phase2_instr4", 0),
        ("You can also re-use answers.", "phase2_instr5", 0),
        ("Here's an example to show you how it works.", "phase2_instr6", 5.0),
    ]
    for text, label, min_sec in p2_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label, min_display_sec=min_sec):
            win.close()
            _close_dummy()
            return

    if not run_phase2_tutorial(win, mouse, participant):
        win.close()
        _close_dummy()
        return

    trials = load_phase2_trials()
    run_phase2_trials(win, mouse, trials, participant, timestamp_str=timestamp_str)
    del trials
    gc.collect()

    # Phase 3 — split instructions (max 2 sentences per screen)
    p3_screens = [
        ("Let's sort some shapes again, like we did in the VERY beginning. Click to place each shape where you think it belongs.", "phase3_instr1", 0),
        ("Again, shapes closer together are ones you're grouping as more similar.", "phase3_instr2", 0),
        ("Feel free to use whatever grouping feels intuitive.", "phase3_instr3", 0),
        ("Once you've submitted the position of a shape, you can't move it again.", "phase3_instr4", 0),
    ]
    gc.collect()  # free Phase 2 memory before Phase 3 task
    for text, label, _ in p3_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label):
            win.close()
            _close_dummy()
            return

    shapes3 = get_shape_paths()
    random.shuffle(shapes3)
    while shapes3 == shapes:
        random.shuffle(shapes3)
    phase3_results = run_drag_phase(win, mouse, shapes3, "phase3", 3, participant, timestamp_str=timestamp_str)
    gc.collect()
    if phase3_results is None:
        win.close()
        _close_dummy()
        return

    # Phase 3 debrief questions
    debrief_results = run_phase3_debrief(win, mouse, participant, timestamp_str=timestamp_str)
    if debrief_results is None:
        win.close()
        _close_dummy()
        return

    experiment_end = time.time()
    write_summary(participant, experiment_start, experiment_end, phase1_results, phase3_results, timestamp_str=timestamp_str)

    _log_ttl_event("experiment_end", trial_info=f"participant={participant}")

    if _ttl_file_ref[0]:
        _ttl_file_ref[0].close()
        _ttl_file_ref[0] = None
        if is_test_participant(participant):
            try:
                ttl_path.unlink(missing_ok=True)
            except Exception:
                pass
        else:
            try:
                new_path = LOG_DIR / f"ttl_log_{participant}_{timestamp_str}.csv"
                if new_path != ttl_path:
                    ttl_path.rename(new_path)
            except Exception:
                pass

    thanks = visual.TextStim(win, text="Thank you! Task complete.", color='black', height=0.05, pos=(0, 0))
    _log_ttl_event("thanks_onset")
    thanks.draw()
    win.flip()
    core.wait(2.0)
    _log_ttl_event("thanks_offset")
    win.close()
    _close_dummy()


if __name__ == '__main__':
    main()
