"""
Blackbody Radiation & The Ultraviolet Catastrophe
==================================================
Animation showing:
  Act 1: Heating iron — color changes with temperature
  Act 2: Experimental spectrum curves at different temperatures
  Act 3: Rayleigh-Jeans classical theory → diverges (Ultraviolet Catastrophe!)
  Act 4: Planck's quantum fix — perfect match
  Act 5: Summary

Output: blackbody_radiation.gif on Desktop
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap

rcParams['font.family'] = 'Calibri'
rcParams['font.size'] = 13

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
h = 6.626e-34
k_B = 1.381e-23
c = 3e8

FPS = 24
DPI = 120
FIG_W, FIG_H = 14, 6.5

BG_COLOR = '#0a0a1a'
TEXT_COLOR = '#e0e0e0'
SUBTITLE_COLOR = '#ffffff'

# ---------------------------------------------------------------------------
# Physics
# ---------------------------------------------------------------------------

def planck(nu, T):
    """Planck's law spectral radiance."""
    with np.errstate(over='ignore', divide='ignore'):
        x = h * nu / (k_B * T)
        denom = np.expm1(x)
        result = 8 * np.pi * h * nu**3 / (c**3 * denom)
        result = np.where(np.isfinite(result), result, 0)
    return result

def rayleigh_jeans(nu, T):
    """Rayleigh-Jeans classical approximation."""
    return 8 * np.pi * k_B * T * nu**2 / c**3

def temp_to_rgb(T):
    """Approximate blackbody color for display (simplified)."""
    # Map temperature to a visual color for the iron block
    if T < 800:
        return '#3a3a3a'  # dark grey, not glowing
    elif T < 1200:
        t = (T - 800) / 400
        r = int(80 + 120 * t)
        return f'#{r:02x}1500'
    elif T < 2000:
        t = (T - 1200) / 800
        r = int(200 + 55 * t)
        g = int(21 + 80 * t)
        return f'#{r:02x}{g:02x}00'
    elif T < 4000:
        t = (T - 2000) / 2000
        r = 255
        g = int(101 + 100 * t)
        b = int(50 * t)
        return f'#{r:02x}{g:02x}{b:02x}'
    elif T < 7000:
        t = (T - 4000) / 3000
        r = 255
        g = int(201 + 54 * t)
        b = int(50 + 180 * t)
        return f'#{r:02x}{g:02x}{b:02x}'
    else:
        return '#fffaf0'  # white-hot

# ---------------------------------------------------------------------------
# Frame allocation
# ---------------------------------------------------------------------------
ACT1_FRAMES = FPS * 8     # Heating iron
ACT2_FRAMES = FPS * 10    # Experimental curves
ACT3_FRAMES = FPS * 12    # Rayleigh-Jeans catastrophe
ACT4_FRAMES = FPS * 12    # Planck's fix
ACT5_FRAMES = FPS * 5     # Summary

TOTAL = ACT1_FRAMES + ACT2_FRAMES + ACT3_FRAMES + ACT4_FRAMES + ACT5_FRAMES
T1 = ACT1_FRAMES
T2 = T1 + ACT2_FRAMES
T3 = T2 + ACT3_FRAMES
T4 = T3 + ACT4_FRAMES
T5 = TOTAL

print(f"Total frames: {TOTAL}, duration: {TOTAL/FPS:.1f}s")

# ---------------------------------------------------------------------------
# Precompute spectrum data
# ---------------------------------------------------------------------------
nu_max = 2.5e15  # Hz — covers visible + UV
nu = np.linspace(1e12, nu_max, 1000)

# Temperatures for experimental curves
temps_exp = [3000, 4000, 5000, 6000]
temp_colors_exp = ['#ff4444', '#ff8844', '#ffcc44', '#ffffff']

# For Act 3: single temperature to compare classical vs quantum
T_compare = 5000

planck_5000 = planck(nu, T_compare)
rj_5000 = rayleigh_jeans(nu, T_compare)

# Normalize for plotting
planck_norm = planck_5000 / planck_5000.max()
rj_norm = rj_5000 / planck_5000.max()  # normalize to same scale
rj_norm_clipped = np.clip(rj_norm, 0, 5)  # let it go high but not insane

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=BG_COLOR)
fig.subplots_adjust(left=0.06, right=0.96, top=0.88, bottom=0.13)

# We'll use a single axes and manage everything manually
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

def setup_spectrum_axes(ax, y_max=1.3, x_label=True):
    """Setup axes for spectrum plot."""
    ax.set_xlim(0, nu_max)
    ax.set_ylim(0, y_max)
    ax.set_facecolor(BG_COLOR)
    ax.spines['bottom'].set_color(TEXT_COLOR)
    ax.spines['left'].set_color(TEXT_COLOR)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)
    if x_label:
        ax.set_xlabel('Frequency  ν', color=TEXT_COLOR, fontsize=13, fontfamily='Calibri')
    ax.set_ylabel('Intensity  I(ν)', color=TEXT_COLOR, fontsize=13, fontfamily='Calibri')
    # Mark visible range
    vis_lo, vis_hi = 4e14, 7.5e14
    ax.axvspan(vis_lo, vis_hi, alpha=0.08, color='white', zorder=0)
    ax.text((vis_lo + vis_hi)/2, y_max * 0.95, 'Visible', color='#888888',
            fontsize=9, ha='center', va='top', fontfamily='Calibri')

# ---------------------------------------------------------------------------
# Drawing helpers for Act 1
# ---------------------------------------------------------------------------
def draw_iron_block(ax, T, cx=0.35, cy=0.5):
    """Draw an iron block with temperature-dependent color (in axes coords as fractions)."""
    # We'll draw in data coordinates. Map to axes fraction.
    color = temp_to_rgb(T)
    # Iron block
    bw, bh = nu_max * 0.12, 0.25
    bx = nu_max * cx - bw/2
    by = cy - bh/2
    rect = patches.FancyBboxPatch((bx, by), bw, bh,
                                   boxstyle='round,pad=0.01',
                                   fc=color, ec='#888888', lw=2, zorder=10)
    ax.add_patch(rect)

    # Glow effect for high temperatures
    if T > 1000:
        glow_alpha = min(0.3, (T - 1000) / 10000)
        glow = patches.FancyBboxPatch((bx - bw*0.15, by - bh*0.15),
                                       bw * 1.3, bh * 1.3,
                                       boxstyle='round,pad=0.03',
                                       fc=color, ec='none', alpha=glow_alpha, zorder=9)
        ax.add_patch(glow)

    # Temperature label
    ax.text(nu_max * cx, cy - bh/2 - 0.06, f'T = {T:.0f} K',
            color=TEXT_COLOR, ha='center', fontsize=14, fontfamily='Calibri',
            fontweight='bold', zorder=11)


# ---------------------------------------------------------------------------
# Act 3: Shake effect
# ---------------------------------------------------------------------------
shake_offsets = np.random.uniform(-0.02, 0.02, TOTAL)

# ---------------------------------------------------------------------------
# Animation update
# ---------------------------------------------------------------------------
def update(frame):
    ax.clear()
    clear_texts()

    # ── Act 1: Heating iron ──
    if frame < T1:
        progress = frame / T1
        T_current = 300 + (7000 - 300) * progress

        ax.set_xlim(0, nu_max)
        ax.set_ylim(0, 1.3)
        ax.set_facecolor(BG_COLOR)
        ax.axis('off')

        draw_iron_block(ax, T_current, cx=0.5, cy=0.6)

        draw_title('Heating an Iron Block', color='#ffaa44')

        if progress < 0.3:
            draw_subtitle("Every object emits radiation. Heat it up, and it starts to glow.")
        elif progress < 0.7:
            draw_subtitle(f"Red hot → Orange → Yellow... the color depends on temperature")
        else:
            draw_subtitle("At very high temperatures, it glows white-hot. But WHY these specific colors?")
        return

    # ── Act 2: Experimental curves ──
    if frame < T2:
        progress = (frame - T1) / ACT2_FRAMES
        setup_spectrum_axes(ax, y_max=1.3)

        # Draw curves one by one
        n_curves = len(temps_exp)
        for i, (T_exp, col) in enumerate(zip(temps_exp, temp_colors_exp)):
            curve_start = i / n_curves
            curve_end = (i + 1) / n_curves
            if progress < curve_start:
                continue

            spec = planck(nu, T_exp)
            spec_norm = spec / planck(nu, 6000).max()

            if progress < curve_end:
                # Partially draw this curve
                frac = (progress - curve_start) / (curve_end - curve_start)
                n_pts = max(2, int(frac * len(nu)))
                ax.plot(nu[:n_pts], spec_norm[:n_pts], color=col, lw=2.5, zorder=3)
            else:
                ax.plot(nu, spec_norm, color=col, lw=2, alpha=0.8, zorder=3)

            # Label
            if progress >= curve_end - 0.02:
                peak_idx = np.argmax(spec_norm)
                ax.text(nu[peak_idx], spec_norm[peak_idx] + 0.05,
                        f'{T_exp} K', color=col, fontsize=10, ha='center',
                        fontfamily='Calibri', fontweight='bold')

        draw_title('Experimental Blackbody Spectra', color='#ffcc44')

        if progress < 0.5:
            draw_subtitle("Scientists measured the radiation spectrum at different temperatures...")
        else:
            draw_subtitle("Higher temperature → peak shifts to higher frequency (Wien's Law)")
        return

    # ── Act 3: Rayleigh-Jeans catastrophe ──
    if frame < T3:
        progress = (frame - T2) / ACT3_FRAMES

        # Shake effect in the catastrophe phase
        is_catastrophe = progress > 0.45 and progress < 0.85
        if is_catastrophe:
            shake = shake_offsets[frame] * 3
            fig.subplots_adjust(left=0.06 + shake, bottom=0.13 + shake * 0.5)
        else:
            fig.subplots_adjust(left=0.06, bottom=0.13)

        # Dynamic y-limit to show divergence
        if progress < 0.4:
            y_max = 1.3
        elif progress < 0.85:
            # Ramp up y-max to show the divergence growing
            ramp = (progress - 0.4) / 0.45
            y_max = 1.3 + 3.7 * ramp  # goes up to 5.0
        else:
            y_max = 1.3  # reset for Planck preview

        setup_spectrum_axes(ax, y_max=y_max)

        # Always show experimental data (Planck at 5000K as "experiment")
        ax.plot(nu, planck_norm, '--', color='#ffffff', lw=2, alpha=0.6,
                label='Experiment (5000 K)', zorder=2)

        if progress < 0.4:
            # Draw Rayleigh-Jeans gradually
            frac = progress / 0.4
            n_pts = max(2, int(frac * len(nu)))
            rj_show = rj_norm_clipped[:n_pts]
            ax.plot(nu[:n_pts], rj_show, color='#ff3333', lw=3, zorder=4)

            draw_title('Classical Theory: Rayleigh-Jeans Law', color='#ff4444')
            draw_subtitle("The classical formula matches at low frequencies... looking good so far...")

        elif progress < 0.85:
            # Show full RJ curve going crazy
            rj_display = np.clip(rj_norm, 0, y_max * 1.2)
            ax.plot(nu, rj_display, color='#ff3333', lw=3, zorder=4)

            # Red warning overlay
            if is_catastrophe:
                warning_alpha = 0.08 + 0.07 * np.sin(frame * 0.5)
                ax.axvspan(7e14, nu_max, alpha=warning_alpha, color='red', zorder=1)

            # Infinity arrow
            ax.annotate('→  ∞ !', xy=(nu_max * 0.85, y_max * 0.85),
                        fontsize=28, color='#ff3333', fontweight='bold',
                        fontfamily='Calibri', zorder=10)

            draw_title('ULTRAVIOLET CATASTROPHE!', color='#ff2222')
            draw_subtitle("At high frequencies, classical theory predicts INFINITE energy! This is absurd.")

        else:
            # Calm down, show the problem clearly
            fig.subplots_adjust(left=0.06, bottom=0.13)
            ax.plot(nu, rj_norm_clipped, color='#ff3333', lw=2, alpha=0.5, zorder=3,
                    label='Rayleigh-Jeans (Classical)')

            draw_title('The Classical Theory Has Failed', color='#ff6666')
            draw_subtitle("We need a new theory. In 1900, Max Planck found the answer...")

        ax.legend(loc='upper right', fontsize=10, facecolor='#1a1a2e',
                  edgecolor='#333', labelcolor=TEXT_COLOR)
        return

    # ── Act 4: Planck's fix ──
    if frame < T4:
        progress = (frame - T3) / ACT4_FRAMES
        fig.subplots_adjust(left=0.06, bottom=0.13)
        setup_spectrum_axes(ax, y_max=1.3)

        # Show experimental data
        ax.plot(nu, planck_norm, '--', color='#ffffff', lw=2, alpha=0.5,
                label='Experiment', zorder=2)

        # Show classical (faded)
        ax.plot(nu, rj_norm_clipped, color='#ff3333', lw=1.5, alpha=0.25,
                label='Classical (fails!)', zorder=2)

        if progress < 0.55:
            # Draw Planck curve gradually
            frac = progress / 0.55
            n_pts = max(2, int(frac * len(nu)))
            ax.plot(nu[:n_pts], planck_norm[:n_pts], color='#00ff88', lw=3.5, zorder=5)

            draw_title("Planck's Quantum Hypothesis", color='#00ff88')
            if progress < 0.3:
                draw_subtitle("Planck's bold idea: energy is not continuous, but comes in discrete packets")
            else:
                draw_subtitle("E = nhν  — energy is quantized! Let's see if the math works...")

        elif progress < 0.8:
            # Full Planck curve — perfect match
            ax.plot(nu, planck_norm, color='#00ff88', lw=3.5, zorder=5,
                    label="Planck's Law")

            # Highlight perfect match
            ax.fill_between(nu, planck_norm, alpha=0.1, color='#00ff88', zorder=1)

            draw_title("PERFECT MATCH!", color='#00ff88')
            draw_subtitle("Planck's formula matches the experiment at ALL frequencies — low AND high")

        else:
            # Show the key formula
            ax.plot(nu, planck_norm, color='#00ff88', lw=3, zorder=5,
                    label="Planck's Law")

            # Big formula in the middle
            ax.text(nu_max * 0.5, 0.7, r'$E = nh\nu$', fontsize=36,
                    color='#00ff88', ha='center', va='center',
                    fontfamily='Calibri', fontweight='bold', zorder=10,
                    bbox=dict(boxstyle='round,pad=0.3', fc='#0a0a1aCC', ec='#00ff88', lw=2))

            # Discrete energy visualization - small dots
            for i, x_pos in enumerate(np.linspace(nu_max*0.15, nu_max*0.45, 8)):
                y_base = 0.15
                n_quanta = i + 1
                for j in range(min(n_quanta, 5)):
                    circle = plt.Circle((x_pos, y_base + j * 0.06), nu_max * 0.008,
                                       fc='#00ff88', ec='none', alpha=0.7, zorder=10)
                    ax.add_patch(circle)

            ax.text(nu_max * 0.30, 0.05, 'Energy packets (quanta)',
                    color='#00ff88', fontsize=10, ha='center', fontfamily='Calibri')

            draw_title("Energy is Quantized", color='#00ff88')
            draw_subtitle("Energy comes in discrete packets: E = nhν.  h = 6.626 × 10⁻³⁴ J·s (Planck's constant)")

        ax.legend(loc='upper right', fontsize=10, facecolor='#1a1a2e',
                  edgecolor='#333', labelcolor=TEXT_COLOR)
        return

    # ── Act 5: Summary ──
    if frame < T5:
        progress = (frame - T4) / ACT5_FRAMES
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_facecolor(BG_COLOR)
        ax.axis('off')

        # Three column summary
        # Classical
        ax.text(2.5, 8.5, 'Classical', color='#ff4444', fontsize=18,
                ha='center', fontweight='bold', fontfamily='Calibri')
        ax.text(2.5, 7.3, 'Energy is continuous\nlike water flowing', color=TEXT_COLOR,
                fontsize=12, ha='center', fontfamily='Calibri')
        ax.text(2.5, 6.0, '→ Predicts ∞ energy\nat high frequency',
                color='#ff4444', fontsize=12, ha='center', fontfamily='Calibri')
        ax.text(2.5, 5.0, 'X  FAILS', color='#ff4444', fontsize=20,
                ha='center', fontweight='bold', fontfamily='Calibri')

        # Arrow
        ax.annotate('', xy=(6, 6.5), xytext=(4.5, 6.5),
                    arrowprops=dict(arrowstyle='->', color=TEXT_COLOR, lw=2))

        # Quantum
        ax.text(7.5, 8.5, 'Quantum (Planck)', color='#00ff88', fontsize=18,
                ha='center', fontweight='bold', fontfamily='Calibri')
        ax.text(7.5, 7.3, 'Energy is discrete\nlike grains of sand', color=TEXT_COLOR,
                fontsize=12, ha='center', fontfamily='Calibri')
        ax.text(7.5, 6.0, '→ Matches experiment\nat ALL frequencies',
                color='#00ff88', fontsize=12, ha='center', fontfamily='Calibri')
        ax.text(7.5, 5.0, 'WORKS', color='#00ff88', fontsize=20,
                ha='center', fontweight='bold', fontfamily='Calibri')

        # Big formula at bottom
        ax.text(5, 2.8, r'$E = nh\nu$', fontsize=48,
                color='#00ff88', ha='center', va='center', fontfamily='Calibri',
                fontweight='bold')
        ax.text(5, 1.5, 'The first crack in classical physics.',
                color=SUBTITLE_COLOR, fontsize=16, ha='center', fontfamily='Calibri')

        draw_title('The First Quantum Idea (1900)', color='#ffcc44')
        return

# ---------------------------------------------------------------------------
# Build and save
# ---------------------------------------------------------------------------
print("Building blackbody radiation animation...")
anim = FuncAnimation(fig, update, frames=TOTAL, interval=1000//FPS, blit=False)

output_path = r'C:\Users\18101\Desktop\blackbody_radiation.gif'
print(f"Saving to {output_path} ...")
writer = PillowWriter(fps=FPS)
anim.save(output_path, writer=writer, dpi=DPI)
print(f"Done! Saved to {output_path}")
plt.close()
