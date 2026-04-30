#!/usr/bin/env python3
"""
ContextShape Task — PsychoPy Implementation
Environment: Python (Anaconda); PsychoPy per requirements.txt (psychopy>=2025.2,<2027)
Fullscreen with DPI scaling. ESC during interactive screens only (not during grid, fixation, stimulus).
TTL via Blackrock parallel port or Cedrus pyxid2. Every screen change and response logged; see csv_documentation.md.
Task object `.bmp` files (excluding `ShapeGrid*`): near-white matte → transparency at load (`OBJECT_WHITE_BG_STRIP_THRESHOLD`).
Fixed-duration waits use module-level `*_SEC` constants (see `PHASE2_REDDOT_DURATION_SEC` and following); keep in sync with TASK_DESCRIPTION.md (timing section).
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

import numpy as np

# Paths relative to script location
SCRIPT_DIR = Path(__file__).resolve().parent
STIMULI_DIR = SCRIPT_DIR / "STIMULI"
SHAPES_DIR = STIMULI_DIR / "shapes"
CONTEXT_DIR = STIMULI_DIR / "contexts"
# Task uses 16 .bmp shapes (first 16 alphabetically in shapes/; matches ShapeGrid_4x4_bmp.png)
PHASE1_SHAPE_COUNT = 16
PHASE1_FIRST_BMP = "ball_slope.bmp"  # first in sorted 16; avoid always leading with this (see main shuffle)
# Raw `STIMULI/shapes/*.bmp` task objects (`ShapeGrid*` composites excluded): near-white matte → transparency at presentation.
OBJECT_WHITE_BG_STRIP_THRESHOLD = 247  # R, G, B all ≥ this level → alpha 0 after load
# PsychoPy `units='height'`: max extent for the longer raster axis (`_image_size_height_units`; aspect preserved).
#
# Phase 1/3 — task BMPs (isolate + placement + placement PNG export):
DRAG_SORT_SHAPE_MAX_EXTENT = 0.30  # draggable / committed center (doubled from 0.15)
ANCHOR_SORT_SHAPE_MAX_EXTENT = 0.20  # previously placed overlays only (doubled from 0.10)

# Phase 1/3 — composite grid PNG (fullscreen / fixation); long edge capped to fraction of monitor height:
PHASE13_GRID_PREVIEW_MAX_EXTENT = 1.0  # was 0.8; doubling 1.6 would clip — use maximal viewport fill
GRID_INSET_MAX_EXTENT = 0.40  # miniature bottom-right reference (doubled from 0.20)

# Phase 2 — contexts: large centered square (same size + cover crop per trial); trial BMP epochs doubled:
PHASE2_CONTEXT_MAX_EXTENT = 1.0  # square side length in height units (width = height × PHASE2_CONTEXT_FRAME_ASPECT_W_OVER_H)
# All Phase 2 context images share this box (cover crop, center); width = height × ratio (1.0 = square).
PHASE2_CONTEXT_FRAME_ASPECT_W_OVER_H = 1.0  # square frame, centered; all contexts same size (cover crop)
PHASE2_TRIAL_OBJECT_MAX_EXTENT = 0.40  # doubled from 0.2
LOG_DIR = SCRIPT_DIR.parent / "LOG_FILES"
PHASE2_TRIAL_ORDER_CSV = SCRIPT_DIR / "phase2_trial_order.csv"
# Required columns in phase2_trial_order.csv (order in file may vary).
PHASE2_CSV_REQUIRED = (
    "shape_path",
    "context1_image",
    "context2_image",
    "context1",
    "context2",
    "variant",
)
# --- Fixed stimulus durations (seconds). TTL aligns with screen boundaries tied to `_log_ttl_event`; see TASK_DESCRIPTION.md (timing section). ---
PHASE2_REDDOT_DURATION_SEC = 2.0  # Phase 2 cue-dot epoch (black `Circle` in `run_phase2_trials` / tutorial)
PHASE_GRID_PREVIEW_SEC = 5.0
PHASE_FIXATION_CROSS_SEC = 1.0
SHAPE_STATIC_PREVIEW_SEC = 1.0  # Phase 1/3: isolate shape before placement
PHASE2_SEGMENT_SEC = 1.0       # Phase 2: context/shape durations (gap before cue dot is 0; see blanks removed below)
PHASE2_FIXATION_PRE_TRIAL_SEC = 0.5
PHASE2_TRIAL_ITI_SEC = 0.5
# Scripted training demos only (+ s on each timed screen vs prior defaults). Phase 2 main trials unchanged.
TRAINING_DEMO_SCREEN_EXTRA_SEC = 1.5
# Animated fallback when `tutorial_video.mp4` is missing (timed steps below)
TUTORIAL_FB_OVERVIEW_SEC = 2.5 + TRAINING_DEMO_SCREEN_EXTRA_SEC
TUTORIAL_FB_CLICK_CENTER_SEC = 1.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
TUTORIAL_FB_CLICK_TARGET_SEC = 2.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
TUTORIAL_FB_STEP5A_SEC = 3.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
TUTORIAL_FB_STEP5B_SEC = 4.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
TUTORIAL_FB_STEP6_SEC = 7.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
# Phase 1 fallback demo: cursor animation (sums with click pulses must fit inside *_CLICK_* totals below)
TUTORIAL_FB_CURSOR_REST_POS = (-0.52, -0.38)
TUTORIAL_FB_CURSOR_TO_SHAPE_SEC = 0.72
TUTORIAL_FB_CURSOR_DRAG_TO_TARGET_SEC = 0.82
TUTORIAL_FB_CURSOR_CLICK_FEEDBACK_SEC = 0.14
# Phase 2 demo (`run_phase2_tutorial`); use *_TRIAL_* / `PHASE2_SEGMENT_SEC` for real Phase 2 trials
PHASE2_TUTORIAL_SEGMENT_SEC = PHASE2_SEGMENT_SEC + TRAINING_DEMO_SCREEN_EXTRA_SEC
PHASE2_TUTORIAL_FIXATION_SEC = PHASE2_FIXATION_PRE_TRIAL_SEC + TRAINING_DEMO_SCREEN_EXTRA_SEC
PHASE2_TUTORIAL_REDDOT_SEC = PHASE2_REDDOT_DURATION_SEC + TRAINING_DEMO_SCREEN_EXTRA_SEC
PHASE2_TUTORIAL_QUESTION_PREVIEW_SEC = 1.5 + TRAINING_DEMO_SCREEN_EXTRA_SEC
PHASE2_TUTORIAL_HIGHLIGHT_FEEDBACK_SEC = 1.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
PHASE2_TUTORIAL_POST_BLANK_SEC = 3.0 + TRAINING_DEMO_SCREEN_EXTRA_SEC
THANKS_SCREEN_SEC = 2.0
PHASE2_INSTR5_MIN_SEC = 5.0  # min display before Enter on `phase2_tutorial_intro` ("Watch this demo…")

# Ensure LOG_FILES exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Suppress iohub if needed
os.environ.setdefault('PSYCHOPY_IOHUB', '0')

from psychopy import visual, core, event
try:
    from psychopy.hardware import keyboard as hw_keyboard
    # Disable hardware keyboard on Mac—known to cause freezes/Enter not registering (PsychoPy discourse #36146, #35710)
    _has_keyboard = sys.platform != 'darwin'
except ImportError:
    hw_keyboard = None
    _has_keyboard = False


def _psycho_win_check_timing():
    """Return whether Window.__init__ should run initial frame-interval calibration (`checkTiming`).
    On macOS, PsychoPy's calibration calls flip() → pyglet can crash with NSTrackingArea /
    ObjCInstance has no attribute 'type' during event dispatch—default off unless overridden.
    Set PSYCHOPY_CHECK_TIMING=1 to enable, 0 to force disable on any OS."""
    v = (os.environ.get('PSYCHOPY_CHECK_TIMING') or '').strip().lower()
    if v in ('1', 'true', 'yes'):
        return True
    if v in ('0', 'false', 'no'):
        return False
    return sys.platform != 'darwin'


def _ensure_psychopy_window_key_focus(win):
    """Bring the experiment window forward so keyboard events are delivered to it.

    With PSYCHOPY_DUMMY_WINDOW=1 a small Window is created first; on macOS that
    window can keep keyboard focus while the fullscreen task runs, so
    event.getKeys() on `win` stays empty until the user clicks the task display."""
    try:
        h = getattr(win, 'winHandle', None)
        if h is None:
            return
        activate = getattr(h, 'activate', None)
        if callable(activate):
            activate()
            return
        switch_to = getattr(h, 'switch_to', None)
        if callable(switch_to):
            switch_to()
    except Exception:
        pass


def _event_key_token(raw):
    """Normalize psychopy.event.getKeys() entries to a key name string."""
    if raw is None:
        return ''
    name = getattr(raw, 'name', None)
    if name is not None:
        return str(name).strip()
    if isinstance(raw, str):
        return raw.strip()
    return str(raw).strip()


def _wait(secs):
    """Wait secs seconds. On macOS, core.wait() can trigger pyglet Cocoa bug
    (ObjCInstance has no attribute type) during event dispatch; use time.sleep instead."""
    if sys.platform == 'darwin':
        time.sleep(secs)
    else:
        core.wait(secs)


def _install_pyglet_cocoa_nsevent_unwrap_patch():
    """macOS: AppKit sometimes returns a single-element NSArray from nextEventMatchingMask
    where pyglet expects NSEvent (__NSSingleObjectArrayI → no .type()). Unwrap before handling.
    Disable with PSYCHOPY_COCOA_EVENT_PATCH=0."""
    if sys.platform != 'darwin':
        return
    if os.environ.get('PSYCHOPY_COCOA_EVENT_PATCH', '1').lower() in ('0', 'false', 'no'):
        return
    try:
        from pyglet.window.cocoa import CocoaWindow
        from pyglet.libs.darwin import cocoapy
    except Exception:
        return
    if getattr(CocoaWindow.dispatch_events, '_nsevent_unwrap_installed', False):
        return
    NSAutoreleasePool = cocoapy.ObjCClass('NSAutoreleasePool')
    NSApplication = cocoapy.ObjCClass('NSApplication')

    def _unwrap_next_event(ev):
        if not ev:
            return None
        cur = ev
        for _ in range(16):
            try:
                cur.type()
                return cur
            except AttributeError:
                pass
            oai = getattr(cur, 'objectAtIndex_', None)
            cnt_f = getattr(cur, 'count', None)
            if not callable(oai) or not callable(cnt_f):
                return None
            try:
                n = int(cnt_f())
            except Exception:
                return None
            if n <= 0:
                return None
            try:
                cur = oai(0)
            except Exception:
                return None
        return None

    def dispatch_events(self):
        self._allow_dispatch_event = True
        self.dispatch_pending_events()
        event = True
        pool = NSAutoreleasePool.new()
        NSApp = NSApplication.sharedApplication()
        while event and self._nswindow and self._context:
            raw = NSApp.nextEventMatchingMask_untilDate_inMode_dequeue_(
                cocoapy.NSAnyEventMask, None, cocoapy.NSEventTrackingRunLoopMode, True)
            event = _unwrap_next_event(raw)
            if event:
                event_type = event.type()
                NSApp.sendEvent_(event)
                if event_type == cocoapy.NSKeyDown and not event.isARepeat():
                    NSApp.sendAction_to_from_(cocoapy.get_selector('pygletKeyDown:'), None, event)
                elif event_type == cocoapy.NSKeyUp:
                    NSApp.sendAction_to_from_(cocoapy.get_selector('pygletKeyUp:'), None, event)
                elif event_type == cocoapy.NSFlagsChanged:
                    NSApp.sendAction_to_from_(cocoapy.get_selector('pygletFlagsChanged:'), None, event)
                NSApp.updateWindows()
        pool.drain()
        self._allow_dispatch_event = False

    dispatch_events._nsevent_unwrap_installed = True
    CocoaWindow.dispatch_events = dispatch_events


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
            _wait(0.01)
            backend.setData(0)
    except Exception:
        pass


def _log_ttl_event(event_label, trigger_code=None, trial_info=None):
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


def _phase2_main_trial_info(trial, t_idx):
    """Key=value string for Phase 2 trial TTL lines (sync with behavioral CSV paths)."""
    return (
        f"trial={t_idx + 1} "
        f"shape={Path(trial['shape_path']).name} "
        f"ctx1={Path(trial['context_1']).name} "
        f"ctx2={Path(trial['context_2']).name} "
        f"variant={trial['variant']}"
    )


def _fmt_unix_csv(ts):
    """Unix timestamp string for numeric cells; empty if missing."""
    return f"{ts:.9f}" if ts is not None else ''


def is_test_participant(name):
    return name and 'test' in name.lower()


def get_shape_paths():
    """Return paths to the 16 task shapes: .bmp in shapes/ (excludes grid composites), first PHASE1_SHAPE_COUNT by sorted name."""
    paths = [str(f) for f in SHAPES_DIR.glob("*.bmp") if not f.name.startswith("ShapeGrid")]
    paths = sorted(paths, key=lambda p: Path(p).name.lower())
    if len(paths) > PHASE1_SHAPE_COUNT:
        paths = paths[:PHASE1_SHAPE_COUNT]
    return paths


def get_phase2_shapes():
    """Unused: Phase 2 stimuli come only from ``shape_path`` rows in ``phase2_trial_order.csv``."""
    all_shapes = get_shape_paths()
    exclude_idx = {5, 6, 9, 10}
    return [p for i, p in enumerate(all_shapes) if i not in exclude_idx]


def get_context_categories():
    """Base category for each {name}.png + {name}1.png pair in contexts/ (e.g. sky, bathroom)."""
    by_name = {f.name: True for f in CONTEXT_DIR.glob("*.png")}
    cats = set()
    for f in CONTEXT_DIR.glob("*.png"):
        s = f.stem
        if s.endswith("1") and len(s) > 1 and f"{s[:-1]}.png" in by_name:
            cats.add(s[:-1])
        elif f"{s}1.png" in by_name:
            pass  # will record base from the *1 file
        else:
            cats.add(s)
    return sorted(cats)


def get_context_image(category, variant):
    """
    Get context image path. Each category has two variants: {category}1.png and {category}.png
    (original → '1' file, control → base name without digit).
    """
    c = category.strip()
    if variant == "original":
        p = CONTEXT_DIR / f"{c}1.png"
        if p.exists():
            return str(p)
    else:
        p = CONTEXT_DIR / f"{c}.png"
        if p.exists():
            return str(p)
    p = CONTEXT_DIR / f"{c}1.png"
    if p.exists():
        return str(p)
    p = CONTEXT_DIR / f"{c}.png"
    if p.exists():
        return str(p)
    return None


def get_shape_grid_path():
    """Return composite grid for Phase 1/3 preview and inset (16 bmps in 4×4)."""
    return str(SHAPES_DIR / "ShapeGrid_4x4_bmp.png")


def get_practice_context_paths():
    """Tutorial: SPACE (practice1) + CIRCUS (practice2). Files `practice1.png`, `practice2.png`
    in `STIMULI/` or `STIMULI/contexts/` (first match wins)."""
    out = []
    for fn in ("practice1.png", "practice2.png"):
        candidates = (STIMULI_DIR / fn, CONTEXT_DIR / fn)
        for p in candidates:
            if p.is_file():
                out.append(str(p))
                break
        else:
            tried = " or ".join(str(p) for p in candidates)
            raise FileNotFoundError(
                f"Phase 2 tutorial needs {fn} (space/circus practice). Tried: {tried}"
            )
    return out


# =========================
#  Button / Wait Helpers — Enter only, no buttons, ESC exits
# =========================
def wait_for_continue(win, text_stim, event_label, log_ttl=True, min_display_sec=0, extra_drawables=None, onset_trial_info=None):
    """Wait for Enter. No buttons—Enter only. min_display_sec: minimum time before Enter is accepted.
    extra_drawables: optional list of stimuli to draw. onset_trial_info: optional trial_info for onset TTL.
    Uses hardware.Keyboard on Mac when available for snappier key response."""
    event.clearEvents()
    hint = visual.TextStim(win, text="Enter to continue.", color='gray', height=0.03, pos=(0, -0.35), units='height')
    extras = extra_drawables or []
    kb = hw_keyboard.Keyboard() if _has_keyboard and hw_keyboard else None

    def draw():
        text_stim.draw()
        for s in extras:
            s.draw()
        hint.draw()

    if log_ttl:
        _log_ttl_event(f"{event_label}_onset", trial_info=onset_trial_info)
    draw()
    win.flip()
    event.clearEvents()
    _wait(0.05)
    if kb:
        kb.clearEvents()
    event.clearEvents()
    clock = core.Clock()
    clock.reset()
    return_pressed = False
    enter_names = {'return', 'enter', 'num_enter', 'kp_enter', 'num_return'}

    def accept_and_exit():
        if log_ttl:
            _log_ttl_event(f"{event_label}_enter")
            _log_ttl_event(f"{event_label}_offset")
        event.clearEvents()
        if kb:
            kb.clearEvents()
        _wait(0.03)  # minimal debounce
        return True

    def check_keys():
        if kb:
            try:
                key_objs = kb.getKeys(['escape', 'return', 'enter'], waitRelease=False)
                return [k.name for k in key_objs]
            except Exception:
                pass
        try:
            return event.getKeys(keyList=['escape', 'return', 'enter', 'num_enter', 'kp_enter'], timeStamped=False)
        except (AttributeError, RuntimeError):
            return []

    while True:
        keys = check_keys()
        if keys:
            if 'escape' in keys:
                _log_ttl_event("escape_pressed", trial_info=f"screen={event_label}")
                core.quit()
            if any(k in enter_names for k in keys):
                if clock.getTime() >= min_display_sec:
                    return accept_and_exit()
                return_pressed = True
        if return_pressed and clock.getTime() >= min_display_sec:
            return accept_and_exit()
        if return_pressed:
            remaining = min_display_sec - clock.getTime()
            if remaining > 0:
                _wait(min(0.03, remaining))
            continue
        draw()
        win.flip()
        _wait(0.005)  # 5ms polling for snappier response




# =========================
#  Phase 0: Participant Login — SRT-style fullscreen
# =========================
def get_participant_name(win):
    """Fullscreen text input like Social Recognition Task. Returns name or None if ESC."""
    _log_ttl_event("participant_name_onset")
    input_id = ""
    # Characters we accept (same as historical key_list singles: a-z A-Z 0-9).
    _allowed_chars = frozenset(
        chr(i) for i in list(range(97, 123)) + list(range(65, 91)) + list(range(48, 58))
    )
    _return_names = frozenset(('return', 'enter', 'num_enter', 'kp_enter', 'num_return'))
    id_prompt = visual.TextStim(
        win,
        text="Enter your name",
        color='black',
        height=0.045,
        wrapWidth=1.4,
        pos=(0, 0.25),
        units='height',
    )
    input_display = visual.TextStim(win, text="", color='black', height=0.06, pos=(0, 0), units='height')

    def redraw():
        id_prompt.draw()
        input_display.text = f"{input_id}_"
        input_display.draw()
        win.flip()

    redraw()
    _ensure_psychopy_window_key_focus(win)
    event.clearEvents()

    while True:
        # Do NOT use event.getKeys(keyList=...): macOS/PsychoPy often emits 'enter' / 'num_enter' vs 'return';
        # a restrictive keyList drops ALL keys so nothing registers. Poll unrestricted, filter here.
        try:
            keys = event.getKeys(timeStamped=False)
        except (AttributeError, RuntimeError):
            keys = []
        for raw in keys:
            key = _event_key_token(raw)
            if not key:
                continue
            low = key.lower()
            if low == 'escape':
                _log_ttl_event("escape_pressed", trial_info="participant_name")
                core.quit()
            if low in _return_names:
                if input_id.strip():
                    _log_ttl_event("participant_name_offset")
                    return input_id.strip() or 'anonymous'
                continue
            if low == 'backspace':
                input_id = input_id[:-1] if input_id else ""
                continue
            if len(key) == 1 and key in _allowed_chars:
                if len(input_id) < 127:
                    input_id += key
        redraw()
        _wait(0.016)


# ----------------------------
# Task object BMP preprocessing (opaque white/matte backdrop → transparency)
# ----------------------------
_task_object_strip_pil_master_cache: dict[str, object] = {}  # resolved path → shared RGBA Pillow image (read-only)


def _shape_bmfilename_strips_white_matte(fname: str) -> bool:
    n = fname.lower()
    return n.endswith('.bmp') and not n.startswith('shapegrid')


def _pil_master_task_shape_white_stripped(path_str: str):
    """Load `STIMULI/shapes/*.bmp` with near-white matte removed; callers should `.copy()` if mutating/shared."""
    from PIL import Image

    canon = os.path.abspath(os.path.expanduser(str(path_str)))
    hit = _task_object_strip_pil_master_cache.get(canon)
    if hit is not None:
        return hit
    pil = Image.open(canon).convert('RGBA')
    a = np.array(pil, dtype=np.uint8)
    thr = OBJECT_WHITE_BG_STRIP_THRESHOLD
    matte = np.all(a[..., :3] >= thr, axis=-1)
    a[matte, 3] = 0
    # Omit mode: Pillow 13 deprecates mode= here; (H,W,4) uint8 implies RGBA.
    out = Image.fromarray(np.ascontiguousarray(a))
    _task_object_strip_pil_master_cache[canon] = out
    return out


def _stimulus_image_arg_for_possible_task_shape(path_str: str):
    """Filepath, or Pillow RGBA copy with matte stripped for Psychopy `ImageStim` / PIL composites."""
    if not _shape_bmfilename_strips_white_matte(Path(path_str).name):
        return path_str
    return _pil_master_task_shape_white_stripped(path_str).copy()


# =========================
#  Phase 1 & 3: Click-to-Place Task
# =========================
def _native_image_aspect_ratio(path_str):
    """Native width / height (~1 if unreadable)."""
    try:
        from PIL import Image
        with Image.open(Path(path_str).expanduser()) as im:
            iw, ih = im.size
        if ih <= 0:
            return 1.0
        return float(iw) / float(ih)
    except Exception:
        return 1.0


def _image_size_height_units(path_str, max_extent):
    """
    `(width, height)` in PsychoPy `units='height'` while preserving BMP/PNG aspect ratio.
    `max_extent` limits the larger side — same role as earlier square `(s, s)`.
    """
    ar = _native_image_aspect_ratio(path_str)
    if ar >= 1.0:
        return (float(max_extent), float(max_extent) / ar)
    return (float(max_extent) * ar, float(max_extent))


# Phase 2 context display: fixed on-screen rectangle; images are center-cropped (cover) to match.
_phase2_context_cover_cache: dict[tuple[str, int, int], object] = {}


def _phase2_context_frame_size_height_units():
    """Fixed (width, height) in `units='height'` for every Phase 2 context image."""
    h = float(PHASE2_CONTEXT_MAX_EXTENT)
    w = h * float(PHASE2_CONTEXT_FRAME_ASPECT_W_OVER_H)
    return (w, h)


def _phase2_context_image_cropped_pil(win, path_str):
    """Scale + center-crop to the Phase 2 frame in pixels (object-fit: cover); cached."""
    from PIL import Image

    w_u, h_u = _phase2_context_frame_size_height_units()
    win_h = max(1, int(win.size[1]))
    out_w = max(2, int(round(w_u * win_h)))
    out_h = max(2, int(round(h_u * win_h)))
    canon = os.path.abspath(os.path.expanduser(str(path_str)))
    key = (canon, out_w, out_h)
    hit = _phase2_context_cover_cache.get(key)
    if hit is not None:
        return hit
    try:
        im = Image.open(canon)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im = im.convert('RGBA')
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[3])
            im = bg
        else:
            im = im.convert('RGB')
        iw, ih = im.size
        if iw <= 0 or ih <= 0:
            raise ValueError('empty image')
        scale = max(out_w / float(iw), out_h / float(ih))
        nw = max(1, int(round(iw * scale)))
        nh = max(1, int(round(ih * scale)))
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - out_w) // 2
        top = (nh - out_h) // 2
        out = im.crop((left, top, left + out_w, top + out_h))
    except Exception:
        out = Image.new('RGB', (out_w, out_h), color=(245, 245, 245))
    _phase2_context_cover_cache[key] = out
    return out


def _pixel_thumbnail_size(iw, ih, max_px):
    """Preserve aspect with longer side capped at max_px (for PIL placement PNG export)."""
    if ih <= 0:
        return (max_px, max_px)
    ar = float(iw) / float(ih)
    if iw >= ih:
        return (max_px, max(1, int(round(max_px / ar))))
    return (max(1, int(round(max_px * ar))), max_px)


def _save_placement_image(results, output_path, win_size=(1920, 1080), max_extent_height_units=None):
    """
    Save placement visualization as PNG. results: list of {shape_path, final_x, final_y}.

    Rasterizes each BMP with the same on-screen footprint as PsychoPy `ImageStim` with
    `units='height'` and `size=_image_size_height_units(path, max_extent)`, so edges/boundaries match
    the task (`DRAG_SORT_SHAPE_MAX_EXTENT` by default).

    Coordinate mapping matches PsychoPy `units='height'`: `event.Mouse._pix2windowUnits` uses pixels
    from window centre divided by `win.size[1]`, so **x** is in ``[-(w/h)/2, +(w/h)/2]`` and **y** in
    ``[-0.5, +0.5]`` (not ±w/h nor ±1). Older code mapped a doubled range and shrunk content to the
    middle 50 % of the PNG (white borders). `win_size` must match the run (`win.size`).
    """
    try:
        from PIL import Image
    except ImportError:
        return
    max_extent_height_units = max_extent_height_units if max_extent_height_units is not None else DRAG_SORT_SHAPE_MAX_EXTENT
    w, h = int(win_size[0]), int(win_size[1])
    # Height units: centred pix offset / win.size[1] → x_px = w/2 + x*h, y_pil = h/2 - y*h (PIL y down).
    img = Image.new('RGB', (w, h), color='white')
    # Longest side of each scaled BMP spans max_extent × window height in pixels — matches ImageStim in height units
    longest_side_px = max(1, int(round(max_extent_height_units * h)))
    for r in results:
        try:
            x = float(r.get('final_x', 0))
            y = float(r.get('final_y', 0))
        except (TypeError, ValueError):
            continue
        x_px = int(round(w / 2.0 + x * h))
        y_px = int(round(h / 2.0 - y * h))
        try:
            shape_img = _pil_master_task_shape_white_stripped(r['shape_path'])
            iw, ih = shape_img.size
            tw, th = _pixel_thumbnail_size(iw, ih, longest_side_px)
            shape_img = shape_img.resize((tw, th), Image.Resampling.LANCZOS)
            paste_x = x_px - tw // 2
            paste_y = y_px - th // 2
            img.paste(shape_img, (paste_x, paste_y), shape_img)
        except Exception:
            pass
    img.save(output_path)


def _make_grid_inset_stim(win, grid_path):
    """Miniature full grid at bottom-right; preserves composite PNG aspect (not forced square)."""
    aspect_win = float(win.size[0]) / float(win.size[1])
    w_units, h_units = _image_size_height_units(grid_path, GRID_INSET_MAX_EXTENT)
    margin = 0.03
    gx = aspect_win - margin - w_units / 2
    gy = -1.0 + margin + h_units / 2
    return visual.ImageStim(win, image=grid_path, units='height', size=(w_units, h_units), pos=(gx, gy))


def run_drag_phase(win, mouse, shape_paths, phase_name, phase_num, participant, anchors=None, timestamp_str=None, inset_grid_path=None):
    """
    Sequential click-to-place task. shape_paths: list of shape file paths.
    anchors: dict {path: (x,y)} of previously placed shapes to show.
    inset_grid_path: if set, show a small full-grid reference in the bottom-right for the
    whole sorting block (1 s isolated preview per shape plus click-to-place until submit).
    Returns list of dicts: shape_path, final_x, final_y, rt, ttl timestamps.
    """
    if anchors is None:
        anchors = {}
    grid_inset = _make_grid_inset_stim(win, inset_grid_path) if inset_grid_path else None
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
        shape_name = Path(shape_path).name
        sh_sz = _image_size_height_units(shape_path, DRAG_SORT_SHAPE_MAX_EXTENT)
        # 1 s: centered isolate preview; miniature full grid stays bottom-right throughout sorting
        img = visual.ImageStim(win, image=_stimulus_image_arg_for_possible_task_shape(shape_path), units='height', size=sh_sz)
        img.setPos((0, 0))
        _log_ttl_event(f"{phase_name}_stimulus_onset", trial_info=f"trial={idx+1} shape={shape_name}")
        img.draw()
        if grid_inset is not None:
            grid_inset.draw()
        win.flip()
        _wait(SHAPE_STATIC_PREVIEW_SEC)
        _log_ttl_event(f"{phase_name}_stimulus_offset", trial_info=f"trial={idx+1} shape={shape_name}")
        del img  # free texture before creating more stims

        # Now clickable: click anywhere to place
        stim = visual.ImageStim(win, image=_stimulus_image_arg_for_possible_task_shape(shape_path), units='height', size=sh_sz)
        stim.setPos((0, 0))

        # Pre-create anchor stims and hint once (avoids per-frame allocation lag)
        anchor_stims = [
            (
                visual.ImageStim(win, image=_stimulus_image_arg_for_possible_task_shape(p), units='height', size=_image_size_height_units(p, ANCHOR_SORT_SHAPE_MAX_EXTENT)),
                ax,
                ay,
            )
            for p, (ax, ay) in anchors.items()
        ]
        hint = visual.TextStim(win, text="Click to place — Enter submits.", color='gray', height=0.028, pos=(0, -0.38), units='height')

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
                    _log_ttl_event("escape_pressed", trial_info=f"{phase_name}_click_place")
                    core.quit()
                if 'return' in keys and click_times:
                    # Require at least one click before Enter is accepted
                    last_click_time = click_times[-1]
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
            if grid_inset is not None:
                grid_inset.draw()
            hint.draw()
            win.flip()

        fx, fy = stim.pos
        last_click_ttl = click_times[-1] if click_times else None
        all_click_ttl_str = ';'.join(f"{t:.9f}" for t in click_times) if click_times else ''
        row = {
            'shape_path': shape_path,
            'final_x': f"{fx:.6f}",
            'final_y': f"{fy:.6f}",
            'rt': f"{rt:.4f}",
            'stimulus_onset_ttl': '',
            'stimulus_offset_ttl': '',
            'click_ttl': f"{last_click_ttl:.9f}" if last_click_ttl else '',
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
                win_size = tuple(win.size) if hasattr(win, 'size') else (1920, 1080)
                png_path = LOG_DIR / f"phase{phase_num}_placements_{participant}_{ts}.png"
                _save_placement_image(results, png_path, win_size)
                _log_ttl_event(f"phase{phase_num}_placements_saved", trial_info=f"{png_path.name} trial={idx+1}")
            except Exception as e:
                print(f"Warning: Could not save placement image: {e}", file=sys.stderr)

    if f:
        f.close()
    if grid_inset is not None:
        del grid_inset

    return results


# =========================
#  Tutorial — Video with subtitles (red square, red circle, green circle; demo sorts by COLOR)
# =========================
# Place tutorial video at STIMULI/tutorial_video.mp4. Video should show clicking to place;
# subtitles describe what's on screen (not instructions read aloud).
# If missing, plays animated fallback simulating click-to-place with a color-based grouping demo.
TUTORIAL_VIDEO = STIMULI_DIR / "tutorial_video.mp4"


def _tutorial_smoothstep(u):
    u = max(0.0, min(1.0, float(u)))
    return u * u * (3.0 - 2.0 * u)


def _make_tutorial_cursor_arrow(win):
    """Mouse-style arrow; `pos` is the tip (click point) in height units."""
    verts = [
        (0.0, 0.0),
        (0.065, 0.022),
        (0.032, 0.022),
        (0.032, 0.068),
        (0.014, 0.068),
        (0.014, 0.022),
    ]
    return visual.ShapeStim(
        win,
        vertices=verts,
        units='height',
        fillColor='#1a1a1a',
        lineColor='#f0f0f0',
        lineWidth=1.5,
        closeShape=True,
        interpolate=False,
    )


def _show_click_place(win, shape_stim, start_pos, end_pos, subtitle, anchors=None, ttl_label=None):
    """Animated click-to-place: cursor moves in, clicks, drags shape to target, clicks again.
    Total dwell times match TUTORIAL_FB_CLICK_CENTER_SEC / TUTORIAL_FB_CLICK_TARGET_SEC so TTL spacing is unchanged.
    anchors: optional list of (stim, (x,y)) for previously placed shapes to keep visible.
    ttl_label: optional prefix for TTL — logs center_onset/offset, target_onset/offset."""
    sub = visual.TextStim(win, text=subtitle, color='black', height=0.032, pos=(0, -0.42),
                          wrapWidth=1.3, units='height', alignText='center')
    anchor_list = anchors or []
    cursor = _make_tutorial_cursor_arrow(win)
    click_ring = visual.Circle(
        win,
        radius=0.02,
        fillColor=None,
        lineColor='steelblue',
        lineWidth=3,
        pos=(0, 0),
        units='height',
        interpolate=False,
    )
    rest = TUTORIAL_FB_CURSOR_REST_POS
    move_to_shape = float(TUTORIAL_FB_CURSOR_TO_SHAPE_SEC)
    drag_sec = float(TUTORIAL_FB_CURSOR_DRAG_TO_TARGET_SEC)
    click_sec = float(TUTORIAL_FB_CURSOR_CLICK_FEEDBACK_SEC)
    hold_center = max(0.0, float(TUTORIAL_FB_CLICK_CENTER_SEC) - move_to_shape - click_sec)
    hold_target = max(0.0, float(TUTORIAL_FB_CLICK_TARGET_SEC) - drag_sec - click_sec)
    frame_dt = max(1.0 / 120.0, float(getattr(win, 'monitorFramePeriod', None) or (1.0 / 60.0)))

    def draw_scene(shape_xy, cursor_xy, ring_radius=None):
        for a_stim, a_pos in anchor_list:
            a_stim.setPos(a_pos)
            a_stim.draw()
        shape_stim.setPos(shape_xy)
        shape_stim.draw()
        if ring_radius is not None and ring_radius > 0:
            click_ring.setPos(shape_xy)
            click_ring.setRadius(ring_radius)
            click_ring.draw()
        if cursor_xy is not None:
            cursor.setPos(cursor_xy)
            cursor.draw()
        sub.draw()

    def animate_scalar(duration_sec, fn):
        """fn(u) draws one frame; u goes 0→1 with smoothstep."""
        if duration_sec <= 0:
            fn(1.0)
            win.flip()
            return
        t0 = time.perf_counter()
        while True:
            elapsed = time.perf_counter() - t0
            u = min(1.0, elapsed / duration_sec)
            fn(_tutorial_smoothstep(u))
            win.flip()
            if u >= 1.0:
                break
            _wait(frame_dt)

    def click_pulse_at(shape_xy):
        n = max(3, int(round(click_sec / frame_dt)))
        for i in range(n + 1):
            p = i / float(n)
            r = 0.014 + 0.034 * p
            draw_scene(shape_xy, shape_xy, ring_radius=r)
            win.flip()
            if i < n:
                _wait(click_sec / n)

    if ttl_label:
        _log_ttl_event(f"{ttl_label}_center_onset")

    # Cursor → shape at center; shape stays at start_pos
    def phase_approach(u):
        cx = rest[0] + (start_pos[0] - rest[0]) * u
        cy = rest[1] + (start_pos[1] - rest[1]) * u
        draw_scene(start_pos, (cx, cy))

    animate_scalar(move_to_shape, phase_approach)
    click_pulse_at(start_pos)

    draw_scene(start_pos, start_pos)
    win.flip()
    _wait(hold_center)

    if ttl_label:
        _log_ttl_event(f"{ttl_label}_center_offset")
        _log_ttl_event(f"{ttl_label}_target_onset")

    # Drag shape to target; cursor follows tip at shape center
    def phase_drag(u):
        sx = start_pos[0] + (end_pos[0] - start_pos[0]) * u
        sy = start_pos[1] + (end_pos[1] - start_pos[1]) * u
        draw_scene((sx, sy), (sx, sy))

    animate_scalar(drag_sec, phase_drag)
    click_pulse_at(end_pos)

    draw_scene(end_pos, end_pos)
    win.flip()
    _wait(hold_target)

    if ttl_label:
        _log_ttl_event(f"{ttl_label}_target_offset")

    del cursor, click_ring


def run_tutorial_phase1(win, mouse, participant):
    """Tutorial: video with subtitles, or animated fallback showing click-to-place.
    Fallback demo uses red square, red circle, green circle and groups by COLOR (reds together; green apart).
    Fallback animates a cursor that moves to each object, shows a click, and drags it to the target."""
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
                    _log_ttl_event("escape_pressed", trial_info="tutorial_video")
                    core.quit()
                movie.draw()
                win.flip()
            _log_ttl_event("tutorial_video_offset")
            used_fallback = False
        except Exception as e:
            print(f"Video playback failed, using fallback: {e}", file=sys.stderr)

    if used_fallback:
        # Click-to-place sequence with animated cursor (move in, click, drag to target, click)
        sq = visual.Rect(win, width=0.16, height=0.16, fillColor='red', lineColor=None)
        circ_red = visual.Circle(win, radius=0.08, fillColor='red', lineColor=None)
        circ_green = visual.Circle(win, radius=0.08, fillColor='green', lineColor=None)

        # Positions: both red shapes clustered on left; green circle on right (sort by color)
        sq_pos = (-0.38, 0.08)
        circ_red_pos = (-0.12, 0.08)
        circ_green_pos = (0.42, 0.08)

        # Step 1: Three shapes overview
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=1")
        sq.setPos((-0.35, 0))
        circ_red.setPos((0, 0))
        circ_green.setPos((0.35, 0))
        sub1 = visual.TextStim(win, text="The first part of the task is about sorting objects. Watch how we sort these objects!", color='black', height=0.032, pos=(0, -0.42),
                              wrapWidth=1.3, units='height', alignText='center')
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        sub1.draw()
        win.flip()
        _wait(TUTORIAL_FB_OVERVIEW_SEC)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=1")

        # Step 2: Red square appears at center, clicks to place on left (no anchors yet)
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=2")
        _show_click_place(win, sq, (0, 0), sq_pos, "First, let's click to place the red square on the left — Then, we hit Enter.",
                          ttl_label="tutorial_fallback_step2")
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=2")

        # Step 3: Red circle joins red cluster beside square (square stays visible as anchor)
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=3")
        circ_red.setPos((0, 0))
        _show_click_place(win, circ_red, (0, 0), circ_red_pos, "Now, let's group the red circle with the red square on the left.",
                          anchors=[(sq, sq_pos)], ttl_label="tutorial_fallback_step3")
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=3")

        # Step 4: Green circle to right, separate color group (previous anchors visible)
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=4")
        circ_green.setPos((0, 0))
        _show_click_place(win, circ_green, (0, 0), circ_green_pos, "Let's place the green circle to the right (in a different group).",
                          anchors=[(sq, sq_pos), (circ_red, circ_red_pos)], ttl_label="tutorial_fallback_step4")
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=4")

        # Step 5a: Color groups — reds together vs green apart
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=5a")
        sq.setPos(sq_pos)
        circ_red.setPos(circ_red_pos)
        circ_green.setPos(circ_green_pos)
        group_circle_redshapes = visual.Circle(win, radius=0.22, fillColor=None, lineColor='black', lineWidth=2,
                                               pos=(-0.25, 0.08), units='height')
        group_circle_green = visual.Circle(win, radius=0.14, fillColor=None, lineColor='black', lineWidth=2,
                                             pos=circ_green_pos, units='height')
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        group_circle_redshapes.draw()
        group_circle_green.draw()
        sub_5a = visual.TextStim(win, text="See how we ended up sorting by color? We could have sorted by shape too — there are no wrong answers here!",
                                color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
        sub_5a.draw()
        win.flip()
        _wait(TUTORIAL_FB_STEP5A_SEC)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=5a")

        # Step 5b: Distance denotes group
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=5b")
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        sub_5b = visual.TextStim(win, text="We created groups, not a spectrum — nearby objects share a group.",
                                color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
        sub_5b.draw()
        win.flip()
        _wait(TUTORIAL_FB_STEP5B_SEC)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=5b")

        # Step 6: Press Enter subtitle
        _log_ttl_event("tutorial_fallback_onset", trial_info="step=6")
        sq.draw()
        circ_red.draw()
        circ_green.draw()
        # sub_5c = visual.TextStim(win, text="A group does not have to pack tight — a large spread is OK.",
        #                         color='black', height=0.028, pos=(0, -0.35), wrapWidth=1.3, units='height', alignText='center')
        sub_enter = visual.TextStim(win, text="Click to place — Enter submits each placement.",
                                   color='black', height=0.032, pos=(0, -0.42), wrapWidth=1.3, units='height', alignText='center')
        # sub_5c.draw()
        sub_enter.draw()
        win.flip()
        _wait(TUTORIAL_FB_STEP6_SEC)
        _log_ttl_event("tutorial_fallback_offset", trial_info="step=6")

    # Transition
    trans = visual.TextStim(win, text="Your turn to group some objects! — Remember the same rules.", color='black', height=0.04, pos=(0, 0),
                           wrapWidth=1.2, units='height')
    return wait_for_continue(win, trans, "tutorial_transition")


# =========================
#  Phase 2: Context Task
# =========================
def _fix_stimuli_path_case(p: Path) -> Path:
    """Map CSV folder names to on-disk: Shapes→shapes, Contexts/Context_Images→contexts (case-sensitive FS)."""
    s = p.as_posix()
    s = s.replace("/Shapes/", "/shapes/").replace("/Contexts/", "/contexts/").replace("/Context_Images/", "/contexts/")
    return Path(s)


def _resolve_stimulus_path(path_str):
    """
    Resolve path to an existing file. Relative paths are under STIMULI_DIR.
    Absolute paths: if missing, try normalizing Shapes/Contexts/Context_Images, then basename in shapes/ or contexts/.
    """
    p = path_str.strip().strip('"')
    if not p:
        raise ValueError("Empty stimulus path in phase2_trial_order.csv")
    path = Path(os.path.expanduser(p))
    to_try: list[Path] = []
    if not path.is_absolute():
        to_try.append((STIMULI_DIR / path).resolve())
    else:
        to_try.append(path.resolve())
        to_try.append(_fix_stimuli_path_case(path).resolve())

    for cand in to_try:
        if cand.is_file():
            return str(cand)

    name = path.name
    for sub in ("shapes", "contexts"):
        alt = (STIMULI_DIR / sub / name).resolve()
        if alt.is_file():
            return str(alt)

    if not path.is_absolute():
        fallback = (STIMULI_DIR / path).resolve()
        return str(fallback)
    return str(path.resolve())


def load_phase2_trials():
    """
    Load Phase 2 trial order from phase2_trial_order.csv. Same fixed order for all participants.
    Required columns: PHASE2_CSV_REQUIRED. Optional: trial_number, shape, primary_context,
    secondary_context (or legacy strong_context / neutral_context for design labels).
    Paths: absolute or relative to STIMULI/; Shapes/Contexts spelling is normalized automatically.
    Run length equals the number of non-empty trial rows (shipped repo template: 64 trials).
    """
    if not PHASE2_TRIAL_ORDER_CSV.exists():
        raise FileNotFoundError(f"Phase 2 trial order file not found: {PHASE2_TRIAL_ORDER_CSV}")
    trials = []
    # utf-8-sig strips Excel BOM if present
    with open(PHASE2_TRIAL_ORDER_CSV, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        missing = [c for c in PHASE2_CSV_REQUIRED if c not in cols]
        if missing:
            raise ValueError(
                f"{PHASE2_TRIAL_ORDER_CSV.name} missing required column(s): {missing}. Found: {cols}"
            )
        for row in reader:
            if not row.get("shape_path", "").strip():
                continue
            shape_path = _resolve_stimulus_path(row["shape_path"])
            ctx1_path = _resolve_stimulus_path(row["context1_image"])
            ctx2_path = _resolve_stimulus_path(row["context2_image"])
            primary = (row.get("primary_context") or row.get("strong_context") or "").strip()
            secondary = (row.get("secondary_context") or row.get("neutral_context") or "").strip()
            trials.append(
                {
                    "shape_path": shape_path,
                    "context_1": ctx1_path,
                    "context_2": ctx2_path,
                    "cat_a": row["context1"].strip(),
                    "cat_b": row["context2"].strip(),
                    "variant": (row.get("variant") or "").strip(),
                    "primary_context": primary,
                    "secondary_context": secondary,
                }
            )
    if not trials:
        raise ValueError(f"No trial rows in {PHASE2_TRIAL_ORDER_CSV}")
    return trials


def run_phase2_tutorial(win, mouse, participant):
    """Phase 2 tutorial: intro, then two practice contexts (see get_practice_context_paths), circle, demo question."""
    # Single intro screen (max 2 sentences) — one Enter before demo
    intro = visual.TextStim(win, text="Watch this demo before you start the task!",
                            color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, intro, "phase2_tutorial_intro", min_display_sec=PHASE2_INSTR5_MIN_SEC):
        return False

    p1, p2 = get_practice_context_paths()
    circ = visual.Circle(win, radius=0.1, fillColor='blue', lineColor=None)
    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    blank = visual.Rect(win, width=3, height=3, fillColor='white', lineColor=None, pos=(0, 0), units='height')
    dot = visual.Circle(win, radius=0.003, fillColor='black', lineColor=None, pos=(0, 0))
    ctx_sz = _phase2_context_frame_size_height_units()
    img1 = visual.ImageStim(win, image=_phase2_context_image_cropped_pil(win, p1), units='height', size=ctx_sz)
    img2 = visual.ImageStim(win, image=_phase2_context_image_cropped_pil(win, p2), units='height', size=ctx_sz)

    # Fixation (longer than main trials — training demo pacing)
    _log_ttl_event("phase2_tutorial_fixation_onset")
    fix.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_FIXATION_SEC)
    _log_ttl_event("phase2_tutorial_fixation_offset")

    p1_bn, p2_bn = Path(p1).name, Path(p2).name
    _log_ttl_event("phase2_tutorial_context1_onset", trial_info=f"context={p1_bn}")
    img1.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_SEGMENT_SEC)
    _log_ttl_event("phase2_tutorial_context1_offset", trial_info=f"context={p1_bn}")

    _log_ttl_event("phase2_tutorial_shape_onset", trial_info="demo=blue_circle")
    circ.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_SEGMENT_SEC)
    _log_ttl_event("phase2_tutorial_shape_offset", trial_info="demo=blue_circle")

    _log_ttl_event("phase2_tutorial_reddot_onset", trial_info="cue=circle_label_1")
    dot.draw()
    txt1 = visual.TextStim(win, text="You might say the circle is a 'PLANET'", color='black', height=0.04, pos=(0, -0.2))
    txt1.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_REDDOT_SEC)
    _log_ttl_event("phase2_tutorial_reddot_offset", trial_info="cue=circle_label_1")

    _log_ttl_event("phase2_tutorial_context2_onset", trial_info=f"context={p2_bn}")
    img2.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_SEGMENT_SEC)
    _log_ttl_event("phase2_tutorial_context2_offset", trial_info=f"context={p2_bn}")

    _log_ttl_event("phase2_tutorial_shape2_onset", trial_info="demo=blue_circle")
    circ.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_SEGMENT_SEC)
    _log_ttl_event("phase2_tutorial_shape2_offset", trial_info="demo=blue_circle")

    _log_ttl_event("phase2_tutorial_reddot2_onset", trial_info="cue=circle_label_2")
    dot.draw()
    txt2 = visual.TextStim(win, text="You might say the circle is a 'BALL'", color='black', height=0.04, pos=(0, -0.2))
    txt2.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_REDDOT_SEC)
    _log_ttl_event("phase2_tutorial_reddot2_offset", trial_info="cue=circle_label_2")

    # Question: SPACE | CIRCUS (left = first practice context, right = second) — demo only
    q = visual.TextStim(win, text="Which context fits best? Use the left/right keys to choose.", color='black', height=0.04, pos=(0, 0.1))
    btn_a = visual.Rect(win, width=0.26, height=0.06, fillColor='lightblue', pos=(-0.2, -0.2), units='height')
    btn_b = visual.Rect(win, width=0.26, height=0.06, fillColor='lightblue', pos=(0.2, -0.2), units='height')
    txt_a = visual.TextStim(win, text="SPACE", color='black', height=0.03, pos=(-0.2, -0.2), units='height')
    txt_b = visual.TextStim(win, text="CIRCUS", color='black', height=0.03, pos=(0.2, -0.2), units='height')
    _log_ttl_event("phase2_tutorial_question_onset")
    q.draw()
    btn_a.draw()
    btn_b.draw()
    txt_a.draw()
    txt_b.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_QUESTION_PREVIEW_SEC)
    _log_ttl_event("phase2_tutorial_question_preview_offset")
    # Highlight right button (second context) + subtitle, matching old “second image” demo
    _log_ttl_event("phase2_tutorial_demo_select_onset")
    btn_b_pressed = visual.Rect(win, width=0.26, height=0.06, fillColor='steelblue', lineColor='black', pos=(0.2, -0.2), units='height')
    sub_select = visual.TextStim(win, text="You might say 'CIRCUS' (right key) is the better context", color='black', height=0.028, pos=(0, -0.38), units='height')
    q.draw()
    btn_a.draw()
    btn_b_pressed.draw()
    txt_a.draw()
    txt_b.draw()
    sub_select.draw()
    win.flip()
    _log_ttl_event("phase2_tutorial_response", trial_info="CIRCUS")
    _wait(PHASE2_TUTORIAL_HIGHLIGHT_FEEDBACK_SEC)
    _log_ttl_event("phase2_tutorial_demo_select_offset")
    _log_ttl_event("phase2_tutorial_question_offset")
    _log_ttl_event("phase2_tutorial_post_blank_onset")
    blank.draw()
    win.flip()
    _wait(PHASE2_TUTORIAL_POST_BLANK_SEC)
    _log_ttl_event("phase2_tutorial_post_blank_offset")

    # Ready screen
    ready = visual.TextStim(win, text="Ready for recorded trials?",
                            color='black', height=0.04, pos=(0, 0), wrapWidth=1.2, units='height')
    cont_btn = visual.Rect(win, width=0.2, height=0.06, fillColor='lightblue', lineColor='black', pos=(0, -0.3), units='height')
    cont_txt = visual.TextStim(win, text="CONTINUE", color='black', height=0.03, pos=(0, -0.3), units='height')
    return wait_for_continue(win, ready, "phase2_ready")


def run_phase2_trials(win, mouse, trials, participant, timestamp_str=None):
    """Run Phase 2 trials from phase2_trial_order.csv with breaks every 16."""
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
    dot = visual.Circle(win, radius=0.006, fillColor='black', lineColor=None, pos=(0, 0))

    total_trials = len(trials)
    for t_idx, trial in enumerate(trials):
        if t_idx > 0 and t_idx % 16 == 0:
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
            wait_for_continue(win, break_text, "phase2_break", extra_drawables=[bar_bg, bar_fill, pct_text],
                              onset_trial_info=f"after_trial={t_idx} total_trials={total_trials}")

        # Fixation 500ms
        ti_line = _phase2_main_trial_info(trial, t_idx)
        p2_ts = {}

        _log_ttl_event("phase2_fixation_onset", trial_info=ti_line)
        p2_ts['fixation_onset_ttl'] = _last_ttl_timestamp[0]
        fix.draw()
        win.flip()
        _wait(PHASE2_FIXATION_PRE_TRIAL_SEC)
        _log_ttl_event("phase2_fixation_offset", trial_info=ti_line)

        ctx_sz = _phase2_context_frame_size_height_units()
        ctx1 = visual.ImageStim(
            win,
            image=_phase2_context_image_cropped_pil(win, trial['context_1']),
            units='height',
            size=ctx_sz,
        )
        ctx2 = visual.ImageStim(
            win,
            image=_phase2_context_image_cropped_pil(win, trial['context_2']),
            units='height',
            size=ctx_sz,
        )
        shape_img = visual.ImageStim(
            win,
            image=_stimulus_image_arg_for_possible_task_shape(trial['shape_path']),
            units='height',
            size=_image_size_height_units(trial['shape_path'], PHASE2_TRIAL_OBJECT_MAX_EXTENT),
        )
        cat_a = trial['cat_a'].upper()
        cat_b = trial['cat_b'].upper()

        _log_ttl_event("phase2_context1_onset", trial_info=ti_line)
        p2_ts['context1_onset_ttl'] = _last_ttl_timestamp[0]
        ctx1.draw()
        win.flip()
        _wait(PHASE2_SEGMENT_SEC)
        _log_ttl_event("phase2_context1_offset", trial_info=ti_line)

        _log_ttl_event("phase2_shape_onset", trial_info=ti_line)
        p2_ts['shape_onset_ttl'] = _last_ttl_timestamp[0]
        shape_img.draw()
        win.flip()
        _wait(PHASE2_SEGMENT_SEC)
        _log_ttl_event("phase2_shape_offset", trial_info=ti_line)

        _log_ttl_event("phase2_reddot_onset", trial_info=ti_line)
        p2_ts['reddot_onset_ttl'] = _last_ttl_timestamp[0]
        dot.draw()
        win.flip()
        _wait(PHASE2_REDDOT_DURATION_SEC)
        _log_ttl_event("phase2_reddot_offset", trial_info=ti_line)

        _log_ttl_event("phase2_context2_onset", trial_info=ti_line)
        p2_ts['context2_onset_ttl'] = _last_ttl_timestamp[0]
        ctx2.draw()
        win.flip()
        _wait(PHASE2_SEGMENT_SEC)
        _log_ttl_event("phase2_context2_offset", trial_info=ti_line)

        _log_ttl_event("phase2_shape2_onset", trial_info=ti_line)
        p2_ts['shape2_onset_ttl'] = _last_ttl_timestamp[0]
        shape_img.draw()
        win.flip()
        _wait(PHASE2_SEGMENT_SEC)
        _log_ttl_event("phase2_shape2_offset", trial_info=ti_line)

        _log_ttl_event("phase2_reddot2_onset", trial_info=ti_line)
        p2_ts['reddot2_onset_ttl'] = _last_ttl_timestamp[0]
        dot.draw()
        win.flip()
        _wait(PHASE2_REDDOT_DURATION_SEC)
        _log_ttl_event("phase2_reddot2_offset", trial_info=ti_line)

        # Question (left/right arrow = context1 / context2 labels shown left/right)
        q = visual.TextStim(win, text="Which context fits best? Use the left/right keys to choose.", color='black', height=0.04, pos=(0, 0.1))
        btn_a = visual.Rect(win, width=0.26, height=0.06, fillColor='lightblue', pos=(-0.2, -0.2), units='height')
        btn_b = visual.Rect(win, width=0.26, height=0.06, fillColor='lightblue', pos=(0.2, -0.2), units='height')
        txt_a = visual.TextStim(win, text=cat_a, color='black', height=0.03, pos=(-0.2, -0.2), units='height')
        txt_b = visual.TextStim(win, text=cat_b, color='black', height=0.03, pos=(0.2, -0.2), units='height')
        # key_hint = visual.TextStim(
        #     win,
        #     text="← or → arrow",
        #     color='gray',
        #     height=0.025,
        #     pos=(0, -0.34),
        #     units='height',
        # )
        q_info = f"{ti_line} cat_a={cat_a} cat_b={cat_b}"
        _log_ttl_event("phase2_question_onset", trial_info=q_info)
        p2_ts['question_onset_ttl'] = _last_ttl_timestamp[0]
        try:
            event.clearEvents()
        except Exception:
            pass
        rt_clock = core.Clock()
        response = None
        first_question_frame = True
        while response is None:
            try:
                keys = event.getKeys(timeStamped=False)
            except (AttributeError, RuntimeError):
                keys = []
            for raw in keys:
                k = str(raw).lower()
                if k == 'escape':
                    _log_ttl_event("escape_pressed", trial_info="phase2_question")
                    core.quit()
                if k == 'left':
                    response = cat_a
                    break
                if k == 'right':
                    response = cat_b
                    break
            if response is not None:
                break
            q.draw()
            btn_a.draw()
            btn_b.draw()
            txt_a.draw()
            txt_b.draw()
            #key_hint.draw()
            win.flip()
            if first_question_frame:
                rt_clock.reset()
                first_question_frame = False
            _wait(0.02)
        rt = rt_clock.getTime()
        _log_ttl_event("phase2_response", trial_info=f"{ti_line} response={response}")
        response_ts = _last_ttl_timestamp[0]
        _log_ttl_event("phase2_question_offset", trial_info=ti_line)

        row = {
            'trial': t_idx + 1,
            'shape_path': trial['shape_path'],
            'context_1_path': trial['context_1'],
            'context_2_path': trial['context_2'],
            'trial_variant': trial['variant'],
            'response': response,
            'rt': f"{rt:.4f}",
            'fixation_onset_ttl': _fmt_unix_csv(p2_ts.get('fixation_onset_ttl')),
            'context1_onset_ttl': _fmt_unix_csv(p2_ts.get('context1_onset_ttl')),
            'shape_onset_ttl': _fmt_unix_csv(p2_ts.get('shape_onset_ttl')),
            'reddot_onset_ttl': _fmt_unix_csv(p2_ts.get('reddot_onset_ttl')),
            'context2_onset_ttl': _fmt_unix_csv(p2_ts.get('context2_onset_ttl')),
            'shape2_onset_ttl': _fmt_unix_csv(p2_ts.get('shape2_onset_ttl')),
            'reddot2_onset_ttl': _fmt_unix_csv(p2_ts.get('reddot2_onset_ttl')),
            'question_onset_ttl': _fmt_unix_csv(p2_ts.get('question_onset_ttl')),
            'response_ttl': f"{response_ts:.9f}" if response_ts else ''
        }
        if writer:
            writer.writerow(row)
            f.flush()
            try:
                os.fsync(f.fileno())
            except (AttributeError, OSError):
                pass

        _log_ttl_event("phase2_trial_iti_onset", trial_info=ti_line)
        blank.draw()
        win.flip()
        _wait(PHASE2_TRIAL_ITI_SEC)
        _log_ttl_event("phase2_trial_iti_offset", trial_info=ti_line)

        del ctx1, ctx2, shape_img
        if (t_idx + 1) % 16 == 0:
            gc.collect()

    if f:
        f.close()


# =========================
#  Summary CSV
# =========================
def run_phase3_debrief(win, mouse, participant, timestamp_str=None):
    """Three Yes/No questions at end of Phase 3. Left arrow = Yes, right arrow = No (not mouse).
    Returns list of dicts or None if ESC."""
    _ = mouse  # keyboard-only debrief; keep signature aligned with other run_* entry points
    questions = [
        "Did you group the objects differently the second time around?",
        "Did the contexts you saw change your grouping the second time?",
        "Did you see the objects differently the second time grouping them than you did when you first saw them?",
    ]
    fieldnames = ['question', 'question_text', 'answer', 'response_key', 'rt', 'onset_ttl', 'response_ttl']
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
        q = visual.TextStim(win, text=qtext, color='black', height=0.04, pos=(0, 0.2), wrapWidth=1.5, units='height',
                           anchorVert='top', alignText='center')
        btn_yes = visual.Rect(win, width=0.18, height=0.06, fillColor='lightgreen', lineColor='black', pos=(-0.22, -0.25), units='height')
        btn_no = visual.Rect(win, width=0.18, height=0.06, fillColor='lightcoral', lineColor='black', pos=(0.22, -0.25), units='height')
        txt_yes = visual.TextStim(win, text="Yes", color='black', height=0.03, pos=(-0.22, -0.25), units='height')
        txt_no = visual.TextStim(win, text="No", color='black', height=0.03, pos=(0.22, -0.25), units='height')
        hint = visual.TextStim(
            win,
            text="USE THE ARROW KEYS TO ANSWER",
            color='gray',
            height=0.028,
            pos=(0, -0.4),
            wrapWidth=1.4,
            units='height',
        )

        _log_ttl_event("phase3_debrief_onset", trial_info=f"question={i+1}")
        onset_ttl = _last_ttl_timestamp[0]
        rt_clock = core.Clock()
        answer = None
        response_key = None
        try:
            event.clearEvents()
        except Exception:
            pass
        first_debrief_frame = True
        while answer is None:
            try:
                keys = event.getKeys(timeStamped=False)
            except (AttributeError, RuntimeError):
                keys = []
            for raw in keys:
                k = str(raw).lower()
                if k == 'escape':
                    _log_ttl_event("escape_pressed", trial_info="phase3_debrief")
                    if f:
                        f.close()
                    return None
                if k == 'left':
                    answer = "Yes"
                    response_key = "left"
                    break
                if k == 'right':
                    answer = "No"
                    response_key = "right"
                    break
            if answer is not None:
                break
            q.draw()
            btn_yes.draw()
            btn_no.draw()
            txt_yes.draw()
            txt_no.draw()
            hint.draw()
            win.flip()
            if first_debrief_frame:
                rt_clock.reset()
                first_debrief_frame = False
            _wait(0.016)

        rt = rt_clock.getTime()
        _log_ttl_event(
            "phase3_debrief_response",
            trial_info=f"question={i+1} answer={answer} key={response_key}",
        )
        response_ttl = _last_ttl_timestamp[0]
        _log_ttl_event("phase3_debrief_offset", trial_info=f"question={i+1}")

        row = {
            'question': i + 1,
            'question_text': qtext,
            'answer': answer,
            'response_key': response_key or '',
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
    """Map shape file to 4×4 (row, col) by order in get_shape_paths() (same as ShapeGrid_4x4_bmp).
    Grid centers: row/col 0->0.10, 1->1.70, 2->3.30, 3->4.90 (latent for analysis)."""
    row_to_g = {0: 0.10, 1: 1.70, 2: 3.30, 3: 4.90}
    target = Path(shape_path).name
    for i, p in enumerate(get_shape_paths()):
        if Path(p).name == target:
            row, col = divmod(i, 4)
            if 0 <= row <= 3 and 0 <= col <= 3:
                return row, col, row_to_g[row], row_to_g[col]
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
    _install_pyglet_cocoa_nsevent_unwrap_patch()
    gc.collect()
    # Do NOT use event.globalKeys for escape (like Social Recognition Task).
    # globalKeys can cause random quits from key repeat or during transitions.
    # Escape is checked explicitly in each input loop instead.

    # Dummy window (helps stability/OOM on some systems, e.g. Social Recognition Task). Disable: PSYCHOPY_DUMMY_WINDOW=0
    use_dummy = os.environ.get('PSYCHOPY_DUMMY_WINDOW', '1').lower() not in ('0', 'false', 'no')
    _chk = _psycho_win_check_timing()
    dummy_win = None
    if use_dummy:
        try:
            dummy_win = visual.Window(
                size=(100, 100), pos=(0, 0), color='white', allowGUI=False, checkTiming=_chk
            )
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
        allowGUI=False,
        checkTiming=_chk,
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

    _shape_set = get_shape_paths()
    if len(_shape_set) < PHASE1_SHAPE_COUNT:
        print(
            f"ERROR: need at least {PHASE1_SHAPE_COUNT} .bmp files in {SHAPES_DIR} (excl. grid); found {len(_shape_set)}.",
            file=sys.stderr,
        )
        try:
            if _ttl_file_ref[0]:
                _ttl_file_ref[0].close()
                _ttl_file_ref[0] = None
        except Exception:
            pass
        win.close()
        _close_dummy()
        return

    experiment_start = time.time()
    _log_ttl_event("experiment_start", trial_info=f"participant={participant}")

    # Welcome
    welcome = visual.TextStim(win, text="Welcome to your task! — Hit Enter to watch the tutorial video.",
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
        ("Ask the experimenter if you have any questions!", "phase1_questions", 0),
        #("You will now sort some objects.", "phase1_instr1", 0),
        # ("Place one at a time (same as demo).", "phase1_instr2", 0),
        # ("Group by proximity—not along a spectrum.", "phase1_instr3", 0),
    ]
    for text, label, min_sec in p1_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label, min_display_sec=min_sec):
            win.close()
            _close_dummy()
            return

    # Before grid: 16 shapes, no need to memorize
    p1_before_grid = [
        ("You will now see all 16 objects you will be sorting at the same time — for reference only; just watch & don't memorize.", "phase1_before_grid", 0), 
    ]
    for text, label, _ in p1_before_grid:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label):
            win.close()
            _close_dummy()
            return

    # Grid 5 sec — large preview + same miniature bottom-right inset as later trials
    grid_path = get_shape_grid_path()
    grid_img = visual.ImageStim(
        win, image=grid_path, units='height', size=_image_size_height_units(grid_path, PHASE13_GRID_PREVIEW_MAX_EXTENT)
    )
    grid_inset_ref = _make_grid_inset_stim(win, grid_path)
    _log_ttl_event("phase1_grid_onset")
    grid_img.draw()
    grid_inset_ref.draw()
    win.flip()
    _wait(PHASE_GRID_PREVIEW_SEC)
    _log_ttl_event("phase1_grid_offset")
    del grid_inset_ref

    # Fixation 1 sec — keep miniature grid in bottom-right
    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    grid_inset_ref = _make_grid_inset_stim(win, grid_path)
    _log_ttl_event("phase1_fixation_onset")
    fix.draw()
    grid_inset_ref.draw()
    win.flip()
    _wait(PHASE_FIXATION_CROSS_SEC)
    _log_ttl_event("phase1_fixation_offset")
    del grid_inset_ref

    p1_post_fixation = [
        ("Now, group these objects like in the demo.", "phase1_instr1", True),
        (
            "Use as many groups as you want, and group objects however feels intuitive.",
            "phase1_instr2",
            False,
        ),
        (
            "Click to place each object — Enter locks. You can't change previous answers after submitting. Hit Enter to start!",
            "phase1_instr3",
            True,
        ),
    ]
    for text, label, with_mini_grid in p1_post_fixation:
        stim = visual.TextStim(
            win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height'
        )
        if with_mini_grid:
            grid_inset_ref = _make_grid_inset_stim(win, grid_path)
            ok = wait_for_continue(win, stim, label, extra_drawables=[grid_inset_ref])
            del grid_inset_ref
        else:
            ok = wait_for_continue(win, stim, label)
        if not ok:
            win.close()
            _close_dummy()
            return

    shapes = get_shape_paths()
    random.shuffle(shapes)
    if Path(shapes[0]).name == PHASE1_FIRST_BMP:
        shapes.append(shapes.pop(0))
    phase1_results = run_drag_phase(win, mouse, shapes, "phase1", 1, participant, timestamp_str=timestamp_str, inset_grid_path=grid_path)
    if phase1_results is None:
        win.close()
        _close_dummy()
        return
    _log_ttl_event("phase1_complete")
    gc.collect()

    # Phase 2 — split instructions (max 2 sentences per screen), explicit explanation
    p2_screens = [
        ("Ask the experimenter if you have any questions!", "phase2_questions", 0),
        ("For the next part of the task, we will show you a demo first. For this part, you will see each object paired with two contexts.", "phase2_instr1", 0),
        ("You will see: a context → object → dot.", "phase2_instr2", 0),
        ("When you see the dot, say what the object might be in that context aloud. Then, use the left/right keys to choose which context fits best.", "phase2_instr3", 0),
        ("The experimenter will record your responses, but don't panic. Just do your best and feel free to re-use answers.", "phase2_instr4", 0),
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

    ask_screen = visual.TextStim(win, text="Ask the experimenter if you have any questions — Enter to start.",
                                 color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
    if not wait_for_continue(win, ask_screen, "phase2_before_trials"):
        win.close()
        _close_dummy()
        return

    trials = load_phase2_trials()
    print(
        f"Phase 2: {len(trials)} trials from {PHASE2_TRIAL_ORDER_CSV.name}",
        file=sys.stderr,
    )
    run_phase2_trials(win, mouse, trials, participant, timestamp_str=timestamp_str)
    del trials
    _log_ttl_event("phase2_complete")
    gc.collect()

    # Phase 3 — split instructions (max 2 sentences per screen), similar structure to Phase 1
    p3_screens = [
        ("Ask the experimenter if you have any questions!", "phase3_questions", 0),
        ("Now you will sort the objects again — like you did right in the beginning. See all the objects first.", "phase3_instr1", 0),
        ("Use whatever grouping method feels intuitive to you.", "phase3_instr2", 0),
    ]
    gc.collect()  # free Phase 2 memory before Phase 3 task
    for text, label, _ in p3_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label):
            win.close()
            _close_dummy()
            return

    # Before grid: 16 shapes, for context
    p3_before_grid = [
        ("You will now see all 16 objects to be grouped at the same time — for reference only; just watch & don't memorize.", "phase3_before_grid", 0),
    ]
    for text, label, _ in p3_before_grid:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        if not wait_for_continue(win, stim, label):
            win.close()
            _close_dummy()
            return

    # Grid 5 sec — large preview + same miniature bottom-right inset as sorting trials
    grid_path = get_shape_grid_path()
    grid_img = visual.ImageStim(
        win, image=grid_path, units='height', size=_image_size_height_units(grid_path, PHASE13_GRID_PREVIEW_MAX_EXTENT)
    )
    grid_inset_ref = _make_grid_inset_stim(win, grid_path)
    _log_ttl_event("phase3_grid_onset")
    grid_img.draw()
    grid_inset_ref.draw()
    win.flip()
    _wait(PHASE_GRID_PREVIEW_SEC)
    _log_ttl_event("phase3_grid_offset")
    del grid_inset_ref

    # Fixation 1 sec — keep miniature grid in bottom-right
    fix = visual.TextStim(win, text='+', color='black', height=0.08, pos=(0, 0))
    grid_inset_ref = _make_grid_inset_stim(win, grid_path)
    _log_ttl_event("phase3_fixation_onset")
    fix.draw()
    grid_inset_ref.draw()
    win.flip()
    _wait(PHASE_FIXATION_CROSS_SEC)
    _log_ttl_event("phase3_fixation_offset")
    del grid_inset_ref

    p3_instr2_screens = [
        ("As before, sort the objects. Click to place — Enter locks.", "phase3_instruction2c", 0),
    ]
    for text, label, _ in p3_instr2_screens:
        stim = visual.TextStim(win, text=text, color='black', height=0.04, pos=(0, 0), wrapWidth=1.4, units='height')
        grid_inset_ref = _make_grid_inset_stim(win, grid_path)
        if not wait_for_continue(win, stim, label, extra_drawables=[grid_inset_ref]):
            win.close()
            _close_dummy()
            return
        del grid_inset_ref

    shapes3 = get_shape_paths()
    random.shuffle(shapes3)
    while shapes3 == shapes:
        random.shuffle(shapes3)
    phase3_results = run_drag_phase(win, mouse, shapes3, "phase3", 3, participant, timestamp_str=timestamp_str, inset_grid_path=grid_path)
    gc.collect()
    if phase3_results is None:
        win.close()
        _close_dummy()
        return
    _log_ttl_event("phase3_complete")

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

    thanks = visual.TextStim(win, text="Done. Thank you!", color='black', height=0.05, pos=(0, 0))
    _log_ttl_event("thanks_onset")
    thanks.draw()
    win.flip()
    _wait(THANKS_SCREEN_SEC)
    _log_ttl_event("thanks_offset")
    win.close()
    _close_dummy()


if __name__ == '__main__':
    main()
