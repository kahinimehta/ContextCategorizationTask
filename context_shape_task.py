#!/usr/bin/env python3
"""
ContextShape Task — PsychoPy Implementation
Environment: Python (Anaconda), PsychoPy v2025.1.1
Fullscreen with DPI scaling. ESC exits at any time.
TTL triggers via Blackrock parallel port for every screen change and response.
"""

import os
import sys
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
    if _ttl_backend is None:
        try:
            from psychopy import parallel
            addr = int(os.environ.get('PARALLEL_PORT_ADDRESS', '0x0378'), 16)
            parallel.setPortAddress(addr)
            _ttl_backend = ('parallel', parallel)
            print("TTL: Using parallel port", file=sys.stderr)
        except Exception:
            _ttl_backend = False
            print("TTL WARNING: No backend. Triggers will NOT be sent.", file=sys.stderr)


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
    """12 shapes: exclude middle 4 (1.70_1.70, 1.70_3.30, 3.30_1.70, 3.30_3.30)."""
    all_shapes = get_shape_paths()
    exclude = {'Shape_1.70_1.70.png', 'Shape_1.70_3.30.png', 'Shape_3.30_1.70.png', 'Shape_3.30_3.30.png'}
    return [p for p in all_shapes if Path(p).name not in exclude]


def get_context_categories():
    """Return list of category folder names (exclude practice images at root)."""
    cats = []
    for d in CONTEXT_DIR.iterdir():
        if d.is_dir():
            cats.append(d.name)
    return sorted(cats)


def get_context_image(category, variant):
    """
    variant: 'original' -> *1 (01b or 01s), 'control' -> *2 (02s)
    Actual files: {cat}_01b.jpg, {cat}_01s.jpg, {cat}_02s.jpg
    """
    cat_dir = CONTEXT_DIR / category
    if variant == 'original':
        for pat in ['*_01b.jpg', '*_01s.jpg', '*1.jpg']:
            matches = list(cat_dir.glob(pat))
            if matches:
                return str(matches[0])
    elif variant == 'control':
        for pat in ['*_02s.jpg', '*2.jpg']:
            matches = list(cat_dir.glob(pat))
            if matches:
                return str(matches[0])
    return None


def get_shape_grid_path():
    return str(SHAPES_DIR / "ShapeGrid_4x4.png")


def get_practice_context_paths():
    return [
        str(CONTEXT_DIR / "practice1.png"),
        str(CONTEXT_DIR / "practice2.png")
    ]


# =========================
#  Button / Wait Helpers — Enter only, no buttons, ESC exits
# =========================
def wait_for_continue(win, text_stim, event_label, log_ttl=True, min_display_sec=0):
    """Wait for Enter. No buttons—Enter only. min_display_sec: minimum time before Enter is accepted."""
    hint = visual.TextStim(win, text="Press Enter to continue.", color='gray', height=0.03, pos=(0, -0.35), units='height')

    def draw():
        text_stim.draw()
        hint.draw()

    if log_ttl:
        _log_ttl_event(event_label)
    draw()
    win.flip()
    clock = core.Clock()
    clock.reset()

    while True:
        keys = event.getKeys(keyList=['escape', 'return'])
        if keys:
            if 'escape' in keys:
                core.quit()
            if 'return' in keys and clock.getTime() >= min_display_sec:
                if log_ttl:
                    _log_ttl_event(f"{event_label}_enter")
                return True
        draw()
        win.flip()
        core.wait(0.016)




# =========================
#  Phase 0: Participant Login — SRT-style fullscreen
# =========================
def get_participant_name(win):
    """Fullscreen text input like Social Recognition Task. Returns name or None if ESC."""
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
        keys = event.getKeys(keyList=key_list + ['escape'])
        if keys:
            if 'escape' in keys:
                core.quit()
            key = keys[0]
            if key == 'return':
                if input_id.strip():
                    return input_id.strip() or 'anonymous'
            elif key == 'backspace':
                input_id = input_id[:-1] if input_id else ""
            elif len(key) == 1:
                input_id += key
        redraw()
        core.wait(0.016)


# =========================
#  Phase 1 & 3: Drag Task
# =========================
def run_drag_phase(win, mouse, shape_paths, phase_name, phase_num, participant, anchors=None):
    """
    Sequential drag task. shape_paths: list of shape file paths.
    anchors: dict {path: (x,y)} of previously placed shapes to show.
    Returns list of dicts: shape_path, final_x, final_y, rt, ttl timestamps.
    """
    if anchors is None:
        anchors = {}
    results = []
    fieldnames = ['shape_path', 'final_x', 'final_y', 'rt', 'stimulus_onset_ttl', 'stimulus_offset_ttl',
                  'drag_start_ttl', 'drag_end_ttl', 'submit_ttl']
    csv_path = LOG_DIR / f"phase{phase_num}_{participant}.csv"
    if not is_test_participant(participant):
        f = open(csv_path, 'w', newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()
    else:
        f = None
        writer = None

    for idx, shape_path in enumerate(shape_paths):
        # 1 second: shape alone, not draggable (screen cleared per spec)
        img = visual.ImageStim(win, image=shape_path, units='height', size=(0.15, 0.15))
        img.setPos((0, 0))
        _log_ttl_event(f"{phase_name}_stimulus_onset", trial_info=f"trial={idx+1}")
        img.draw()
        win.flip()
        core.wait(1.0)
        _log_ttl_event(f"{phase_name}_stimulus_offset", trial_info=f"trial={idx+1}")

        # Now draggable
        shape_name = Path(shape_path).name
        stim = visual.ImageStim(win, image=shape_path, units='height', size=(0.15, 0.15))
        stim.setPos((0, 0))
        drag_clock = core.Clock()
        drag_clock.reset()
        drag_start_logged = [False]
        start_pos = [0, 0]

        def draw_drag():
            for p, (ax, ay) in anchors.items():
                a = visual.ImageStim(win, image=p, units='height', size=(0.1, 0.1))
                a.setPos((ax, ay))
                a.draw()
            stim.draw()
            hint = visual.TextStim(win, text="Press Enter to submit.", color='gray', height=0.028, pos=(0, -0.38), units='height')
            hint.draw()

        def full_draw():
            draw_drag()

        rt_start = time.time()
        submitted = False
        while not submitted:
            keys = event.getKeys(keyList=['escape', 'return'])
            if keys:
                if 'escape' in keys:
                    core.quit()
                if 'return' in keys:
                    submitted = True
                    break
            mpos = mouse.getPos()
            mbuttons = mouse.getPressed()
            if mbuttons[0]:
                if not drag_start_logged[0]:
                    drag_start_logged[0] = True
                    _log_ttl_event(f"{phase_name}_drag_start", trial_info=f"trial={idx+1}")
                stim.setPos(mpos)
            full_draw()
            win.flip()
            core.wait(0.016)

        rt = time.time() - rt_start
        fx, fy = stim.pos
        _log_ttl_event(f"{phase_name}_enter_submit", trial_info=f"trial={idx+1} shape={shape_name}")

        row = {
            'shape_path': shape_path,
            'final_x': f"{fx:.6f}",
            'final_y': f"{fy:.6f}",
            'rt': f"{rt:.4f}",
            'stimulus_onset_ttl': '',  # Could store from _last_ttl_timestamp
            'stimulus_offset_ttl': '',
            'drag_start_ttl': '',
            'drag_end_ttl': '',
            'submit_ttl': f"{_last_ttl_timestamp[0]:.9f}" if _last_ttl_timestamp[0] else ''
        }
        results.append(row)
        anchors[shape_path] = (float(fx), float(fy))

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


# =========================
#  Tutorial — Video with subtitles (red square, red circle, green circle)
# =========================
# Place tutorial video at STIMULI/tutorial_video.mp4. Video should show dragging in action;
# subtitles describe what's on screen (not instructions read aloud).
# If missing, plays animated fallback simulating the drag sequence.
TUTORIAL_VIDEO = STIMULI_DIR / "tutorial_video.mp4"


def _animate_shape_move(win, shape_stim, start_pos, end_pos, duration, subtitle, clock):
    """Animate shape from start_pos to end_pos over duration. Subtitle at bottom."""
    sub = visual.TextStim(win, text=subtitle, color='black', height=0.032, pos=(0, -0.42),
                          wrapWidth=1.3, units='height', alignText='center')
    t0 = clock.getTime()
    while clock.getTime() - t0 < duration:
        keys = event.getKeys(keyList=['escape'])
        if keys and 'escape' in keys:
            core.quit()
        t = (clock.getTime() - t0) / duration
        t = min(1.0, t)
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        shape_stim.setPos((x, y))
        shape_stim.draw()
        sub.draw()
        win.flip()
        core.wait(0.016)


def run_tutorial_phase1(win, mouse, participant):
    """Tutorial: video with subtitles, or animated fallback showing dragging. Shapes: red square, red circle, green circle."""
    used_fallback = True
    if TUTORIAL_VIDEO.exists():
        try:
            movie = visual.MovieStim(win, str(TUTORIAL_VIDEO), play=True)
            _log_ttl_event("tutorial_video_onset")
            while movie.status != visual.FINISHED:
                keys = event.getKeys(keyList=['escape'])
                if keys and 'escape' in keys:
                    core.quit()
                movie.draw()
                win.flip()
            _log_ttl_event("tutorial_video_offset")
            used_fallback = False
        except Exception as e:
            print(f"Video playback failed, using fallback: {e}", file=sys.stderr)

    if used_fallback:
        # Animated sequence showing dragging (subtitles describe what's on screen)
    clock = core.Clock()
    sq = visual.Rect(win, width=0.16, height=0.16, fillColor='red', lineColor=None)
    circ_red = visual.Circle(win, radius=0.08, fillColor='red', lineColor=None)
    circ_green = visual.Circle(win, radius=0.08, fillColor='green', lineColor=None)

    # Step 1: Three shapes overview
    _log_ttl_event("tutorial_fallback_onset", trial_info="step=1")
    sq.setPos((-0.3, 0))
    circ_red.setPos((0, 0))
    circ_green.setPos((0.3, 0))
    sub1 = visual.TextStim(win, text="Three shapes appear.", color='black', height=0.032, pos=(0, -0.42),
                          wrapWidth=1.3, units='height', alignText='center')
    sq.draw()
    circ_red.draw()
    circ_green.draw()
    sub1.draw()
    win.flip()
    core.wait(2.5)
    _log_ttl_event("tutorial_fallback_offset", trial_info="step=1")

    # Step 2: Red square appears, drags left
    _log_ttl_event("tutorial_fallback_onset", trial_info="step=2")
    clock.reset()
    _animate_shape_move(win, sq, (0, 0), (-0.35, 0), 1.5, "Red square appears. Dragging to the left.", clock)
    _log_ttl_event("tutorial_fallback_offset", trial_info="step=2")

    # Step 3: Red circle appears, drags left
    _log_ttl_event("tutorial_fallback_onset", trial_info="step=3")
    clock.reset()
    circ_red.setPos((0, 0))
    _animate_shape_move(win, circ_red, (0, 0), (-0.35, 0.08), 1.5, "Red circle appears. Dragging to the left.", clock)
    _log_ttl_event("tutorial_fallback_offset", trial_info="step=3")

    # Step 4: Green circle appears, drags right
    _log_ttl_event("tutorial_fallback_onset", trial_info="step=4")
    clock.reset()
    circ_green.setPos((0, 0))
    _animate_shape_move(win, circ_green, (0, 0), (0.35, 0), 1.5, "Green circle appears. Dragging to the right.", clock)
    _log_ttl_event("tutorial_fallback_offset", trial_info="step=4")

    # Step 5: Final layout + alternative grouping note
    _log_ttl_event("tutorial_fallback_onset", trial_info="step=5")
    sq.setPos((-0.35, 0))
    circ_red.setPos((-0.35, 0.08))
    circ_green.setPos((0.35, 0))
    sq.draw()
    circ_red.draw()
    circ_green.draw()
    sub_alt = visual.TextStim(win, text="There were alternative ways of grouping, but this is what we went with.",
                              color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
    sub_alt.draw()
    win.flip()
    core.wait(3.0)
    _log_ttl_event("tutorial_fallback_offset", trial_info="step=5")

    # Step 6: Press Enter subtitle
    _log_ttl_event("tutorial_fallback_onset", trial_info="step=6")
    sq.draw()
    circ_red.draw()
    circ_green.draw()
    sub_enter = visual.TextStim(win, text="Press Enter to submit each placement.",
                                color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
    sub_enter.draw()
    win.flip()
    core.wait(2.0)
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
def build_phase2_trials(participant):
    """
    Build 48 trials: 12 shapes × 4 variants.
    Variants: original, context_swapped, control_context, control_context_swapped.
    Same shape never consecutive.
    """
    shapes = get_phase2_shapes()
    categories = get_context_categories()
    if len(categories) < 2:
        raise RuntimeError("Need at least 2 context categories")
    random.seed(hash(participant) % (2**32) if participant else None)
    trials = []
    for shape_path in shapes:
        cat_a, cat_b = random.sample(categories, 2)
        ctx_a_orig = get_context_image(cat_a, 'original')
        ctx_b_orig = get_context_image(cat_b, 'original')
        ctx_a_ctrl = get_context_image(cat_a, 'control')
        ctx_b_ctrl = get_context_image(cat_b, 'control')
        if not all([ctx_a_orig, ctx_b_orig, ctx_a_ctrl, ctx_b_ctrl]):
            continue
        trials.append({'shape_path': shape_path, 'context_1': ctx_a_orig, 'context_2': ctx_b_orig,
                      'cat_a': cat_a, 'cat_b': cat_b, 'variant': 'original'})
        trials.append({'shape_path': shape_path, 'context_1': ctx_b_orig, 'context_2': ctx_a_orig,
                      'cat_a': cat_a, 'cat_b': cat_b, 'variant': 'context_swapped'})
        trials.append({'shape_path': shape_path, 'context_1': ctx_a_ctrl, 'context_2': ctx_b_ctrl,
                      'cat_a': cat_a, 'cat_b': cat_b, 'variant': 'control_context'})
        trials.append({'shape_path': shape_path, 'context_1': ctx_b_ctrl, 'context_2': ctx_a_ctrl,
                      'cat_a': cat_a, 'cat_b': cat_b, 'variant': 'control_context_swapped'})
    random.shuffle(trials)
    # Enforce no consecutive same shape
    for _ in range(100):
        bad = False
        for i in range(1, len(trials)):
            if Path(trials[i]['shape_path']).name == Path(trials[i-1]['shape_path']).name:
                bad = True
                j = random.randint(i+1, len(trials)-1) if i+1 < len(trials) else random.randint(0, i-1)
                trials[i], trials[j] = trials[j], trials[i]
                break
        if not bad:
            break
    return trials


def run_phase2_tutorial(win, mouse, participant):
    """Phase 2 tutorial: practice1, practice2, circle, CIRCUS | SPACE."""
    p1, p2 = get_practice_context_paths()
    circ = visual.Circle(win, radius=0.2, fillColor='blue', lineColor=None)
    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    blank = visual.Rect(win, width=3, height=3, fillColor='white', lineColor=None, pos=(0, 0), units='height')
    dot = visual.Circle(win, radius=0.02, fillColor='red', lineColor=None, pos=(0, 0))
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

    # Red dot + "PLANET" 2000ms
    _log_ttl_event("phase2_tutorial_reddot_onset")
    dot.draw()
    txt1 = visual.TextStim(win, text="You might say the circle is a 'PLANET'", color='black', height=0.04, pos=(0, -0.2))
    txt1.draw()
    win.flip()
    core.wait(2.0)
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
    blank.draw()
    win.flip()
    core.wait(1.0)

    # Red dot + "BALL" 2000ms
    dot.draw()
    txt2 = visual.TextStim(win, text="You might say the circle is a 'BALL'", color='black', height=0.04, pos=(0, -0.2))
    txt2.draw()
    win.flip()
    core.wait(2.0)

    # Question: CIRCUS | SPACE
    q = visual.TextStim(win, text="Which context fits the object better?", color='black', height=0.04, pos=(0, 0.1))
    btn_circus = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', pos=(-0.2, -0.2), units='height')
    btn_space = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', pos=(0.2, -0.2), units='height')
    txt_c = visual.TextStim(win, text="CIRCUS", color='black', height=0.03, pos=(-0.2, -0.2), units='height')
    txt_s = visual.TextStim(win, text="SPACE", color='black', height=0.03, pos=(0.2, -0.2), units='height')
    _log_ttl_event("phase2_tutorial_question_onset")
    q.draw()
    btn_circus.draw()
    btn_space.draw()
    txt_c.draw()
    txt_s.draw()
    win.flip()
    # Wait for SPACE click (example)
    while True:
        mpos = mouse.getPos()
        mbuttons = mouse.getPressed()
        if mbuttons[0] and 0.1 <= mpos[0] <= 0.3 and -0.23 <= mpos[1] <= -0.17:
            _log_ttl_event("phase2_tutorial_response", trial_info="SPACE")
            break
        keys = event.getKeys(keyList=['escape'])
        if keys and 'escape' in keys:
            return False
        q.draw()
        btn_circus.draw()
        btn_space.draw()
        txt_c.draw()
        txt_s.draw()
        win.flip()
        core.wait(0.02)
    blank.draw()
    win.flip()
    core.wait(3.0)

    # Ready screen
    ready = visual.TextStim(win, text="Ready to try this with some actual shapes and images?",
                            color='black', height=0.04, pos=(0, 0), wrapWidth=1.2, units='height')
    cont_btn = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', lineColor='black', pos=(0, -0.3), units='height')
    cont_txt = visual.TextStim(win, text="CONTINUE", color='black', height=0.03, pos=(0, -0.3), units='height')
    return wait_for_continue(win, ready, "phase2_ready")


def run_phase2_trials(win, mouse, trials, participant):
    """Run 48 Phase 2 trials with breaks every 12."""
    fieldnames = ['trial', 'shape_path', 'context_1_path', 'context_2_path', 'trial_variant', 'response',
                   'rt', 'fixation_onset_ttl', 'context1_onset_ttl', 'shape_onset_ttl', 'reddot_onset_ttl',
                   'context2_onset_ttl', 'shape2_onset_ttl', 'reddot2_onset_ttl', 'question_onset_ttl', 'response_ttl']
    csv_path = LOG_DIR / f"phase2_{participant}.csv"
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
    dot = visual.Circle(win, radius=0.02, fillColor='red', lineColor=None, pos=(0, 0))

    for t_idx, trial in enumerate(trials):
        if t_idx > 0 and t_idx % 12 == 0:
            break_text = visual.TextStim(win, text="Take a break! Press Enter when ready to move on.",
                                        color='black', height=0.04, pos=(0, 0), wrapWidth=1.2, units='height')
            _log_ttl_event("phase2_break_onset", trial_info=f"after_trial={t_idx}")
            wait_for_continue(win, break_text, "phase2_break")

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

        blank.draw()
        win.flip()
        core.wait(1.0)

        _log_ttl_event("phase2_reddot_onset", trial_info=f"trial={t_idx+1}")
        dot.draw()
        win.flip()
        core.wait(2.0)
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

        blank.draw()
        win.flip()
        core.wait(1.0)

        _log_ttl_event("phase2_reddot2_onset", trial_info=f"trial={t_idx+1}")
        dot.draw()
        win.flip()
        core.wait(2.0)
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
            keys = event.getKeys(keyList=['escape'])
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

        blank.draw()
        win.flip()
        core.wait(0.5)

    if f:
        f.close()


# =========================
#  Summary CSV
# =========================
def run_phase3_debrief(win, mouse, participant):
    """Two Yes/No questions at end of Phase 3. Returns list of dicts or None if ESC."""
    questions = [
        "Did you use the same grouping strategy as the first time you sorted these shapes?",
        "Did the images associated with each shape you saw influence your grouping the second time around?",
    ]
    fieldnames = ['question', 'question_text', 'answer', 'rt', 'onset_ttl', 'response_ttl']
    csv_path = LOG_DIR / f"debrief_{participant}.csv"
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
            keys = event.getKeys(keyList=['escape'])
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
    """Extract (row, col) from Shape_X_Y.png. Grid: 0.10, 1.70, 3.30, 4.90 -> rows/cols 0-3."""
    name = Path(shape_path).stem
    try:
        parts = name.replace('Shape_', '').split('_')
        if len(parts) >= 2:
            x, y = float(parts[0]), float(parts[1])
            row = {0.10: 0, 1.70: 1, 3.30: 2, 4.90: 3}.get(x, -1)
            col = {0.10: 0, 1.70: 1, 3.30: 2, 4.90: 3}.get(y, -1)
            return row, col, x, y
    except (ValueError, IndexError):
        pass
    return -1, -1, 0, 0


def write_summary(participant, experiment_start, experiment_end, phase1_results, phase3_results):
    """Write summary_{participant}.csv"""
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
    csv_path = LOG_DIR / f"summary_{participant}.csv"
    if is_test_participant(participant):
        return
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


# =========================
#  Main
# =========================
def main():
    global _ttl_file_ref, _ttl_writer_ref
    event.globalKeys.add(key='escape', func=lambda: core.quit(), modifiers=[])

    win = visual.Window(
        size=(1920, 1080),
        fullscr=True,
        color='white',
        units='height',
        allowGUI=False
    )
    mouse = event.Mouse(win=win)
    mouse.setVisible(True)

    participant = get_participant_name(win)
    participant = participant.strip() or 'anonymous'

    _probe_ttl()
    if not is_test_participant(participant):
        ttl_path = LOG_DIR / f"ttl_log_{participant}.csv"
        _ttl_file_ref[0] = open(ttl_path, 'w', newline='')
        _ttl_writer_ref[0] = csv.DictWriter(_ttl_file_ref[0], fieldnames=['timestamp', 'trigger_code', 'event_label', 'trial_info'])
        _ttl_writer_ref[0].writeheader()
        _ttl_file_ref[0].flush()

    experiment_start = time.time()

    # Welcome
    welcome = visual.TextStim(win, text="Welcome to our task! Let's get started. First, watch this example video of how we work on this task.",
                              color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    cont_btn = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', lineColor='black', pos=(0, -0.3), units='height')
    cont_txt = visual.TextStim(win, text="CONTINUE", color='black', height=0.03, pos=(0, -0.3), units='height')
    if not wait_for_continue(win, welcome, "welcome"):
        win.close()
        return

    # Tutorial Phase 1
    if not run_tutorial_phase1(win, mouse, participant):
        win.close()
        return

    # Phase 1 — instructions much longer after practice
    instr1 = visual.TextStim(win, text="Let's sort some shapes. First you will see all of them. Then you will place them one at a time and group them where you think they belong, as in the practice.\n\nPress Enter when you're ready.",
                             color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, instr1, "phase1_instructions", min_display_sec=10.0):
        win.close()
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

    instr2 = visual.TextStim(win, text="You will now see the shapes from before, one at a time. Group each to where you think it belongs on the screen. Press Enter to submit each placement.",
                             color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, instr2, "phase1_instruction2"):
        win.close()
        return

    shapes = get_shape_paths()
    random.shuffle(shapes)
    if Path(shapes[0]).name == "Shape_0.10_0.10.png":
        shapes.append(shapes.pop(0))
    phase1_results = run_drag_phase(win, mouse, shapes, "phase1", 1, participant)
    if phase1_results is None:
        win.close()
        return

    # Phase 2
    instr_p2 = visual.TextStim(win, text="Now, you will see the shapes again, in conjunction with different contexts. Try to think of what the shape might be in that context and say it out loud.\n\nHere's an example.",
                              color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, instr_p2, "phase2_instructions", min_display_sec=8.0):
        win.close()
        return

    if not run_phase2_tutorial(win, mouse, participant):
        win.close()
        return

    trials = build_phase2_trials(participant)
    run_phase2_trials(win, mouse, trials, participant)

    # Phase 3
    instr_p3 = visual.TextStim(win, text="Let's sort some shapes again, like we did in the VERY beginning. Feel free to use whatever grouping feels intuitive.",
                               color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, instr_p3, "phase3_instructions"):
        win.close()
        return

    shapes3 = get_shape_paths()
    random.shuffle(shapes3)
    while shapes3 == shapes:
        random.shuffle(shapes3)
    phase3_results = run_drag_phase(win, mouse, shapes3, "phase3", 3, participant)
    if phase3_results is None:
        win.close()
        return

    # Phase 3 debrief questions
    debrief_results = run_phase3_debrief(win, mouse, participant)
    if debrief_results is None:
        win.close()
        return

    experiment_end = time.time()
    write_summary(participant, experiment_start, experiment_end, phase1_results, phase3_results)

    if _ttl_file_ref[0]:
        _ttl_file_ref[0].close()
        _ttl_file_ref[0] = None

    thanks = visual.TextStim(win, text="Thank you! Task complete.", color='black', height=0.05, pos=(0, 0))
    thanks.draw()
    win.flip()
    core.wait(2.0)
    win.close()


if __name__ == '__main__':
    main()
