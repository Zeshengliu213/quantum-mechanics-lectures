"""
Double-Slit Experiment Animation  (complete rewrite)
=====================================================
Four acts demonstrating the core mystery of quantum mechanics:

  Act 1 (~14s): Classical wave theory — Huygens wavelets, 2D interference
                field, bright/dark fringes on screen
  Act 2 (~16s): Quantum electrons, no detector — dots accumulate into
                interference pattern
  Act 3 (~12s): Which-way detector — collapse, two Gaussian blobs
  Act 4  (~5s): Text-only summary table

Output: double_slit_animation.gif in lecture01 folder
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap

# ---------------------------------------------------------------------------
# Global style  (matches photoelectric_effect.py)
# ---------------------------------------------------------------------------
rcParams['font.family'] = 'Calibri'
rcParams['font.size'] = 13

FPS = 24
DPI = 120
FIG_W, FIG_H = 14, 6.5

BG_COLOR      = '#0a0a1a'
TEXT_COLOR    = '#e0e0e0'
SUBTITLE_COLOR = '#ffffff'
WAVE_COLOR    = '#5ba4e6'      # blue  – classical waves
QUANT_COLOR   = '#b07ee8'      # purple – quantum electrons
DET_COLOR     = '#e05454'      # red   – detector
BARRIER_COLOR = '#556677'
SCREEN_COLOR  = '#334455'

np.random.seed(42)

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
SOURCE_X  = 1.0
BARRIER_X = 4.5
SCREEN_X  = 10.0
SLIT_Y1   = 3.8    # upper slit centre (figure y coords 0-6)
SLIT_Y2   = 2.2    # lower slit centre
SLIT_W    = 0.18   # slit width
BARRIER_W = 0.18

# Double-slit physics (for sampling distribution)
d   = 1.0    # slit separation (arbitrary units that scale to the figure)
a   = 0.25   # slit width
lam = 0.12   # de Broglie wavelength
L   = 4.0    # source-to-screen effective distance

# ---------------------------------------------------------------------------
# Frame allocation
# ---------------------------------------------------------------------------
ACT1_FRAMES = FPS * 14   # 14 s
ACT2_FRAMES = FPS * 16   # 16 s
ACT3_FRAMES = FPS * 12   # 12 s
ACT4_FRAMES = FPS * 5    #  5 s

TOTAL = ACT1_FRAMES + ACT2_FRAMES + ACT3_FRAMES + ACT4_FRAMES
bounds = np.cumsum([0, ACT1_FRAMES, ACT2_FRAMES, ACT3_FRAMES, ACT4_FRAMES])
T0, T1, T2, T3, T4 = bounds

print(f"Total frames: {TOTAL}, duration: {TOTAL/FPS:.1f}s")

# ---------------------------------------------------------------------------
# Figure setup  (single-axes design)
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=BG_COLOR)
fig.subplots_adjust(left=0.06, right=0.96, top=0.88, bottom=0.13)
ax = fig.add_subplot(111)

subtitle_obj = None
title_obj    = None

def clear_texts():
    global subtitle_obj, title_obj
    if subtitle_obj is not None:
        subtitle_obj.remove()
        subtitle_obj = None
    if title_obj is not None:
        title_obj.remove()
        title_obj = None

def draw_subtitle(text, y=0.04):
    global subtitle_obj
    subtitle_obj = fig.text(0.5, y, text, color=SUBTITLE_COLOR, fontsize=14,
                            ha='center', va='center', fontfamily='Calibri',
                            fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.4',
                                      fc='#000000aa', ec='none'))

def draw_title(text, color=TEXT_COLOR):
    global title_obj
    title_obj = fig.text(0.5, 0.93, text, color=color, fontsize=18,
                         ha='center', fontfamily='Calibri', fontweight='bold')

def setup_axes():
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_barrier(show_detector=False, detector_flash=False):
    """Draw wall with two slits."""
    mid_y   = (SLIT_Y1 + SLIT_Y2) / 2.0   # 3.0
    gap_top = SLIT_Y1 - SLIT_W / 2          # bottom of upper slit opening
    gap_bot = SLIT_Y2 + SLIT_W / 2          # top  of lower slit opening

    # top block
    ax.add_patch(patches.Rectangle(
        (BARRIER_X - BARRIER_W / 2, SLIT_Y1 + SLIT_W / 2),
        BARRIER_W, 6.0 - (SLIT_Y1 + SLIT_W / 2),
        fc=BARRIER_COLOR, ec='none', zorder=5))
    # middle block (between slits)
    ax.add_patch(patches.Rectangle(
        (BARRIER_X - BARRIER_W / 2, SLIT_Y2 + SLIT_W / 2),
        BARRIER_W, (SLIT_Y1 - SLIT_W / 2) - (SLIT_Y2 + SLIT_W / 2),
        fc=BARRIER_COLOR, ec='none', zorder=5))
    # bottom block
    ax.add_patch(patches.Rectangle(
        (BARRIER_X - BARRIER_W / 2, 0.0),
        BARRIER_W, SLIT_Y2 - SLIT_W / 2,
        fc=BARRIER_COLOR, ec='none', zorder=5))

    # screen
    ax.plot([SCREEN_X, SCREEN_X], [0.2, 5.8],
            color=SCREEN_COLOR, lw=3, zorder=3)
    ax.text(SCREEN_X, 0.08, 'Screen', color=TEXT_COLOR, ha='center',
            fontsize=9, fontfamily='Calibri')

    # slit labels
    ax.text(BARRIER_X - 0.35, SLIT_Y1, 'S₁', color=TEXT_COLOR, ha='right',
            va='center', fontsize=9, fontfamily='Calibri')
    ax.text(BARRIER_X - 0.35, SLIT_Y2, 'S₂', color=TEXT_COLOR, ha='right',
            va='center', fontsize=9, fontfamily='Calibri')

    if show_detector:
        # Red square detectors
        glow_alpha = 0.6 + 0.4 * np.sin(detector_flash * 0.5) if detector_flash else 0.6
        for sy in [SLIT_Y1, SLIT_Y2]:
            det_x = BARRIER_X + 0.35
            ax.plot(det_x, sy, 's', color=DET_COLOR, ms=12,
                    zorder=10, markeredgecolor='#ff8888', markeredgewidth=1)
            # glow
            ax.plot(det_x, sy, 's', color=DET_COLOR, ms=24,
                    alpha=0.25 * glow_alpha, zorder=9)
        ax.text(BARRIER_X + 0.75, 3.0, 'Detector\nON',
                color=DET_COLOR, ha='left', va='center',
                fontsize=11, fontweight='bold', fontfamily='Calibri')


def draw_electron_gun():
    """Draw the electron gun (square marker) on the left."""
    gx, gy = SOURCE_X, 3.0
    ax.add_patch(patches.FancyBboxPatch(
        (gx - 0.35, gy - 0.28), 0.7, 0.56,
        boxstyle='round,pad=0.04',
        fc='#223344', ec=QUANT_COLOR, lw=1.5, zorder=6))
    ax.text(gx, gy, 'e⁻\ngun', color=QUANT_COLOR, ha='center', va='center',
            fontsize=8, fontfamily='Calibri', fontweight='bold', zorder=7)


# ---------------------------------------------------------------------------
# Pre-compute 2D interference intensity grid  (done ONCE, outside update)
# ---------------------------------------------------------------------------
NX, NY = 260, 220
_xs = np.linspace(BARRIER_X + 0.05, SCREEN_X - 0.05, NX)
_ys = np.linspace(0.3, 5.7, NY)
_XX, _YY = np.meshgrid(_xs, _ys)   # shape (NY, NX)

# distances from each slit
_R1 = np.sqrt((_XX - BARRIER_X) ** 2 + (_YY - SLIT_Y1) ** 2)
_R2 = np.sqrt((_XX - BARRIER_X) ** 2 + (_YY - SLIT_Y2) ** 2)

# wavenumber scaled to figure units (tuned for visible fringes)
_k = 14.0

# pre-compute R values clamped away from 0
_R1_safe = np.maximum(_R1, 0.05)
_R2_safe = np.maximum(_R2, 0.05)

# envelope (amplitude / sqrt(r)) — stored for fast combination with phase
_A1 = 1.0 / np.sqrt(_R1_safe)
_A2 = 1.0 / np.sqrt(_R2_safe)

# screen intensity (time-averaged, no phase) for static fringe bands
_SCREEN_Y = np.linspace(0.3, 5.7, 300)
_r1_screen = np.abs(_SCREEN_Y - SLIT_Y1)
_r2_screen = np.abs(_SCREEN_Y - SLIT_Y2)
_screen_I  = np.cos(_k * (_r1_screen - _r2_screen) / 2.0) ** 2

# colourmap: dark blue → bright cyan/white  (interference field)
_cmap_wave = LinearSegmentedColormap.from_list(
    'wave', ['#0a0a1a', '#0a1a3a', '#1040a0', '#2080e0', '#80d0ff', '#ffffff'])

# colourmap: dark → amber  (screen intensity bands)
_cmap_screen = LinearSegmentedColormap.from_list(
    'screen', ['#0a0a1a', '#1a1a2a', '#5ba4e6', '#aaddff', '#ffffff'])

# ---------------------------------------------------------------------------
# Pre-sample electron hit positions for Acts 2 & 3
# ---------------------------------------------------------------------------
N_ELECTRONS = 350

# Act 2: interference distribution  P ∝ cos²(π d y / λL) · sinc²(π a y / λL)
# y in figure units: map screen range [0.3, 5.7] → centred at 3.0
def _interference_pdf(y_fig):
    y = y_fig - 3.0   # centre at 0
    arg_cos  = np.pi * d * y / (lam * L)
    arg_sinc = a * y / (lam * L)
    return (np.cos(arg_cos) ** 2) * (np.sinc(arg_sinc) ** 2)

def _sample_pdf(pdf_func, n, ylo=0.4, yhi=5.6):
    y_grid = np.linspace(ylo, yhi, 3000)
    p = pdf_func(y_grid)
    p /= p.max()
    samples = []
    while len(samples) < n:
        cands = np.random.uniform(ylo, yhi, n * 4)
        u     = np.random.uniform(0, 1, n * 4)
        pvals = np.interp(cands, y_grid, p)
        samples.extend(cands[u < pvals].tolist())
    return np.array(samples[:n])

hits_quantum = _sample_pdf(_interference_pdf, N_ELECTRONS)

# Act 3: Gaussian blobs around each slit centre (no interference)
_which_slit3 = np.random.choice([0, 1], size=N_ELECTRONS)
hits_detector = np.where(
    _which_slit3 == 0,
    np.random.normal(SLIT_Y1, 0.38, N_ELECTRONS),
    np.random.normal(SLIT_Y2, 0.38, N_ELECTRONS))
hits_detector = np.clip(hits_detector, 0.35, 5.65)

# ---------------------------------------------------------------------------
# Subtitle text sequences for Act 1
# ---------------------------------------------------------------------------
_ACT1_SUBTITLES = [
    (0.0,  0.28, "Each slit acts as a new wave source (Huygens)"),
    (0.28, 0.58, "Waves superpose → constructive + destructive interference"),
    (0.58, 1.01, "Classical prediction: bright and dark fringes"),
]

# ---------------------------------------------------------------------------
# Animation update
# ---------------------------------------------------------------------------
def update(frame):
    ax.clear()
    clear_texts()
    setup_axes()

    # ── Act 1: Classical wave theory ──────────────────────────────────────
    if frame < T1:
        progress = (frame - T0) / ACT1_FRAMES
        draw_title('Act I: Classical Wave Theory', color=WAVE_COLOR)

        # --- incoming plane wave (horizontal sinusoidal lines, scrolling) ---
        phase_scroll = frame * 0.22   # scrolling speed
        n_lines = 9
        for i in range(n_lines):
            y_line = 0.5 + i * (5.0 / (n_lines - 1))
            x_wave = np.linspace(0.05, BARRIER_X - BARRIER_W / 2, 200)
            y_wave = y_line + 0.10 * np.sin(2 * np.pi * (x_wave - phase_scroll) / 0.55)
            alpha  = 0.25 + 0.55 * np.exp(-((y_line - 3.0) ** 2) / 3.5)
            ax.plot(x_wave, y_wave, color=WAVE_COLOR, lw=0.9, alpha=alpha, zorder=2)

        # source label
        ax.plot(SOURCE_X, 3.0, '>', color=WAVE_COLOR, ms=7, zorder=6)
        ax.text(SOURCE_X, 0.18, 'Source', color=TEXT_COLOR, ha='center',
                fontsize=9, fontfamily='Calibri')

        # --- barrier ---
        draw_barrier()

        # --- Huygens circular wavelets from each slit ---
        # Number of rings grows with time
        max_rings = max(1, int(progress * 22))
        phase_ring = frame * 0.22
        ring_spacing = 0.50

        for slit_y in [SLIT_Y1, SLIT_Y2]:
            for ring_idx in range(1, max_rings + 1):
                radius = ring_idx * ring_spacing - (phase_ring % ring_spacing)
                if radius <= 0.05:
                    continue
                theta = np.linspace(-np.pi / 2, np.pi / 2, 160)
                rx = BARRIER_X + radius * np.cos(theta)
                ry = slit_y   + radius * np.sin(theta)
                # clip to axes
                mask = (rx > BARRIER_X + 0.05) & (rx < SCREEN_X + 0.1) & (ry > 0.0) & (ry < 6.0)
                fade = max(0.05, 0.7 - ring_idx * 0.04)
                if mask.sum() > 1:
                    ax.plot(rx[mask], ry[mask],
                            color=WAVE_COLOR, lw=0.7, alpha=fade, zorder=3)

        # --- 2D interference intensity field (imshow, pre-computed grid) ---
        phase_field = frame * 0.22
        field = (_A1 * np.cos(_k * _R1_safe - phase_field) +
                 _A2 * np.cos(_k * _R2_safe - phase_field)) ** 2
        # normalise to [0, 1]
        fmax = field.max()
        if fmax > 0:
            field /= fmax

        field_alpha = min(0.72, progress * 4.0)   # fade in gradually
        ax.imshow(field,
                  extent=[BARRIER_X + 0.05, SCREEN_X - 0.05, 0.3, 5.7],
                  origin='lower', aspect='auto',
                  cmap=_cmap_wave, alpha=field_alpha, zorder=1,
                  vmin=0, vmax=1)

        # --- screen intensity bands ---
        bar_w   = 0.28
        screen_alpha = min(0.9, progress * 5.0)
        for si in range(len(_SCREEN_Y) - 1):
            col = _cmap_screen(_screen_I[si])
            ax.add_patch(patches.Rectangle(
                (SCREEN_X, _SCREEN_Y[si]),
                bar_w, _SCREEN_Y[si + 1] - _SCREEN_Y[si],
                fc=col, ec='none', alpha=screen_alpha, zorder=4))

        # subtitle progression
        for t_start, t_end, text in _ACT1_SUBTITLES:
            if t_start <= progress < t_end:
                draw_subtitle(text)
                break
        return

    # ── Act 2: Quantum electrons, no detector ────────────────────────────
    if frame < T2:
        act_p  = (frame - T1) / ACT2_FRAMES
        act_f  = frame - T1               # frame index within act

        draw_title('Act II: Quantum Electrons — No Detector', color=QUANT_COLOR)
        draw_barrier()
        draw_electron_gun()

        n_shown = min(int(act_p * N_ELECTRONS) + 1, N_ELECTRONS)

        # accumulated dots on screen
        if n_shown > 0:
            ys_hit = hits_quantum[:n_shown]
            ax.scatter(np.full(n_shown, SCREEN_X + 0.06),
                       ys_hit, s=4, c=QUANT_COLOR, alpha=0.55, zorder=6,
                       linewidths=0)

        # electron in flight (ghost through both slits before barrier)
        if n_shown < N_ELECTRONS:
            traj_phase = (act_f % 18) / 18.0   # 0 → 1 over 18 frames
            fly_x = SOURCE_X + traj_phase * (SCREEN_X - SOURCE_X)
            target_y = hits_quantum[min(n_shown, N_ELECTRONS - 1)]

            if fly_x < BARRIER_X:
                # split ghost: going toward both slits
                t_frac = (fly_x - SOURCE_X) / (BARRIER_X - SOURCE_X)
                for sy in [SLIT_Y1, SLIT_Y2]:
                    fy = 3.0 + (sy - 3.0) * t_frac
                    ax.plot(fly_x, fy, 'o', color=QUANT_COLOR,
                            ms=5, alpha=0.45, zorder=8)
            else:
                # after barrier: two ghost paths converging on target
                t_frac = (fly_x - BARRIER_X) / (SCREEN_X - BARRIER_X)
                for sy in [SLIT_Y1, SLIT_Y2]:
                    fy = sy + (target_y - sy) * t_frac
                    ax.plot(fly_x, fy, 'o', color=QUANT_COLOR,
                            ms=5, alpha=0.35, zorder=8)

        # running count
        ax.text(0.4, 5.7, f'Electrons: {n_shown}', color=QUANT_COLOR,
                fontsize=11, fontfamily='Calibri', fontweight='bold',
                transform=ax.transData, zorder=10)

        if act_p < 0.55:
            draw_subtitle("Each electron arrives as a point — yet the pattern is a wave!")
        else:
            draw_subtitle("|ψ|² gives the probability distribution")
        return

    # ── Act 3: Which-way detector ─────────────────────────────────────────
    if frame < T3:
        act_p = (frame - T2) / ACT3_FRAMES
        act_f = frame - T2

        draw_title('Act III: Which-Way Detector', color=DET_COLOR)
        draw_barrier(show_detector=True, detector_flash=act_f)
        draw_electron_gun()

        n_shown = min(int(act_p * N_ELECTRONS) + 1, N_ELECTRONS)

        # accumulated dots — two blobs (warm orange-red)
        if n_shown > 0:
            ys_hit = hits_detector[:n_shown]
            cols = [DET_COLOR if _which_slit3[i] == 0 else '#e07040'
                    for i in range(n_shown)]
            ax.scatter(np.full(n_shown, SCREEN_X + 0.06),
                       ys_hit, s=4, c=cols, alpha=0.55, zorder=6,
                       linewidths=0)

        # electron in flight — definite path (single dot)
        if n_shown < N_ELECTRONS:
            traj_phase = (act_f % 18) / 18.0
            fly_x  = SOURCE_X + traj_phase * (SCREEN_X - SOURCE_X)
            i_curr = min(n_shown, N_ELECTRONS - 1)
            slit_y = SLIT_Y1 if _which_slit3[i_curr] == 0 else SLIT_Y2
            target_y = hits_detector[i_curr]
            if fly_x < BARRIER_X:
                t_frac = (fly_x - SOURCE_X) / (BARRIER_X - SOURCE_X)
                fy = 3.0 + (slit_y - 3.0) * t_frac
            else:
                t_frac = (fly_x - BARRIER_X) / (SCREEN_X - BARRIER_X)
                fy = slit_y + (target_y - slit_y) * t_frac
            ax.plot(fly_x, fy, 'o', color=DET_COLOR, ms=5, zorder=8)

        # running count
        ax.text(0.4, 5.7, f'Electrons: {n_shown}', color=DET_COLOR,
                fontsize=11, fontfamily='Calibri', fontweight='bold',
                transform=ax.transData, zorder=10)

        # explanatory panel on right
        panel_x = SCREEN_X + 0.55
        ax.text(panel_x, 5.2, 'Knowing which slit:', color=DET_COLOR,
                fontsize=11, fontfamily='Calibri', fontweight='bold')
        ax.text(panel_x, 4.7, '→ ψ collapses to', color=TEXT_COLOR,
                fontsize=10, fontfamily='Calibri')
        ax.text(panel_x, 4.35, '   one definite path', color=TEXT_COLOR,
                fontsize=10, fontfamily='Calibri')
        ax.text(panel_x, 3.75, '→ No superposition', color=TEXT_COLOR,
                fontsize=10, fontfamily='Calibri')
        ax.text(panel_x, 3.4, '→ No interference', color=TEXT_COLOR,
                fontsize=10, fontfamily='Calibri')
        ax.text(panel_x, 2.8, 'Result: two blobs', color=DET_COLOR,
                fontsize=11, fontfamily='Calibri', fontweight='bold')
        ax.text(panel_x, 2.4, '(classical!)', color=DET_COLOR,
                fontsize=10, fontfamily='Calibri')

        if act_p < 0.5:
            draw_subtitle("Knowing which slit destroys the superposition")
        else:
            draw_subtitle("Measurement = disturbance → interference vanishes")
        return

    # ── Act 4: Summary table ──────────────────────────────────────────────
    if frame < T4:
        draw_title('The Double-Slit Experiment — Summary', color=TEXT_COLOR)

        # three-row comparison table
        col_x = [1.5, 4.6, 8.2]
        row_y = [4.6, 3.6, 2.6]
        headers = ['Scenario', 'Pattern on Screen', 'Explanation']
        rows = [
            ('Classical wave',         'Interference fringes',    'Superposition of\nHuygens wavelets'),
            ('Quantum (no detector)',   'Interference fringes!',   '|ψ|² — electron\ngoes through both'),
            ('Quantum (with detector)', 'Two Gaussian blobs',      'Wave function\ncollapses on detection'),
        ]
        row_colors = [WAVE_COLOR, QUANT_COLOR, DET_COLOR]

        # header row
        for cx, hdr in zip(col_x, headers):
            ax.text(cx, 5.35, hdr, color='#aaaaaa', fontsize=12,
                    fontfamily='Calibri', fontweight='bold')

        # divider
        ax.plot([1.0, 11.0], [5.1, 5.1], color='#334455', lw=1)

        for ri, (row, ry, rc) in enumerate(zip(rows, row_y, row_colors)):
            for ci, (cell, cx) in enumerate(zip(row, col_x)):
                fa = 'Calibri'
                fw = 'bold' if ci == 0 else 'normal'
                fc = rc if ci == 0 else TEXT_COLOR
                ax.text(cx, ry, cell, color=fc, fontsize=11,
                        fontfamily=fa, fontweight=fw, va='center',
                        linespacing=1.4)
            ax.plot([1.0, 11.0], [ry - 0.55, ry - 0.55],
                    color='#223344', lw=0.8, alpha=0.7)

        ax.text(6.0, 1.0,
                '"If you think you understand quantum mechanics,\nyou don\'t understand quantum mechanics."  — Feynman',
                color='#888888', fontsize=11, ha='center', fontfamily='Calibri',
                style='italic', linespacing=1.5)

        draw_subtitle("The double-slit experiment: the heart of quantum mechanics")
        return


# ---------------------------------------------------------------------------
# Build and save
# ---------------------------------------------------------------------------
print(f"Total frames: {TOTAL}, duration: {TOTAL/FPS:.1f}s")
print("Building double-slit animation … this may take a few minutes.")

anim = FuncAnimation(fig, update, frames=TOTAL,
                     interval=1000 // FPS, blit=False)

output_path = r'C:\Users\18101\Desktop\downdload\量子力学讲义\lecture01\double_slit_animation.gif'
print(f"Saving to {output_path} ...")
writer = PillowWriter(fps=FPS)
anim.save(output_path, writer=writer, dpi=DPI)
print(f"Done! Saved to {output_path}")
plt.close()
