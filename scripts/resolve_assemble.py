#!/usr/bin/env python3
"""
resolve_assemble.py — Pilote DaVinci Resolve via l'API de scripting.

Étape 1 : connecte, crée le projet, importe les médias, crée la timeline
avec la voix off (9 MP3) dans l'ordre sur A1.

Usage : python3 scripts/resolve_assemble.py
"""

from __future__ import annotations

import sys
from pathlib import Path

MODULES = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
sys.path.append(MODULES)

import DaVinciResolveScript as dvr  # noqa: E402

VIDEO = Path("/Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/02_ARTEON/wildlens/video")
VO = sorted((VIDEO / "vo").glob("scene-*.mp3"))          # 9
CLIPS = sorted((VIDEO / "clips").glob("*.mp4"))          # 3
ASSETS = sorted((VIDEO / "assets").glob("*"))            # 10 images


def main() -> int:
    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        print("❌ Impossible de se connecter à Resolve (l'app est-elle ouverte ?)")
        return 1
    print(f"✅ Connecté : {resolve.GetProductName()} {resolve.GetVersionString()}")

    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if project is None:
        project = pm.CreateProject("WildLens-IA-vivant")
        print("✅ Projet créé : WildLens-IA-vivant")
    else:
        print(f"✅ Projet courant : {project.GetName()}")
    if project is None:
        print("❌ Pas de projet")
        return 1

    mp = project.GetMediaPool()
    media = [str(p) for p in VO + CLIPS + ASSETS]
    ok = mp.ImportMedia(media)
    print(f"✅ Import de {len(media)} médias : {'OK' if ok else 'partiel'}")

    clips = mp.GetRootFolder().GetClipList()
    print(f"   {len(clips)} clips dans le Media Pool")

    # Timeline : voix off dans l'ordre sur A1
    vo_clips = [c for c in clips if c.GetName().startswith("scene-")]
    vo_clips.sort(key=lambda c: c.GetName())
    tl = mp.CreateTimelineFromClips("WildLens-IA-vivant", vo_clips)
    if tl is not None:
        project.SetCurrentTimeline(tl)
        print(f"✅ Timeline créée : {tl.GetName()} — voix off posée sur A1")
        items = tl.GetItemListInTrack("audio", 1)
        print(f"   {len(items)} clips audio sur A1")
    else:
        print("⚠️  Timeline non créée (les clips audio sont-ils bien importés ?)")
        return 1

    # Ajoute une piste vidéo V1 pour les visuels
    tl.AddTrack("video", 1)
    print("✅ Piste vidéo V1 ajoutée")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
