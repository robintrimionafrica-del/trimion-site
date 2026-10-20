# Original 8-second R&B instrumental for the post videos: deep 808 sub bass, claps, hats, warm pad.
# Mixed with headroom (peak -1.5 dBFS, about -15 dB RMS) so phone speakers don't distort.
import numpy as np, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR = 48000; BPM = 90; BEAT = 60 / BPM; DUR = 8.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
def t(n): return np.arange(n) / SR
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def place(buf, snd, at):
    i = int(at * SR); j = min(len(buf), i + len(snd))
    if i < len(buf): buf[i:j] += snd[:j - i]
def note(m): return 440 * 2 ** ((m - 69) / 12)

# Chords (one per 4 beats): Am9, Fmaj9, G6/9 -> roots A1, F1, G1
CH = [([57, 60, 64, 67, 71], 33), ([53, 57, 60, 64, 67], 29), ([55, 59, 62, 64, 69], 31)]

L = np.zeros(N); R = np.zeros(N); SUB = np.zeros(N)

# 808: sine with a fast pitch drop, long tail, gentle harmonics so small speakers can "hear" it
def k808(freq, length):
    n = int(length * SR); tt = t(n)
    f = freq * (1 + 1.6 * np.exp(-tt / 0.018))
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.exp(-tt / (length * 0.55)) * np.minimum(1, tt / 0.002)
    s = np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.22 * np.sin(3 * ph) + 0.08 * np.sin(4 * ph)
    click = np.exp(-tt / 0.004) * np.sin(2 * np.pi * 1800 * tt) * 0.25
    return np.tanh(1.3 * s * env) / np.tanh(1.3) + click
for bar in range(3):
    root = note(CH[bar][1])
    for b, ln, mul in [(0, 1.4, 1), (1.5, 0.9, 1), (2.75, 1.2, 1.335 if bar == 2 else 1)]:
        place(SUB, k808(root * mul, ln), (bar * 4 + b) * BEAT)

# Kick punch on top of the 808 (short, tight)
def kick():
    n = int(0.18 * SR); tt = t(n)
    f = 55 * (1 + 4 * np.exp(-tt / 0.012)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt / 0.06)
K = np.zeros(N)
for bar in range(3):
    for b in (0, 1.5, 2.75): place(K, kick(), (bar * 4 + b) * BEAT)

# Clap on 2 and 4, with a wide echo
def clap():
    n = int(0.35 * SR); tt = t(n); nz = rng.standard_normal(n)
    env = sum(np.exp(-np.maximum(tt - d, 0) / 0.009) * (tt >= d) for d in (0, 0.011, 0.023)) + 0.6 * np.exp(-np.maximum(tt - 0.03, 0) / 0.12) * (tt >= 0.03)
    return bp(nz, 900, 4500) * env
C = np.zeros(N)
for beat in range(12):
    if beat % 2 == 1: place(C, clap(), beat * BEAT)

# Hats: 8ths with a 1/32 roll at the end of each bar
def hat(v=1.0):
    n = int(0.05 * SR); tt = t(n)
    return hp(rng.standard_normal(n), 7000) * np.exp(-tt / 0.012) * v
H = np.zeros(N)
for bar in range(3):
    for e in range(8):
        if e == 7:
            for r in range(4): place(H, hat(0.55 + 0.1 * r), (bar * 4 + 3.5 + r * 0.125) * BEAT)
        else: place(H, hat(1.0 if e % 2 == 0 else 0.6), (bar * 4 + e * 0.5) * BEAT)

# Pad: detuned saws, low-passed, slow attack
P = np.zeros(N)
for bar, (notes, _) in enumerate(CH):
    n = int(4 * BEAT * SR) + int(0.4 * SR); tt = t(n); s = np.zeros(n)
    for m in notes:
        for d in (-0.07, 0.0, 0.07):
            f = note(m + d); s += 2 * ((tt * f) % 1) - 1
    env = np.minimum(1, tt / 0.35) * np.minimum(1, np.maximum(0, (n / SR - tt) / 0.5))
    place(P, lp(s, 1600) * env / 15, bar * 4 * BEAT)
# Pluck melody (sine bell) on offbeats
M = np.zeros(N)
mel = [76, 0, 74, 72, 0, 71, 72, 0, 69, 0, 71, 72, 74, 0, 72, 71, 0, 67, 69, 0, 71, 0, 74, 76]
for i, m in enumerate(mel):
    if not m: continue
    n = int(0.6 * SR); tt = t(n); f = note(m)
    place(M, (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.22), i * 0.5 * BEAT)

def echo(x, d, fb, wet):
    y = x.copy(); k = int(d * SR)
    for i in range(1, 5): y[k * i:] += x[:-k * i] * (fb ** i) * wet if k * i < len(x) else 0
    return y
def verb(x, wet=0.3):
    y = x.copy()
    for d, g in [(0.029, .5), (0.037, .45), (0.041, .4), (0.053, .35), (0.067, .3), (0.079, .25)]:
        k = int(d * SR); z = np.zeros_like(x)
        for i in range(1, 8):
            if k * i < len(x): z[k * i:] += x[:-k * i] * g ** i
        y += lp(z, 5000) * wet / 3
    return y

SUB = hp(lp(SUB, 320), 34)                 # clean sub: nothing below 32 Hz, nothing harsh above
Cw = verb(echo(C, BEAT * 0.75, 0.35, 1), 0.5)
Pw = verb(P, 0.6); Mw = verb(echo(M, BEAT * 0.75, 0.4, 1), 0.5)
mono = 0.8 * SUB + 0.6 * K + 0.75 * Cw + 0.3 * H + 0.55 * Pw + 0.3 * Mw
# Stereo width on pad, hats and melody only (bass stays centred)
side = 0.12 * (np.roll(Pw, 300) - Pw) + 0.06 * (np.roll(H, 120) - H) + 0.05 * (np.roll(Mw, 500) - Mw)
L = mono + side; R = mono - side
st = np.stack([L, R], 1)
fade = np.ones(N); fade[:int(.01 * SR)] = np.linspace(0, 1, int(.01 * SR)); fade[-int(.35 * SR):] = np.linspace(1, 0, int(.35 * SR))
st *= fade[:, None]
st = st / np.max(np.abs(st)) * 10 ** (-1.5 / 20)   # peak -1.5 dBFS
rms = 20 * np.log10(np.sqrt(np.mean(st ** 2)))
print('peak -1.5 dBFS, RMS %.1f dB' % rms)
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
