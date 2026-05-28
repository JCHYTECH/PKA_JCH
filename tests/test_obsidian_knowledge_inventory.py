from pathlib import Path

from scripts.obsidian_knowledge_inventory import (
    build_inventory,
    propose_wikilinks,
    render_wikilink_dry_run,
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
    # All previously ambiguous terms resolved by JCH on 2026-05-25.
    # When AMBIGUOUS_TERMS is empty, review_queue shows no ambiguous candidates.
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nClaude and Dobby.")
    write(tmp_path / "JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/docs/ai.md", "# AI\n\nClaude and ChatGPT.")

    inventory = build_inventory(tmp_path)
    review_queue = render_review_queue(inventory)

    assert "# Review Queue" in review_queue
    assert "No ambiguous candidates detected." in review_queue


def test_dictionary_prefers_team_folder_for_agents(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nDobby profile.")
    write(tmp_path / "wiki/Daily/2026/05/2026-05-25.md", "# Daily\n\nDobby worked on Obsidian.")
    write(tmp_path / "wiki/Daily/2026/05/2026-05-26.md", "# Daily\n\nDobby worked on WildNexus.")
    write(tmp_path / "wiki/Daily/2026/05/2026-05-27.md", "# Daily\n\nDobby worked on PKA.")

    inventory = build_inventory(tmp_path)
    dictionary = render_knowledge_dictionary(inventory)

    assert "## Dobby" in dictionary
    assert "- folder: `TEAM`" in dictionary


def test_generated_inventory_files_are_not_scanned(tmp_path):
    write(
        tmp_path / "JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph/indexes/technology_index.md",
        "# Technology Index\n\nGraphify should not count from generated output.",
    )
    write(
        tmp_path / "JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph/knowledge_dictionary.md",
        "# Knowledge Dictionary\n\nGraphify should not count from generated output.",
    )

    inventory = build_inventory(tmp_path)

    assert inventory.notes == []
    assert "Graphify" not in inventory.technologies


def test_wikilink_dry_run_limits_files_and_skips_ambiguous_terms(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nDobby profile.")
    write(tmp_path / "TEAM/claude.md", "# Claude\n\nClaude profile.")
    for index in range(1, 7):
        write(
            tmp_path / f"notes/note-{index}.md",
            f"# Note {index}\n\nDobby uses Obsidian and Claude here.",
        )

    inventory = build_inventory(tmp_path)
    suggestions = propose_wikilinks(inventory, max_files=5)
    report = render_wikilink_dry_run(inventory, suggestions, max_files=5)

    assert len({suggestion.note_path for suggestion in suggestions}) == 5
    assert "notes/note-6.md" not in report
    # Claude is now linkable (resolved from ambiguous by JCH on 2026-05-25)
    assert "[[Dobby]] uses [[Obsidian]] and [[Claude]] here." in report


def test_wikilink_dry_run_keeps_existing_links_untouched(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nDobby profile.")
    write(tmp_path / "notes/linked.md", "# Linked\n\n[[Dobby]] uses Obsidian.")

    inventory = build_inventory(tmp_path)
    suggestions = propose_wikilinks(inventory, max_files=5)
    report = render_wikilink_dry_run(inventory, suggestions, max_files=5)

    assert "[[Dobby]] uses [[Obsidian]]." in report
    assert "[[[[Dobby]]]]" not in report


def test_wikilink_dry_run_skips_inline_code_and_root_pointer_files(tmp_path):
    write(tmp_path / "ADAPTER-PROMPT.md", "# Prompt\n\nDobby uses Obsidian.")
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nDobby profile.")
    write(tmp_path / "notes/code.md", "# Code\n\nRead `TEAM/dobby.md` before Obsidian.")

    inventory = build_inventory(tmp_path)
    suggestions = propose_wikilinks(inventory, max_files=5)
    report = render_wikilink_dry_run(inventory, suggestions, max_files=5)

    assert "ADAPTER-PROMPT.md" not in report
    assert "`TEAM/dobby.md` before [[Obsidian]]." in report
    assert "`TEAM/[[Dobby]].md`" not in report


def test_wikilink_dry_run_skips_markdown_link_syntax(tmp_path):
    write(tmp_path / "TEAM/dobby.md", "# Dobby\n\nDobby profile.")
    write(tmp_path / "notes/dash.md", "# Dash\n\n| [Modeles Dobby](modeles.html) |\n| [02_ARTEON](../03_PROJECTS/02_ARTEON/INDEX.md) |")

    inventory = build_inventory(tmp_path)
    suggestions = propose_wikilinks(inventory, max_files=5)
    report = render_wikilink_dry_run(inventory, suggestions, max_files=5)

    # Dobby should NOT be wikilinked inside markdown link syntax [text](url)
    assert "[Modeles [[Dobby]]](modeles.html)" not in report
    assert "[[[02_ARTEON]]]" not in report
    assert "[02_ARTEON](../03_PROJECTS/[[02_ARTEON]]/INDEX.md)" not in report
