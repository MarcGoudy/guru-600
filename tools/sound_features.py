"""Empreinte d'un son rendu (WAV de p600_render) : timbre moyen (spectre en 24 bandes log, normalisé), brillance au fil
du temps (centroïde, 16 points) et volume au fil du temps (RMS, 16 points), sur l'accord tenu puis relâché (0 à 3,5 s)
et sur la phrase. Distance entre deux sons : mêmes poids pour le timbre, la brillance et le volume.
    venv/bin/python p600/sound_features.py DOSSIER.wav... -> features.npz"""
import sys, wave, glob, os
import numpy as np

SR = 44100

def load(path):
    w = wave.open(path)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32).reshape(-1, 2).mean(1) / 32768
    return a

def feat(a):
    seg = a[: int(3.5 * SR)]                      # the chord, held 2 s then released
    n, hop = 2048, 1024
    frames = np.lib.stride_tricks.sliding_window_view(seg, n)[::hop] * np.hanning(n)
    spec = np.abs(np.fft.rfft(frames, axis=1)) + 1e-9
    freqs = np.fft.rfftfreq(n, 1 / SR)
    edges = np.geomspace(80, 16000, 25)
    bands = np.stack([spec[:, (freqs >= edges[i]) & (freqs < edges[i + 1])].sum(1) for i in range(24)], 1)
    rms = np.sqrt((frames ** 2).mean(1)) + 1e-9
    tim = np.log(bands[: len(bands) * 2 // 3].mean(0) + 1e-6); tim -= tim.mean(); tim /= np.linalg.norm(tim) + 1e-9
    cen = (spec * freqs).sum(1) / spec.sum(1)
    idx = np.linspace(0, len(rms) - 1, 16).astype(int)
    cen16 = np.log2(cen[idx] + 1) / 14
    vol16 = 20 * np.log10(rms[idx] / rms.max()) / 60
    ph = a[int(3.5 * SR): int(6 * SR)]
    phr = np.sqrt(np.mean(ph.reshape(-1, 2205) ** 2, 1)) + 1e-9 if len(ph) >= 2205 * 4 else np.zeros(40)
    phr = 20 * np.log10(phr[:40] / (phr.max() + 1e-9)) / 60
    return np.concatenate([tim * 2, cen16, vol16, phr * 0.5]), float(rms.max())

if __name__ == '__main__':
    out = sys.argv[-1]
    names, F, L = [], [], []
    for d in sys.argv[1:-1]:
        for p in sorted(glob.glob(os.path.join(d, '*.wav'))):
            f, l = feat(load(p)); names.append(os.path.basename(d) + '/' + os.path.basename(p)); F.append(f); L.append(l)
    np.savez(out, names=np.array(names), F=np.array(F), L=np.array(L))
    print(len(names), 'empreintes ->', out)
