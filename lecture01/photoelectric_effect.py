"""
Photoelectric Effect Animation
===============================
Animation showing:
  Act 1: Classical prediction (what we'd expect)
  Act 2: Experiment — vary intensity (more electrons, same energy)
  Act 3: Experiment — vary frequency (threshold! energy depends on frequency)
  Act 4: Classical theory fails (side-by-side comparison)
  Act 5: Einstein's explanation — photons!
  Act 6: Replay with photon model
  Act 7: Summary

Output: photoelectric_effect.gif on Desktop
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import rcParams

rcParams['font.family'] = 'Calibri'
rcParams['font.size'] = 13

FPS = 24
DPI = 120
FIG_W, FIG_H = 14, 6.5

BG_COLOR = '#0a0a1a'
TEXT_COLOR = '#e0e0e0'
SUBTITLE_COLOR = '#ffffff'
METAL_COLOR = '#7788aa'
ELECTRON_COLOR = '#00ccff'
PHOTON_COLORS = {
    'red': '#ff3333',
    'green': '#33ff33',
    'blue': '#3388ff',
    'violet': '#aa44ff',
}

np.random.seed(123)

# ---------------------------------------------------------------------------
# Frame allocation
# ---------------------------------------------------------------------------
ACT1_FRAMES = FPS * 6     # Classical prediction
ACT2_FRAMES = FPS * 12    # Vary intensity
ACT3_FRAMES = FPS * 14    # Vary frequency
ACT4_FRAMES = FPS * 6     # Classical fails
ACT5_FRAMES = FPS * 12    # Einstein's photons
ACT6_FRAMES = FPS * 10    # Replay with photon model
ACT7_FRAMES = FPS * 5     # Summary

TOTAL = ACT1_FRAMES + ACT2_FRAMES + ACT3_FRAMES + ACT4_FRAMES + ACT5_FRAMES + ACT6_FRAMES + ACT7_FRAMES
boundaries = np.cumsum([0, ACT1_FRAMES, ACT2_FRAMES, ACT3_FRAMES, ACT4_FRAMES, ACT5_FRAMES, ACT6_FRAMES, ACT7_FRAMES])
T0, T1, T2, T3, T4, T5, T6, T7 = boundaries

print(f"Total frames: {TOTAL}, duration: {TOTAL/FPS:.1f}s")

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=BG_COLOR)
ax = fig.add_subplot(111)

subtitle_obj = None
title_obj = None

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
                            bbox=dict(boxstyle='round,pad=0.4', fc='#000000aa', ec='none'))

def draw_title(text, color=TEXT_COLOR):
    global title_obj
    title_obj = fig.text(0.5, 0.93, text, color=color, fontsize=18,
                         ha='center', fontfamily='Calibri', fontweight='bold')


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_metal_plate(ax, x=5.0):
    """Draw the metal plate (target)."""
    plate_w = 0.3
    plate_h = 4.0
    rect = patches.FancyBboxPatch((x - plate_w/2, 3 - plate_h/2),
                                   plate_w, plate_h,
                                   boxstyle='round,pad=0.02',
                                   fc=METAL_COLOR, ec='#99aabb', lw=2, zorder=5)
    ax.add_patch(rect)
    ax.text(x, 0.6, 'Metal', color=TEXT_COLOR, ha='center', fontsize=10,
            fontfamily='Calibri')

def draw_light_wave(ax, x_start, x_end, y_center, amplitude, wavelength, color, phase=0, alpha=1.0):
    """Draw a sinusoidal light wave."""
    x = np.linspace(x_start, x_end, 300)
    y = y_center + amplitude * np.sin(2 * np.pi * (x - phase) / wavelength)
    ax.plot(x, y, color=color, lw=2, alpha=alpha, zorder=3)
    # Draw a few more lines for "beam" effect
    for offset in [-0.15, 0.15]:
        y2 = y_center + offset + amplitude * np.sin(2 * np.pi * (x - phase) / wavelength + 0.3)
        ax.plot(x, y2, color=color, lw=1, alpha=alpha * 0.4, zorder=3)

def draw_photons(ax, positions, color, size=12):
    """Draw photon particles as glowing dots."""
    for (px, py) in positions:
        ax.plot(px, py, 'o', color=color, ms=size, alpha=0.9, zorder=8)
        ax.plot(px, py, 'o', color=color, ms=size * 1.8, alpha=0.2, zorder=7)

def draw_electrons(ax, positions, velocities=None):
    """Draw ejected electrons with velocity arrows."""
    for i, (ex, ey) in enumerate(positions):
        ax.plot(ex, ey, 'o', color=ELECTRON_COLOR, ms=6, zorder=8)
        if velocities is not None and i < len(velocities):
            vx = velocities[i]
            ax.annotate('', xy=(ex + vx, ey), xytext=(ex, ey),
                        arrowprops=dict(arrowstyle='->', color=ELECTRON_COLOR, lw=1.5),
                        zorder=9)

def draw_data_panel(ax, freq_label, intensity_label, n_electrons, e_energy, panel_x=8.0):
    """Draw a data readout panel on the right side."""
    panel_y = 4.8
    ax.text(panel_x, panel_y, 'DATA PANEL', color='#888888', fontsize=11,
            fontfamily='Calibri', fontweight='bold')
    ax.text(panel_x, panel_y - 0.5, f'Frequency:  {freq_label}', color=TEXT_COLOR,
            fontsize=12, fontfamily='Calibri')
    ax.text(panel_x, panel_y - 1.0, f'Intensity:   {intensity_label}', color=TEXT_COLOR,
            fontsize=12, fontfamily='Calibri')
    ax.text(panel_x, panel_y - 1.7, f'Electrons out:  {n_electrons}', color=ELECTRON_COLOR,
            fontsize=13, fontfamily='Calibri', fontweight='bold')
    ax.text(panel_x, panel_y - 2.2, f'Electron energy: {e_energy}', color=ELECTRON_COLOR,
            fontsize=13, fontfamily='Calibri', fontweight='bold')

def setup_experiment_axes(ax):
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off')


# ---------------------------------------------------------------------------
# Pre-generate electron trajectories
# ---------------------------------------------------------------------------
def gen_electrons_burst(n, start_x=5.3, y_center=3.0, spread=1.5, max_vx=1.5):
    """Generate n electrons ejected from the plate."""
    ys = y_center + np.random.uniform(-spread, spread, n)
    vxs = np.random.uniform(0.3, max_vx, n)
    return [(start_x, y) for y in ys], vxs.tolist()


# ---------------------------------------------------------------------------
# Animation update
# ---------------------------------------------------------------------------
def update(frame):
    ax.clear()
    clear_texts()

    # ── Act 1: Classical prediction ──
    if frame < T1:
        progress = (frame - T0) / ACT1_FRAMES
        setup_experiment_axes(ax)

        # Title
        draw_title('Classical Prediction', color='#ffaa44')

        # Show setup with light wave
        draw_metal_plate(ax)
        phase = frame * 0.15
        draw_light_wave(ax, 0.5, 4.8, 3.0, 0.3, 1.2, '#ffcc44', phase=phase)

        # Classical prediction text
        ax.text(8, 4.5, 'Classical theory predicts:', color='#ffaa44',
                fontsize=13, fontfamily='Calibri', fontweight='bold')

        items = [
            ('1. Brighter light = faster electrons', 0.25),
            ('2. Any color works, if bright enough', 0.5),
            ('3. Dim light needs time to build up energy', 0.75),
        ]
        for text, threshold in items:
            if progress > threshold:
                ax.text(8, 4.5 - items.index((text, threshold)) * 0.6 - 0.6,
                        text, color=TEXT_COLOR, fontsize=11, fontfamily='Calibri')

        draw_subtitle("In 1887, Heinrich Hertz discovered something that broke these predictions...")
        return

    # ── Act 2: Vary intensity ──
    if frame < T2:
        progress = (frame - T1) / ACT2_FRAMES
        setup_experiment_axes(ax)
        draw_title('Experiment: Vary Light Intensity', color='#3388ff')
        draw_metal_plate(ax)

        # Intensity ramps up over time
        if progress < 0.15:
            intensity = 0.2
            label_int = 'Low'
            n_e = 2
        elif progress < 0.4:
            intensity = 0.2 + 0.6 * ((progress - 0.15) / 0.25)
            label_int = 'Medium'
            n_e = 5
        elif progress < 0.65:
            intensity = 0.8
            label_int = 'Medium'
            n_e = 5
        else:
            intensity = 1.0
            label_int = 'High'
            n_e = 10

        # Blue light wave with varying amplitude
        phase = frame * 0.15
        draw_light_wave(ax, 0.5, 4.8, 3.0, 0.15 + 0.35 * intensity,
                        1.0, '#3388ff', phase=phase, alpha=0.5 + 0.5 * intensity)

        # Electrons — number changes, but arrow length (energy) stays the same!
        e_energy = 0.8  # fixed!
        if progress > 0.1:
            np.random.seed(int(progress * 5))
            positions, _ = gen_electrons_burst(n_e, max_vx=e_energy)
            vxs = [e_energy] * n_e
            # Animate electrons moving outward
            anim_t = (progress * 3) % 1.0
            moved_pos = [(px + vx * anim_t * 1.5, py + np.random.uniform(-0.05, 0.05))
                         for (px, py), vx in zip(positions, vxs)]
            draw_electrons(ax, moved_pos, vxs)

        draw_data_panel(ax, 'Blue (fixed)', label_int, n_e,
                        f'{e_energy:.1f} eV (CONSTANT!)')

        # Intensity bar
        bar_x, bar_y = 1.5, 0.8
        ax.add_patch(patches.Rectangle((bar_x, bar_y), 2.5, 0.3,
                                        fc='#1a1a2e', ec='#555', lw=1))
        ax.add_patch(patches.Rectangle((bar_x, bar_y), 2.5 * intensity, 0.3,
                                        fc='#3388ff', ec='none'))
        ax.text(bar_x + 1.25, bar_y - 0.25, 'Intensity', color=TEXT_COLOR,
                fontsize=10, ha='center', fontfamily='Calibri')

        if progress < 0.5:
            draw_subtitle("Increase brightness: MORE electrons come out...")
        else:
            draw_subtitle("...but each electron has the SAME energy! Classical prediction #1: WRONG!")
        return

    # ── Act 3: Vary frequency ──
    if frame < T3:
        progress = (frame - T2) / ACT3_FRAMES
        setup_experiment_axes(ax)
        draw_title('Experiment: Vary Light Frequency', color='#aa44ff')
        draw_metal_plate(ax)

        # Frequency sweep: red → green → blue → violet
        if progress < 0.25:
            color = '#ff3333'
            wavelength = 2.0
            freq_label = 'Red (low)'
            can_eject = False
            e_energy = 0
            sub_progress = progress / 0.25
        elif progress < 0.45:
            color = '#ff8833'
            wavelength = 1.6
            freq_label = 'Orange (low-mid)'
            can_eject = False
            e_energy = 0
            sub_progress = (progress - 0.25) / 0.2
        elif progress < 0.6:
            # threshold moment!
            color = '#33cc33'
            wavelength = 1.2
            freq_label = 'Green (threshold!)'
            can_eject = True
            e_energy = 0.4
            sub_progress = (progress - 0.45) / 0.15
        elif progress < 0.78:
            color = '#3388ff'
            wavelength = 0.9
            freq_label = 'Blue (above threshold)'
            can_eject = True
            e_energy = 1.2
            sub_progress = (progress - 0.6) / 0.18
        else:
            color = '#aa44ff'
            wavelength = 0.7
            freq_label = 'Violet (high)'
            can_eject = True
            e_energy = 2.0
            sub_progress = (progress - 0.78) / 0.22

        phase = frame * 0.15
        draw_light_wave(ax, 0.5, 4.8, 3.0, 0.3, wavelength, color, phase=phase)

        # Frequency bar
        bar_x, bar_y = 1.5, 0.8
        freq_frac = min(1.0, progress / 0.85)
        ax.add_patch(patches.Rectangle((bar_x, bar_y), 2.5, 0.3,
                                        fc='#1a1a2e', ec='#555', lw=1))
        # Rainbow gradient approximation
        colors_bar = ['#ff3333', '#ff8833', '#ffff33', '#33ff33', '#3388ff', '#aa44ff']
        for i, c in enumerate(colors_bar):
            seg_w = 2.5 / len(colors_bar)
            if bar_x + i * seg_w < bar_x + 2.5 * freq_frac:
                draw_w = min(seg_w, bar_x + 2.5 * freq_frac - bar_x - i * seg_w)
                if draw_w > 0:
                    ax.add_patch(patches.Rectangle((bar_x + i * seg_w, bar_y),
                                                    draw_w, 0.3, fc=c, ec='none', alpha=0.8))
        ax.text(bar_x + 1.25, bar_y - 0.25, 'Frequency', color=TEXT_COLOR,
                fontsize=10, ha='center', fontfamily='Calibri')

        if not can_eject:
            # No electrons — show "X" on the plate
            ax.text(5.0, 3.0, 'X', color='#ff3333', fontsize=36,
                    ha='center', va='center', fontweight='bold', zorder=12)
            n_e = 0
        else:
            # Electrons with energy proportional to frequency
            np.random.seed(42)
            n_e = 5
            positions, _ = gen_electrons_burst(n_e, max_vx=e_energy)
            vxs = [e_energy] * n_e
            anim_t = (sub_progress * 2) % 1.0
            moved_pos = [(px + vx * anim_t * 1.5, py + np.random.uniform(-0.03, 0.03))
                         for (px, py), vx in zip(positions, vxs)]
            draw_electrons(ax, moved_pos, vxs)

        draw_data_panel(ax, freq_label, 'Fixed',
                        n_e, f'{e_energy:.1f} eV' if e_energy > 0 else 'N/A')

        # Threshold line annotation
        if progress > 0.4:
            ax.text(8, 1.5, 'Threshold frequency exists!',
                    color='#ffcc00', fontsize=12, fontfamily='Calibri', fontweight='bold')

        if progress < 0.25:
            draw_subtitle("Red light: no electrons at all, no matter how long we wait!")
        elif progress < 0.45:
            draw_subtitle("Still nothing! Below threshold frequency = zero electrons")
        elif progress < 0.6:
            draw_subtitle("At the threshold frequency: electrons finally appear!")
        elif progress < 0.78:
            draw_subtitle("Higher frequency = each electron has MORE energy. Classical prediction #2: WRONG!")
        else:
            draw_subtitle("Violet light: electrons are very energetic. Energy depends on COLOR, not brightness!")
        return

    # ── Act 4: Classical fails ──
    if frame < T4:
        progress = (frame - T3) / ACT4_FRAMES
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 6)
        ax.set_facecolor(BG_COLOR)
        ax.axis('off')

        draw_title('Classical Theory: Three Strikes', color='#ff4444')

        predictions = [
            ('Brighter = faster electrons', 'More electrons, SAME speed', 1.5),
            ('Any color works', 'Below threshold = NOTHING', 3.0),
            ('Dim light needs time', 'Electrons come out INSTANTLY', 4.5),
        ]

        for i, (classical, experiment, x_offset) in enumerate(predictions):
            show_at = i * 0.25
            if progress > show_at:
                y = 4.5 - i * 1.3
                ax.text(1, y, f'#{i+1}', color='#888888', fontsize=14,
                        fontfamily='Calibri', fontweight='bold')
                ax.text(2, y, f'Predicted: {classical}', color='#ff6666',
                        fontsize=12, fontfamily='Calibri')
                ax.text(2, y - 0.45, f'Reality:      {experiment}', color='#66ff88',
                        fontsize=12, fontfamily='Calibri')
                # Strike-through on prediction
                if progress > show_at + 0.15:
                    ax.plot([1.9, 7.2], [y, y], color='#ff3333', lw=2, zorder=10)

        if progress > 0.8:
            ax.text(6, 0.8, 'We need a completely new idea...', color='#ffcc44',
                    fontsize=16, ha='center', fontfamily='Calibri', fontweight='bold')

        draw_subtitle("Classical wave theory fails ALL three predictions. Something fundamental is wrong.")
        return

    # ── Act 5: Einstein's explanation ──
    if frame < T5:
        progress = (frame - T4) / ACT5_FRAMES
        setup_experiment_axes(ax)
        draw_metal_plate(ax)

        draw_title("Einstein's Explanation: Light = Photons (1905)", color='#ffcc44')

        if progress < 0.35:
            # Show transition: wave → particles
            phase = frame * 0.15
            # Fading wave
            wave_alpha = max(0, 1.0 - progress / 0.35)
            draw_light_wave(ax, 0.5, 4.8, 3.0, 0.3, 1.0, '#3388ff',
                            phase=phase, alpha=wave_alpha)

            # Appearing photons
            photon_alpha = min(1.0, progress / 0.2)
            n_photons = int(progress / 0.35 * 6) + 1
            photon_xs = np.linspace(1.0, 4.5, 8)[:n_photons]
            photon_ys = 3.0 + 0.2 * np.sin(photon_xs * 3 + frame * 0.2)
            for px, py in zip(photon_xs, photon_ys):
                ax.plot(px, py, 'o', color='#ffcc44', ms=14, alpha=photon_alpha, zorder=8)
                ax.plot(px, py, 'o', color='#ffcc44', ms=22, alpha=photon_alpha * 0.2, zorder=7)

            draw_subtitle("Einstein's radical idea: light is not a continuous wave, but discrete PHOTONS")

        elif progress < 0.65:
            # Photon hits electron — billiard ball collision
            sub_p = (progress - 0.35) / 0.3

            # Photon approaching
            photon_x = 2.0 + sub_p * 2.8  # moves from 2.0 to 4.8
            if photon_x < 4.9:
                ax.plot(photon_x, 3.0, 'o', color='#ffcc44', ms=16, zorder=8)
                ax.plot(photon_x, 3.0, 'o', color='#ffcc44', ms=26, alpha=0.2, zorder=7)
                ax.text(photon_x, 3.5, r'E = h$\nu$', color='#ffcc44',
                        fontsize=12, ha='center', fontfamily='Calibri')

            # After collision
            if sub_p > 0.85:
                # Photon disappears, electron flies out
                e_x = 5.3 + (sub_p - 0.85) * 8
                ax.plot(e_x, 3.0, 'o', color=ELECTRON_COLOR, ms=8, zorder=8)
                ax.annotate('', xy=(e_x + 0.8, 3.0), xytext=(e_x, 3.0),
                            arrowprops=dict(arrowstyle='->', color=ELECTRON_COLOR, lw=2))
                # "Burst" effect at collision point
                for angle in np.linspace(0, 2*np.pi, 8):
                    bx = 5.0 + 0.3 * np.cos(angle)
                    by = 3.0 + 0.3 * np.sin(angle)
                    ax.plot(bx, by, '*', color='#ffcc44', ms=4, alpha=0.5)

            draw_subtitle("One photon hits one electron — like a billiard ball collision!")

        else:
            # Energy equation
            sub_p = (progress - 0.65) / 0.35

            # Show the equation building up
            ax.text(6, 4.8, 'The Energy Equation:', color='#ffcc44',
                    fontsize=14, fontfamily='Calibri', fontweight='bold')

            # E_photon = hv
            ax.text(6, 4.0, r'Photon energy:   E = h$\nu$', color='#ffcc44',
                    fontsize=13, fontfamily='Calibri')

            if sub_p > 0.2:
                ax.text(6, 3.3, 'Work function:    W  (energy to escape metal)',
                        color=METAL_COLOR, fontsize=13, fontfamily='Calibri')

            if sub_p > 0.4:
                ax.text(6, 2.3, r'Electron energy:  $E_k$ = h$\nu$ - W',
                        color=ELECTRON_COLOR, fontsize=16, fontfamily='Calibri',
                        fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', fc='#0a0a1aCC',
                                  ec=ELECTRON_COLOR, lw=2))

            if sub_p > 0.6:
                ax.text(6, 1.4, r'If h$\nu$ < W  :  electron CANNOT escape!',
                        color='#ff4444', fontsize=13, fontfamily='Calibri')
                ax.text(6, 0.8, r'If h$\nu$ > W  :  electron escapes with energy h$\nu$ - W',
                        color='#66ff88', fontsize=13, fontfamily='Calibri')

            # Visual: energy bar diagram on the left
            bar_x = 1.5
            # Photon energy bar
            ax.add_patch(patches.Rectangle((bar_x, 1.0), 0.8, 3.5,
                                            fc='#ffcc44', alpha=0.3, ec='#ffcc44', lw=2))
            ax.text(bar_x + 0.4, 4.7, r'h$\nu$', color='#ffcc44', fontsize=14,
                    ha='center', fontfamily='Calibri', fontweight='bold')

            # Work function portion
            ax.add_patch(patches.Rectangle((bar_x, 1.0), 0.8, 1.5,
                                            fc=METAL_COLOR, alpha=0.5, ec=METAL_COLOR, lw=2))
            ax.text(bar_x + 0.4, 1.75, 'W', color='#ffffff', fontsize=14,
                    ha='center', fontfamily='Calibri', fontweight='bold')

            # Electron kinetic energy portion
            if sub_p > 0.4:
                ax.add_patch(patches.Rectangle((bar_x, 2.5), 0.8, 2.0,
                                                fc=ELECTRON_COLOR, alpha=0.3,
                                                ec=ELECTRON_COLOR, lw=2))
                ax.text(bar_x + 0.4, 3.5, r'$E_k$', color=ELECTRON_COLOR, fontsize=14,
                        ha='center', fontfamily='Calibri', fontweight='bold')

            draw_subtitle(r"E_k = hv - W  :  everything is explained by one simple equation!")
        return

    # ── Act 6: Replay with photon model ──
    if frame < T6:
        progress = (frame - T5) / ACT6_FRAMES
        setup_experiment_axes(ax)
        draw_metal_plate(ax)

        draw_title('Photon Model Explains Everything', color='#00ff88')

        if progress < 0.5:
            # Red photons — can't eject
            sub_p = progress / 0.5
            n_photons = 4
            for i in range(n_photons):
                px = 1.0 + i * 0.9 + sub_p * 3.0
                py = 2.5 + i * 0.4
                if px < 4.9:
                    ax.plot(px, py, 'o', color='#ff3333', ms=14, zorder=8)
                    ax.plot(px, py, 'o', color='#ff3333', ms=22, alpha=0.2, zorder=7)
                elif px < 5.5:
                    # Hit and shatter
                    for angle in np.linspace(0, 2*np.pi, 6):
                        sx = 5.0 + 0.2 * np.cos(angle) * (px - 4.9) * 3
                        sy = py + 0.2 * np.sin(angle) * (px - 4.9) * 3
                        ax.plot(sx, sy, '.', color='#ff3333', ms=3, alpha=0.5)

            ax.text(7, 4.5, 'Red photon energy:', color='#ff3333',
                    fontsize=13, fontfamily='Calibri', fontweight='bold')
            ax.text(7, 3.8, r'h$\nu_{red}$ < W', color='#ff3333',
                    fontsize=16, fontfamily='Calibri')
            ax.text(7, 3.0, 'Not enough energy!', color='#ff3333',
                    fontsize=13, fontfamily='Calibri')
            ax.text(7, 2.3, 'Photon absorbed,\nelectron stays put.', color=TEXT_COLOR,
                    fontsize=12, fontfamily='Calibri')

            draw_subtitle("Red photons: too little energy per photon. No electrons escape, no matter how many photons!")

        else:
            # Blue/violet photons — eject electrons
            sub_p = (progress - 0.5) / 0.5
            n_photons = 4
            for i in range(n_photons):
                px = 1.0 + i * 0.9 + sub_p * 3.0
                py = 2.5 + i * 0.4
                if px < 4.9:
                    ax.plot(px, py, 'o', color='#aa44ff', ms=14, zorder=8)
                    ax.plot(px, py, 'o', color='#aa44ff', ms=22, alpha=0.2, zorder=7)
                else:
                    # Electron ejected!
                    ex = 5.3 + (px - 4.9) * 1.2
                    ey = py
                    if ex < 10:
                        ax.plot(ex, ey, 'o', color=ELECTRON_COLOR, ms=7, zorder=8)
                        ax.annotate('', xy=(ex + 0.6, ey), xytext=(ex, ey),
                                    arrowprops=dict(arrowstyle='->', color=ELECTRON_COLOR, lw=1.5))

            ax.text(7, 4.5, 'Violet photon energy:', color='#aa44ff',
                    fontsize=13, fontfamily='Calibri', fontweight='bold')
            ax.text(7, 3.8, r'h$\nu_{violet}$ > W', color='#aa44ff',
                    fontsize=16, fontfamily='Calibri')
            ax.text(7, 3.0, 'Enough energy!', color='#00ff88',
                    fontsize=13, fontfamily='Calibri')
            ax.text(7, 2.3, 'Electron escapes with\n' + r'$E_k$ = h$\nu$ - W', color=TEXT_COLOR,
                    fontsize=12, fontfamily='Calibri')

            draw_subtitle("Violet photons: each one carries enough energy. Electrons fly out instantly!")
        return

    # ── Act 7: Summary ──
    if frame < T7:
        progress = (frame - T6) / ACT7_FRAMES
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 6)
        ax.set_facecolor(BG_COLOR)
        ax.axis('off')

        draw_title('The Photoelectric Effect (Nobel Prize 1921)', color='#ffcc44')

        # Key formula
        ax.text(6, 4.2, r'$E_k = h\nu - W$', fontsize=40,
                color='#ffcc44', ha='center', va='center', fontfamily='Calibri',
                fontweight='bold')

        # Two columns
        ax.text(3, 2.8, 'Light is a WAVE', color='#ff4444', fontsize=15,
                ha='center', fontfamily='Calibri', fontweight='bold')
        ax.text(3, 2.2, 'X  Cannot explain', color='#ff4444', fontsize=13,
                ha='center', fontfamily='Calibri')

        ax.text(9, 2.8, 'Light is PHOTONS', color='#00ff88', fontsize=15,
                ha='center', fontfamily='Calibri', fontweight='bold')
        ax.text(9, 2.2, 'Explains everything', color='#00ff88', fontsize=13,
                ha='center', fontfamily='Calibri')

        ax.plot([6, 6], [2.0, 3.2], color='#555555', lw=1)

        ax.text(6, 1.0, 'Light is both wave AND particle.\nThe second crack in classical physics.',
                color=SUBTITLE_COLOR, fontsize=15, ha='center', fontfamily='Calibri',
                linespacing=1.5)

        return

# ---------------------------------------------------------------------------
# Build and save
# ---------------------------------------------------------------------------
print("Building photoelectric effect animation...")
anim = FuncAnimation(fig, update, frames=TOTAL, interval=1000//FPS, blit=False)

output_path = r'C:\Users\18101\Desktop\photoelectric_effect.gif'
print(f"Saving to {output_path} ...")
writer = PillowWriter(fps=FPS)
anim.save(output_path, writer=writer, dpi=DPI)
print(f"Done! Saved to {output_path}")
plt.close()
