#!/usr/bin/env python3
"""
assemble_ffmpeg.py v3 — Rough cut WildLens : zoom + clips IA + textes (avec bandeau) + musique.

Usage : python3 scripts/assemble_ffmpeg.py
"""

from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

VIDEO = Path("/Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/02_ARTEON/wildlens/video")
ASSETS = VIDEO / "assets"
CLIPS = VIDEO / "clips"
VO = VIDEO / "vo"
MUSIC = VIDEO / "musique"
OUT = VIDEO / "rough-cut"
TMP = OUT / "tmp"

IVOIRE = "0xF8F5F0"
IVOIRE_HEX = "#F8F5F0"
NOIR = "#0D0B09"
FPS = 25

# (type, source, audio, overlays)
SCENES = [
    ("image", "03-manuscrit-voynich.jpg",     "scene-01.mp3", ["title"]),
    ("image", "03-manuscrit-voynich.jpg",     "scene-02.mp3", ["kicker-02"]),
    ("clip",  "clip-b-spectrogramme.mp4",     "scene-03.mp3", ["kicker-03"]),
    ("image", "05-cerveau-passereau.jpg",     "scene-04.mp3", ["kicker-04"]),
    ("image", "06b-fleur-uv.jpg",             "scene-05.mp3", ["kicker-05"]),
    ("clip",  "clip-a-trou.mp4",              "scene-06.mp3", ["kicker-06"]),
    ("image", "08-anciens-corvide.jpg",       "scene-07.mp3", ["kicker-07"]),
    ("clip",  "clip-c-convergence.mp4",       "scene-08.mp3", ["kicker-08", "citation-08"]),
    ("image", "11-cloture-brume.jpg",         "scene-09.mp3", ["citation-09"]),
]

TITLE = "L'IA ne parlera jamais le langage du vivant"
SUBTITLE = "Du manuscrit de Voynich au chant des oiseaux — pourquoi la machine voit les motifs, pas le sens."
KICKERS = {
    "kicker-02": "Le manuscrit qui résiste",
    "kicker-03": "Le même mur, côté animal",
    "kicker-04": "Le cerveau ne suffit pas",
    "kicker-05": "La fleur qu'on ne voit pas",
    "kicker-06": "Peut-on déduire un monde inconnu ?",
    "kicker-07": "Ce que les anciens savaient",
    "kicker-08": "La loi du dialecte",
}
CITATIONS = {
    "citation-08": "Le dialecte est le luxe des signaux non vitaux.",
    "citation-09": "La machine cartographie ce qui est mesurable. Le sens appartient à celui qui reste immobile, qui écoute — et qui accepte d'être regardé en retour.",
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("❌", " ".join(cmd[:6]), "...")
        print(r.stderr[-700:])
        return False
    return True


def dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(f)],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def gen_png(path, text, size, pos="center", sub=None, italic=False):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    box = dict(boxstyle="round,pad=0.5", facecolor=IVOIRE_HEX, alpha=0.62, edgecolor="none")
    if pos == "center":
        ax.text(0.5, 0.55, text, fontsize=size, fontweight="bold", color=NOIR,
                ha="center", va="center", style="italic" if italic else "normal", bbox=box)
        if sub:
            ax.text(0.5, 0.40, sub, fontsize=int(size * 0.42), color=NOIR,
                    ha="center", va="center", bbox=box)
    elif pos == "topleft":
        ax.text(0.06, 0.92, text, fontsize=size, fontweight="bold", color=NOIR,
                ha="left", va="top", bbox=box)
    plt.savefig(path, transparent=True)
    plt.close(fig)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)

    music_files = sorted(MUSIC.glob("*"))
    music = random.choice(music_files)
    print(f"🎵 musique : {music.name}")

    # 1. textes
    gen_png(TMP / "title.png", TITLE, 60, "center", SUBTITLE)
    for k, t in KICKERS.items():
        gen_png(TMP / f"{k}.png", t, 38, "topleft")
    gen_png(TMP / "citation-08.png", CITATIONS["citation-08"], 52, "center", italic=True)
    gen_png(TMP / "citation-09.png", CITATIONS["citation-09"], 42, "center", italic=True)
    print("✅ textes générés")

    # 2. segments
    segs = []
    for i, (typ, src, audio, overlays) in enumerate(SCENES, 1):
        d = dur(VO / audio)
        seg = TMP / f"seg-{i:02d}.mp4"
        nframes = int(d * FPS)
        if typ == "image":
            vf = (f"scale=8000:-2,"
                  f"zoompan=z='min(zoom+0.0006,1.15)':d={nframes}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},format=yuv420p,setsar=1")
            ok = run(["ffmpeg", "-y", "-i", str(ASSETS / src), "-vf", vf,
                      "-frames:v", str(nframes), "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(seg)])
        else:
            ok = run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(CLIPS / src),
                      "-t", f"{d:.2f}", "-vf", "scale=1920:1080,fps=25,format=yuv420p,setsar=1",
                      "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(seg)])
        if not ok:
            return 1
        # superpose les textes (plusieurs possibles)
        specs = []
        for ov in overlays:
            if ov == "title":
                specs.append((TMP / "title.png", ""))
            elif ov.startswith("kicker"):
                specs.append((TMP / f"{ov}.png", ":enable='lt(t,6)'"))
            elif ov.startswith("citation"):
                specs.append((TMP / f"{ov}.png", f":enable='gt(t,{d-9:.1f})'"))
        if specs:
            seg2 = TMP / f"seg-{i:02d}-t.mp4"
            fc = ""
            prev = "[0:v]"
            for j in range(len(specs)):
                out_label = f"[o{j}]"
                fc += f"{prev}[{j+1}:v]overlay=0:0{specs[j][1]}{out_label};"
                prev = out_label
            fc += f"{prev}format=yuv420p[vout]"
            cmd = ["ffmpeg", "-y", "-i", str(seg)]
            for png, _ in specs:
                cmd += ["-i", str(png)]
            cmd += ["-filter_complex", fc, "-map", "[vout]",
                    "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(seg2)]
            if run(cmd):
                seg = seg2
        segs.append(seg)
        print(f"✅ seg-{i:02d}  {src:30} {d:6.1f}s ({typ}{' + ' + '+'.join(overlays) if overlays else ''})")
    seg_durs = [dur(s) for s in segs]

    # 3. voix off
    vo_full = TMP / "vo-full.m4a"
    vo_cmd = ["ffmpeg", "-y"]
    for _, _, a, _ in SCENES:
        vo_cmd += ["-i", str(VO / a)]
    vo_cmd += ["-filter_complex", f"concat=n={len(SCENES)}:v=0:a=1[out]", "-map", "[out]",
               "-c:a", "aac", "-b:a", "192k", str(vo_full)]
    if not run(vo_cmd):
        return 1
    print("✅ voix off concaténée")

    # 4. musique
    total = sum(seg_durs) - (len(seg_durs) - 1)
    music_bed = TMP / "music-bed.m4a"
    if not run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(music), "-vn", "-t", f"{total:.2f}",
                "-af", "volume=0.14", "-c:a", "aac", "-b:a", "128k", str(music_bed)]):
        return 1
    audio_mix = TMP / "audio-mix.m4a"
    if not run(["ffmpeg", "-y", "-i", str(vo_full), "-i", str(music_bed),
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[aout]",
                "-map", "[aout]", "-c:a", "aac", "-b:a", "192k", str(audio_mix)]):
        return 1
    print("✅ musique mixée")

    # 5. xfade
    inputs = []
    for s in segs:
        inputs += ["-i", str(s)]
    n = len(segs)
    fc, prev, cum, T = [], "[0:v]", seg_durs[0], 1.0
    for i in range(1, n):
        out = f"[v{i}]" if i < n - 1 else "[vout]"
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={T}:offset={cum - T - 0.05:.2f}{out}")
        prev = out
        cum += seg_durs[i] - T
    vout = TMP / "video-full.mp4"
    if not run(["ffmpeg", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[vout]",
               "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", str(vout)]):
        return 1
    print("✅ vidéo concaténée")

    # 6. mux
    final = OUT / "WildLens-IA-vivant-roughcut.mp4"
    if not run(["ffmpeg", "-y", "-i", str(vout), "-i", str(audio_mix),
                "-c:v", "copy", "-c:a", "aac", "-shortest", str(final)]):
        return 1
    print(f"✅ FINAL → {final}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
