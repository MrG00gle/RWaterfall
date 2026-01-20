import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

samples = np.load("samples.npy")
fs = 20e6
n_fft = 1024
n_overlap = n_fft // 2

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 6))

# ────────────────────────────────
# Left: Waterfall (kept as one-sided / positive frequencies)
spec, freqs, times, im = ax_left.specgram(
    samples,
    NFFT=n_fft,
    Fs=fs,
    noverlap=n_overlap,
    detrend='mean',
    cmap='viridis',
    scale='dB',
    vmin=-90,
    vmax=-30
)
ax_left.set_xlabel('Time (s)')
ax_left.set_ylabel('Frequency (MHz)')
ax_left.set_title('Waterfall')
ax_left.set_ylim(0, fs/2 / 1e6)
fig.colorbar(im, ax=ax_left, label='dB', fraction=0.046, pad=0.04)

# ────────────────────────────────
# Right: PSD centered at 0 MHz (two-sided spectrum)
from scipy.signal import welch

f, Pxx = welch(
    samples,
    fs=fs,
    nperseg=n_fft,
    noverlap=n_overlap,
    window='hann',                # explicit window is good practice
    detrend='constant',           # ← fixed: use 'constant' instead of 'mean'
    scaling='spectrum',           # or 'density' — 'spectrum' gives power in V²
    return_onesided=False
)

Pxx_dB = 10 * np.log10(Pxx + 1e-20)

# Center 0 Hz
f_shifted = np.fft.fftshift(f) / 1e6
Pxx_dB_shifted = np.fft.fftshift(Pxx_dB)

ax_right.plot(f_shifted, Pxx_dB_shifted, lw=1.1, color='C0')
ax_right.set_xlabel('Frequency (MHz)')
ax_right.set_ylabel('Power (dB)')
ax_right.set_title('PSD (centered at 0 MHz)')
ax_right.grid(True, alpha=0.35)
ax_right.set_xlim(-fs/2e6, fs/2e6)          # symmetric around 0
ax_right.set_ylim(-100, -20)                # tune to your signal levels

plt.tight_layout()
plt.show()