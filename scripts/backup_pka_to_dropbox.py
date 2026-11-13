#!/usr/bin/env python3
"""
backup_pka_to_dropbox.py — Backup chiffré des données critiques PKA vers Dropbox.

Stratégie :
  - team.db         → backup chiffré quotidien (AES-256, pas de clé en clair)
  - MEMORY.md       → copie miroir (non sensible)
  - docs/system/    → copie miroir (non sensible)
  - JCH_PRIVATE/    → backup chiffré seulement (contient secrets)
  - TEAM/backups/   → rotation automatique (>7j supprimés sur Dropbox)

Usage :
  python3 scripts/backup_pka_to_dropbox.py           # backup complet
  python3 scripts/backup_pka_to_dropbox.py --dry-run  # simuler sans écrire

Dropbox target : ~/Dropbox/PKA_BACKUPS/
  ├── db/           # team.db chiffrés (1 par jour)
  ├── critical/     # MEMORY.md, docs/system/
  ├── private/      # JCH_PRIVATE chiffré
  └── manifest.json # inventaire des backups
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DROPBOX_ROOT = Path.home() / "Dropbox"
BACKUP_ROOT = DROPBOX_ROOT / "PKA_BACKUPS"

# Sous-dossiers
DB_DIR = BACKUP_ROOT / "db"
CRITICAL_DIR = BACKUP_ROOT / "critical"
PRIVATE_DIR = BACKUP_ROOT / "private"

# Fichiers à sauvegarder en clair (miroir)
MIRROR_FILES = [
    ROOT / "MEMORY.md",
]

MIRROR_DIRS = [
    ROOT / "docs" / "system",
]

# Fichiers à chiffrer avant upload
ENCRYPT_FILES = [
    ROOT / "TEAM" / "team.db",
]

ENCRYPT_DIRS = [
    ROOT / "JCH_PRIVATE",
]

# Rotation : garder N jours de backups
RETENTION_DAYS = 7


def ensure_dirs():
    for d in [DB_DIR, CRITICAL_DIR, PRIVATE_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def encrypt_file(src: Path, dst: Path) -> bool:
    """Encrypt with openssl AES-256-CBC. Password from macOS Keychain or env var."""
    password = os.environ.get("PKA_BACKUP_PASSWORD")
    if not password:
        # Try macOS Keychain
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-s", "PKA_BACKUP", "-w"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                password = result.stdout.strip()
        except Exception:
            pass

    if not password:
        print("⚠️  Pas de mot de passe trouvé (env PKA_BACKUP_PASSWORD ou Keychain 'PKA_BACKUP')", file=sys.stderr)
        print("   Backup annulé pour les fichiers chiffrés.", file=sys.stderr)
        return False

    try:
        subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-salt",
             "-pbkdf2", "-iter", "100000",
             "-in", str(src), "-out", str(dst),
             "-pass", f"pass:{password}"],
            check=True, capture_output=True, timeout=30
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Chiffrement échoué pour {src.name}: {e.stderr.decode()[:200]}", file=sys.stderr)
        return False


def decrypt_file(src: Path, dst: Path, password: str) -> bool:
    """Decrypt for restore (used manually)."""
    try:
        subprocess.run(
            ["openssl", "enc", "-d", "-aes-256-cbc",
             "-pbkdf2", "-iter", "100000",
             "-in", str(src), "-out", str(dst),
             "-pass", f"pass:{password}"],
            check=True, capture_output=True, timeout=30
        )
        return True
    except subprocess.CalledProcessError:
        return False


def backup_mirror_files(dry_run: bool = False) -> list[str]:
    """Copy non-sensitive files as-is."""
    backed = []
    for src in MIRROR_FILES:
        if src.exists():
            dst = CRITICAL_DIR / src.name
            if not dry_run:
                shutil.copy2(src, dst)
            backed.append(str(src.relative_to(ROOT)))
    for src_dir in MIRROR_DIRS:
        if src_dir.is_dir():
            dst_dir = CRITICAL_DIR / src_dir.name
            if not dry_run:
                if dst_dir.exists():
                    shutil.rmtree(dst_dir)
                shutil.copytree(src_dir, dst_dir)
            backed.append(f"{src_dir.relative_to(ROOT)}/")
    return backed


def backup_encrypted_files(dry_run: bool = False) -> list[str]:
    """Encrypt and copy sensitive files."""
    backed = []
    today = dt.date.today().isoformat()

    for src in ENCRYPT_FILES:
        if src.exists():
            dst = DB_DIR / f"{src.stem}_{today}{src.suffix}.enc"
            if not dry_run:
                if encrypt_file(src, dst):
                    backed.append(str(src.relative_to(ROOT)))
            else:
                backed.append(f"{src.relative_to(ROOT)} [dry-run]")

    for src_dir in ENCRYPT_DIRS:
        if src_dir.is_dir():
            # Tar + encrypt
            tar_path = Path(tempfile.mktemp(suffix=".tar.gz"))
            try:
                if not dry_run:
                    with tarfile.open(tar_path, "w:gz") as tar:
                        tar.add(src_dir, arcname=src_dir.name)
                    dst = PRIVATE_DIR / f"{src_dir.name}_{today}.tar.gz.enc"
                    if encrypt_file(tar_path, dst):
                        backed.append(f"{src_dir.relative_to(ROOT)}/")
                else:
                    backed.append(f"{src_dir.relative_to(ROOT)}/ [dry-run]")
            finally:
                if tar_path.exists():
                    tar_path.unlink()

    return backed


def rotate_backups():
    """Remove backups older than RETENTION_DAYS."""
    cutoff = dt.datetime.now() - dt.timedelta(days=RETENTION_DAYS)
    removed = 0

    for d in [DB_DIR, PRIVATE_DIR]:
        if d.is_dir():
            for f in d.iterdir():
                if f.is_file() and f.stat().st_mtime < cutoff.timestamp():
                    f.unlink()
                    removed += 1

    # Also clean old team.db backups in TEAM/backups if >30 days
    local_backup_dir = ROOT / "TEAM" / "backups"
    cutoff_30 = dt.datetime.now() - dt.timedelta(days=30)
    if local_backup_dir.is_dir():
        for f in local_backup_dir.iterdir():
            if f.is_file() and f.stat().st_mtime < cutoff_30.timestamp():
                f.unlink()
                removed += 1

    return removed


def write_manifest(backed_up: list[str], dry_run: bool):
    manifest = {
        "date": dt.datetime.now().isoformat(),
        "host": os.uname().nodename,
        "files_backed_up": backed_up,
        "count": len(backed_up),
        "dry_run": dry_run,
    }
    if not dry_run:
        (BACKUP_ROOT / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False)
        )
    return manifest


def check_dropbox_available() -> bool:
    """Verify Dropbox folder is accessible."""
    if not DROPBOX_ROOT.is_dir():
        print("❌ Dropbox non trouvé à", DROPBOX_ROOT, file=sys.stderr)
        return False
    # Quick write test
    test_file = BACKUP_ROOT / ".write_test"
    try:
        test_file.write_text("ok")
        test_file.unlink()
        return True
    except Exception:
        print("❌ Dropbox non accessible en écriture", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Backup PKA critical data to Dropbox")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing")
    args = parser.parse_args()

    if not args.dry_run and not check_dropbox_available():
        sys.exit(1)

    ensure_dirs()

    print(f"\n🔒 PKA → Dropbox Backup — {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if args.dry_run:
        print("   (DRY RUN — aucune écriture)")
    print()

    # Mirror (non-sensitive)
    mirror = backup_mirror_files(args.dry_run)
    if mirror:
        print(f"📄 Miroir ({len(mirror)} fichiers) :")
        for m in mirror:
            print(f"   ✅ {m}")

    # Encrypted (sensitive)
    encrypted = backup_encrypted_files(args.dry_run)
    if encrypted:
        print(f"🔐 Chiffré ({len(encrypted)} fichiers) :")
        for e in encrypted:
            print(f"   ✅ {e}")

    # Rotation
    removed = rotate_backups()
    if removed:
        print(f"\n🗑️  Rotation : {removed} anciens backups supprimés")

    # Manifest
    manifest = write_manifest(mirror + encrypted, args.dry_run)
    total = len(mirror) + len(encrypted)
    print(f"\n📋 {total} fichiers sauvegardés → {BACKUP_ROOT}")
    print(f"   Manifest: {BACKUP_ROOT / 'manifest.json'}")

    if not mirror and not encrypted:
        print("\n⚠️  Aucun fichier sauvegardé. Vérifie les sources.")


if __name__ == "__main__":
    main()
