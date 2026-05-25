from pathlib import Path


PKA_DIR = Path(__file__).resolve().parents[1]


def test_pka_save_shortcut_launches_interactive_save():
    shortcut = PKA_DIR / "bin" / "pka-save"

    assert shortcut.exists()
    assert shortcut.stat().st_mode & 0o111

    content = shortcut.read_text(encoding="utf-8")
    assert "scripts/pka_save.py" in content
    assert "--interactive" in content


def test_pka_shortcut_is_short_alias_for_pka_save():
    shortcut = PKA_DIR / "bin" / "pka"

    assert shortcut.exists()
    assert shortcut.stat().st_mode & 0o111

    content = shortcut.read_text(encoding="utf-8")
    assert 'exec "$PKA_DIR/bin/pka-save"' in content
