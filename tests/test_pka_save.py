from datetime import datetime

from scripts import pka_save


def test_build_section_includes_model_and_project_metadata():
    section = pka_save.build_section(
        datetime(2026, 5, 24, 14, 30),
        "session-test",
        "Résumé court.",
        "- Action",
        "- Décision",
        "- Suite",
        model="codex",
        project="WILDNEXUS",
    )

    assert "### Contexte" in section
    assert "- Modèle : codex" in section
    assert "- Projet : WILDNEXUS" in section
    assert "### Résumé\nRésumé court." in section
