from pathlib import Path

from scripts.obsidian_knowledge_inventory import (
    build_inventory,
    render_agent_index,
    render_knowledge_dictionary,
    render_note_index,
    render_project_index,
    render_review_queue,
    render_technology_index,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_inventory_extracts_frontmatter_title_tags_and_aliases(tmp_path):
    write(
        tmp_path / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/INDEX.md",
        """---
type: project
status: active
aliases:
  - WildNexus P0
tags: [wildnexus, hardware]
---

# WildNexus

WildNexus uses ESP32-S3 and LoRa.
""",
    )

    inventory = build_inventory(tmp_path)

    assert len(inventory.notes) == 1
    note = inventory.notes[0]
    assert note.title == "WildNexus"
    assert note.note_type == "project"
    assert note.status == "active"
    assert note.aliases == ["WildNexus P0"]
    assert note.tags == ["wildnexus", "hardware"]
    assert note.path == Path("JCH_Inbox/03_PROJECTS/03_WILDNEXUS/INDEX.md")


def test_inventory_classifies_projects_agents_and_technologies(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nRole: Orchestrator")
    write(tmp_path / "TEAM/ROSTER.md", "# Team Roster\n\n| Dobby | Orchestrator |")
    write(
        tmp_path / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/Start.md",
        "# WildNexus Start\n\nESP32-S3, LoRa, Raspberry Pi 5, BirdNET and Tailscale.",
    )
    write(
        tmp_path / "JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/docs/graphify-workflow-jch.md",
        "# Graphify Workflow\n\nObsidian, Graphify, Claude and ChatGPT.",
    )

    inventory = build_inventory(tmp_path)

    assert "03_WILDNEXUS" in inventory.projects
    assert "01_AI_IT_TOOLS" in inventory.projects
    assert "Dobby" in inventory.agents
    assert "ESP32-S3" in inventory.technologies
    assert "LoRa" in inventory.technologies
    assert "Obsidian" in inventory.technologies


def test_renderers_create_expected_sections(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nDobby and Obsidian.")
    write(tmp_path / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/Start.md", "# WildNexus\n\nESP32-S3 and LoRa.")

    inventory = build_inventory(tmp_path)

    assert "# Note Index" in render_note_index(inventory)
    assert "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/Start.md" in render_note_index(inventory)
    assert "# Project Index" in render_project_index(inventory)
    assert "03_WILDNEXUS" in render_project_index(inventory)
    assert "# Agent Index" in render_agent_index(inventory)
    assert "Dobby" in render_agent_index(inventory)
    assert "# Technology Index" in render_technology_index(inventory)
    assert "ESP32-S3" in render_technology_index(inventory)
    assert "# Knowledge Dictionary" in render_knowledge_dictionary(inventory)
    assert "canonical: ESP32-S3" in render_knowledge_dictionary(inventory)


def test_review_queue_flags_ambiguous_aliases(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nClaude and Dobby.")
    write(tmp_path / "JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/docs/ai.md", "# AI\n\nClaude and ChatGPT.")

    inventory = build_inventory(tmp_path)
    review_queue = render_review_queue(inventory)

    assert "# Review Queue" in review_queue
    assert "Claude" in review_queue
    assert "Ambiguous runtime or model reference" in review_queue
