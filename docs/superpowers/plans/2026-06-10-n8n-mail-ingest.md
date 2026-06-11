# n8n Mail Ingest Implementation Plan

> **For agentic workers:** REQUIRED SUB-[[SKILL]]: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local PKA intake path for n8n-created mail markdown files from Gmail principal and Outlook JCHYTECH.

**Architecture:** n8n Cloud writes normalized mail markdown files into a Dropbox-synced landing folder. A local Python importer validates, deduplicates, sanitizes filenames, and moves [[accepted]] files into `JCH_Inbox/00_INBOX/email_imports/`. Existing PKA mail intelligence remains in `email_digest.py`, `gmail_gatekeeper.py`, `outlook_gatekeeper.py`, and later [[Pie]] processing.

**Tech Stack:** Python 3 standard library, pytest, Markdown files, Dropbox-synced file drop, n8n Gmail and Microsoft Outlook triggers.

---

## File Structure

- Create `scripts/n8n_mail_ingest.py`: local importer CLI and reusable functions.
- Create `tests/test_n8n_mail_ingest.py`: unit tests for validation, deduplication, filename sanitization, and promotional filtering.
- Create `docs/system/n8n-mail-ingest.md`: operator notes for the two n8n workflows.
- Use `_local/n8n_mail_ingest_state.json`: runtime deduplication state, not committed.
- Use `_local/n8n-mail-drop/`: default local test landing folder, not committed.
- Use `JCH_Inbox/00_INBOX/email_imports/`: canonical [[accepted]] intake folder.

## Task 1: Add Failing Tests For The Local Importer

**Files:**
- Create: `tests/test_n8n_mail_ingest.py`
- Later create: `scripts/n8n_mail_ingest.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_n8n_mail_ingest.py` with this content:

```python
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.n8n_mail_ingest import (
    ImportResult,
    import_drop_dir,
    parse_mail_markdown,
    should_skip_promotional,
    slugify,
)


VALID_MAIL = """# Email importé

**Source :** gmail-principal
**Provider message id :** msg-123
**Thread/conversation id :** thread-456
**Date reçue :** 2026-06-10T09:30:00+02:00
**De :** Jean Dupont <jean@example.com>
**Objet :** Contrat Vetalyx
**Statut :** à trier

---

## Aperçu

Bonjour Jean-Claude, voici le document à relire.

## Pièces jointes

- contrat.pdf, application/pdf, 120000

## Voir aussi

- [[Dobby]]
- [[Pie]]
"""


def test_parse_mail_markdown_extracts_required_fields():
    parsed = parse_mail_markdown(VALID_MAIL)

    assert parsed.source == "gmail-principal"
    assert parsed.provider_message_id == "msg-123"
    assert parsed.thread_id == "thread-456"
    assert parsed.received_at == "2026-06-10T09:30:00+02:00"
    assert parsed.sender == "Jean Dupont <jean@example.com>"
    assert parsed.subject == "Contrat Vetalyx"


def test_parse_mail_markdown_rejects_missing_required_field():
    broken = VALID_MAIL.replace("**Provider message id :** msg-123\n", "")

    with pytest.raises(ValueError, match="Provider message id"):
        parse_mail_markdown(broken)


def test_slugify_keeps_filename_short_and_ascii_safe():
    value = slugify("Jean Dupont / Contrat Vétalyx très urgent !!!", max_length=32)

    assert value == "jean-dupont-contrat-vetalyx"
    assert len(value) <= 32


def test_should_skip_promotional_matches_obvious_newsletter():
    parsed = parse_mail_markdown(
        VALID_MAIL.replace("Jean Dupont <jean@example.com>", "Newsletter <news@example.com>")
        .replace("Contrat Vetalyx", "Unsubscribe - promotion exclusive")
    )

    assert should_skip_promotional(parsed) is True


def test_import_drop_dir_moves_valid_mail_and_deduplicates(tmp_path: Path):
    drop_dir = tmp_path / "drop"
    inbox_dir = tmp_path / "JCH_Inbox" / "00_INBOX" / "email_imports"
    state_file = tmp_path / "_local" / "n8n_mail_ingest_state.json"
    drop_dir.mkdir(parents=True)

    source_file = drop_dir / "gmail-msg.md"
    source_file.write_text(VALID_MAIL, encoding="utf-8")

    first = import_drop_dir(drop_dir, inbox_dir, state_file)
    second = import_drop_dir(drop_dir, inbox_dir, state_file)

    assert first == [
        ImportResult(
            source="gmail-principal",
            provider_message_id="msg-123",
            status="imported",
            output_path=inbox_dir / "2026-06-10_gmail-principal_jean-dupont_contrat-vetalyx.md",
            reason="accepted",
        )
    ]
    assert second == []
    assert not source_file.exists()
    assert first[0].output_path.exists()

    state = json.loads(state_file.read_text(encoding="utf-8"))
    assert state["seen"] == ["gmail-principal:msg-123"]


def test_import_drop_dir_rejects_malformed_without_moving_to_inbox(tmp_path: Path):
    drop_dir = tmp_path / "drop"
    inbox_dir = tmp_path / "inbox"
    state_file = tmp_path / "state.json"
    drop_dir.mkdir()
    bad_file = drop_dir / "bad.md"
    bad_file.write_text("# Email importé\n\n**Source :** gmail-principal\n", encoding="utf-8")

    results = import_drop_dir(drop_dir, inbox_dir, state_file)

    assert len(results) == 1
    assert results[0].status == "rejected"
    assert "Provider message id" in results[0].reason
    assert bad_file.exists()
    assert not inbox_dir.exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
pytest tests/test_n8n_mail_ingest.py -v
```

Expected: FAIL during import with `ModuleNotFoundError: No module named 'scripts.n8n_mail_ingest'`.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/test_n8n_mail_ingest.py
git commit -m "test: specify n8n mail ingest importer"
```

## Task 2: Implement The Local Importer

**Files:**
- Create: `scripts/n8n_mail_ingest.py`
- Test: `tests/test_n8n_mail_ingest.py`

- [ ] **Step 1: Create the importer**

Create `scripts/n8n_mail_ingest.py` with this content:

```python
#!/usr/bin/env python3
"""Import n8n-created mail markdown files into the PKA inbox.

Model: GPT-5 (2026-06-10, n8n mail ingest pilot)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DROP_DIR = ROOT / "_local" / "n8n-mail-drop"
DEFAULT_INBOX_DIR = ROOT / "JCH_Inbox" / "00_INBOX" / "email_imports"
DEFAULT_STATE_FILE = ROOT / "_local" / "n8n_mail_ingest_state.json"
REQUIRED_FIELDS = {
    "Source": "source",
    "Provider message id": "provider_message_id",
    "Date reçue": "received_at",
    "De": "sender",
    "Objet": "subject",
}
PROMOTIONAL_PATTERNS = (
    "unsubscribe",
    "newsletter",
    "promotion",
    "promo",
    "offre exclusive",
    "soldes",
    "discount",
    "no-reply",
    "noreply",
)


@dataclass(frozen=True)
class MailIntake:
    source: str
    provider_message_id: str
    thread_id: str
    received_at: str
    sender: str
    subject: str
    content: str


@dataclass(frozen=True)
class ImportResult:
    source: str
    provider_message_id: str
    status: str
    output_path: Path | None
    reason: str


def slugify(value: str, max_length: int = 48) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    if not slug:
        return "unknown"
    return slug[:max_length].rstrip("-")


def _field_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"^\*\*{re.escape(label)}\s*:\*\*\s*(.+?)\s*$", re.MULTILINE)


def _extract_field(content: str, label: str) -> str:
    match = _field_pattern(label).search(content)
    if not match:
        raise ValueError(f"Missing required field: {label}")
    value = match.group(1).strip()
    if not value:
        raise ValueError(f"Empty required field: {label}")
    return value


def parse_mail_markdown(content: str) -> MailIntake:
    values = {
        attr: _extract_field(content, label)
        for label, attr in REQUIRED_FIELDS.items()
    }
    thread_match = _field_pattern("Thread/conversation id").search(content)
    thread_id = thread_match.group(1).strip() if thread_match else ""
    return MailIntake(
        source=values["source"],
        provider_message_id=values["provider_message_id"],
        thread_id=thread_id,
        received_at=values["received_at"],
        sender=values["sender"],
        subject=values["subject"],
        content=content,
    )


def should_skip_promotional(mail: MailIntake) -> bool:
    haystack = f"{mail.sender}\n{mail.subject}".lower()
    return any(pattern in haystack for pattern in PROMOTIONAL_PATTERNS)


def load_state(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("seen", []))


def save_state(path: Path, seen: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"seen": sorted(seen)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def dedupe_key(mail: MailIntake) -> str:
    return f"{mail.source}:{mail.provider_message_id}"


def output_filename(mail: MailIntake) -> str:
    date_part = mail.received_at[:10]
    try:
        datetime.fromisoformat(mail.received_at.replace("Z", "+00:00"))
    except ValueError:
        date_part = datetime.now().strftime("%Y-%m-%d")
    sender_name = mail.sender.split("<", 1)[0].strip() or mail.sender
    return (
        f"{date_part}_"
        f"{slugify(mail.source, 32)}_"
        f"{slugify(sender_name, 32)}_"
        f"{slugify(mail.subject, 48)}.md"
    )


def import_file(source_path: Path, inbox_dir: Path, seen: set[str]) -> ImportResult:
    try:
        mail = parse_mail_markdown(source_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return ImportResult(
            source="unknown",
            provider_message_id="unknown",
            status="rejected",
            output_path=None,
            reason=str(exc),
        )

    key = dedupe_key(mail)
    if key in seen:
        source_path.unlink()
        return ImportResult(mail.source, mail.provider_message_id, "duplicate", None, "already seen")

    if should_skip_promotional(mail):
        source_path.unlink()
        seen.add(key)
        return ImportResult(mail.source, mail.provider_message_id, "skipped", None, "promotional")

    inbox_dir.mkdir(parents=True, exist_ok=True)
    output_path = inbox_dir / output_filename(mail)
    if output_path.exists():
        output_path = inbox_dir / f"{output_path.stem}-{slugify(mail.provider_message_id, 16)}.md"
    shutil.move(str(source_path), output_path)
    seen.add(key)
    return ImportResult(mail.source, mail.provider_message_id, "imported", output_path, "accepted")


def import_drop_dir(drop_dir: Path, inbox_dir: Path, state_file: Path) -> list[ImportResult]:
    if not drop_dir.exists():
        return []
    seen = load_state(state_file)
    results: list[ImportResult] = []
    for source_path in sorted(drop_dir.glob("*.md")):
        result = import_file(source_path, inbox_dir, seen)
        if result.status != "duplicate":
            results.append(result)
    save_state(state_file, seen)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Import n8n mail markdown drops into PKA inbox")
    parser.add_argument("--drop-dir", type=Path, default=DEFAULT_DROP_DIR)
    parser.add_argument("--inbox-dir", type=Path, default=DEFAULT_INBOX_DIR)
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE)
    args = parser.parse_args()

    results = import_drop_dir(args.drop_dir, args.inbox_dir, args.state_file)
    for result in results:
        output = result.output_path.as_posix() if result.output_path else "-"
        print(f"{result.status}\t{result.source}\t{result.provider_message_id}\t{output}\t{result.reason}")
    return 1 if any(result.status == "rejected" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run importer tests**

Run:

```bash
pytest tests/test_n8n_mail_ingest.py -v
```

Expected: PASS, 6 tests passed.

- [ ] **Step 3: Commit importer**

```bash
git add scripts/n8n_mail_ingest.py tests/test_n8n_mail_ingest.py
git commit -m "feat: import n8n mail drops into inbox"
```

## Task 3: Add Operator Documentation For n8n

**Files:**
- Create: `docs/system/n8n-mail-ingest.md`

- [ ] **Step 1: Write the operator notes**

Create `docs/system/n8n-mail-ingest.md` with this content:

```markdown
# n8n Mail Ingest

Date: 2026-06-10
Owner: [[Dobby]]
Specialists: [[Pie]], [[Forge]], [[Castor]]

## Purpose

n8n detects new mail from Gmail principal and Outlook JCHYTECH, creates normalized markdown files, and drops them into a synchronized landing folder. PKA imports those files locally through `scripts/n8n_mail_ingest.py`.

## Boundaries

- n8n is the trigger and transport layer.
- PKA is the intelligence, archive, deduplication, and routing layer.
- n8n must not delete, archive, move, or label source mailbox messages during the pilot.
- n8n must not store OAuth tokens, webhook secrets, or mailbox secrets in markdown output.

## Local Import Command

```bash
python3 scripts/n8n_mail_ingest.py \
  --drop-dir _local/n8n-mail-drop \
  --[[inbox]]-dir JCH_Inbox/00_INBOX/email_imports \
  --state-file _local/n8n_mail_ingest_state.json
```

## Workflow 1: PKA Mail Ingest - Gmail Principal

Nodes:

1. Gmail Trigger
   - Event: new email
   - Mailbox: Gmail principal
   - Body mode: preview or bounded plain text
   - Attachments: metadata only
2. IF Filter
   - Continue only when sender and subject do not contain obvious promotional patterns:
     - `unsubscribe`
     - `newsletter`
     - `promotion`
     - `promo`
     - `discount`
     - `no-reply`
     - `noreply`
3. Markdown Builder
   - Build the exact markdown shape documented below.
4. Dropbox File Create
   - Folder: synchronized PKA n8n mail drop folder
   - Filename: `{{$now.format('yyyy-MM-dd')}}_gmail-principal_{{$json.id}}.md`

## Workflow 2: PKA Mail Ingest - Outlook JCHYTECH

Nodes:

1. Microsoft Outlook Trigger
   - Event: new email
   - Mailbox: JCHYTECH
   - Body mode: preview or bounded plain text
   - Attachments: metadata only
2. IF Filter
   - Same promotional filter as Gmail.
3. Markdown Builder
   - Build the exact markdown shape documented below.
4. Dropbox File Create
   - Folder: synchronized PKA n8n mail drop folder
   - Filename: `{{$now.format('yyyy-MM-dd')}}_outlook-jchytech_{{$json.id}}.md`

## Markdown Shape

```markdown
# Email importé

**Source :** gmail-principal
**Provider message id :** `<provider_message_id>`
**Thread/conversation id :** `<thread_or_conversation_id>`
**Date reçue :** `<received_at>`
**De :** Sender Name <sender@example.com>
**Objet :** `<subject>`
**Statut :** à trier

---

## Aperçu

`<bounded_plain_text_preview>`

## Pièces jointes

- Nom, type, taille si disponible

## Voir aussi

- [[Dobby]]
- [[Pie]]
```

For Outlook, set `Source` to `outlook-jchytech`.

## Verification

1. Send one controlled Gmail principal test mail.
2. Confirm one markdown file appears in the synchronized drop folder.
3. Run the local import command.
4. Confirm one file appears in `JCH_Inbox/00_INBOX/email_imports/`.
5. Run the local import command again.
6. Confirm no duplicate file is created.
7. Repeat the same sequence for Outlook JCHYTECH.
```

- [ ] **Step 2: Commit documentation**

```bash
git add docs/system/n8n-mail-ingest.md
git commit -m "docs: document n8n mail ingest workflows"
```

## Task 4: Add Local Manual Verification Fixtures

**Files:**
- Create: `_local/n8n-mail-drop/` during verification only
- Modify: no committed source files expected

- [ ] **Step 1: Create a local Gmail fixture**

Run:

```bash
mkdir -p _local/n8n-mail-drop
cat > _local/n8n-mail-drop/gmail-test.md <<'EOF'
# Email importé

**Source :** gmail-principal
**Provider message id :** local-gmail-001
**Thread/conversation id :** local-thread-001
**Date reçue :** 2026-06-10T10:00:00+02:00
**De :** Test Gmail <test.gmail@example.com>
**Objet :** Test n8n Gmail
**Statut :** à trier

---

## Aperçu

Message de test local pour le pipeline n8n Gmail.

## Pièces jointes

- Aucun

## Voir aussi

- [[Dobby]]
- [[Pie]]
EOF
```

- [ ] **Step 2: Run local import**

Run:

```bash
python3 scripts/n8n_mail_ingest.py \
  --drop-dir _local/n8n-mail-drop \
  --inbox-dir /tmp/pka-n8n-mail-test/inbox \
  --state-file /tmp/pka-n8n-mail-test/state.json
```

Expected output contains:

```text
imported	gmail-principal	local-gmail-001
```

- [ ] **Step 3: Verify deduplication**

Run the same command again:

```bash
python3 scripts/n8n_mail_ingest.py \
  --drop-dir _local/n8n-mail-drop \
  --inbox-dir /tmp/pka-n8n-mail-test/inbox \
  --state-file /tmp/pka-n8n-mail-test/state.json
```

Expected: no output, because the first run moved the fixture and recorded the dedupe key.

## Task 5: Configure n8n Workflows Manually

**Files:**
- Modify in n8n Cloud UI: `PKA Mail Ingest - Gmail Principal`
- Modify in n8n Cloud UI: `PKA Mail Ingest - Outlook JCHYTECH`
- No repo file changes required unless exporting workflow JSON later.

- [ ] **Step 1: Create the Gmail workflow in n8n**

In n8n Cloud, create workflow `PKA Mail Ingest - Gmail Principal`:

```text
Gmail Trigger
IF promotional filter
Set markdown fields
Dropbox create file
```

Use this exact `Source` field:

```text
gmail-principal
```

- [ ] **Step 2: Create the Outlook workflow in n8n**

In n8n Cloud, create workflow `PKA Mail Ingest - Outlook JCHYTECH`:

```text
Microsoft Outlook Trigger
IF promotional filter
Set markdown fields
Dropbox create file
```

Use this exact `Source` field:

```text
outlook-jchytech
```

- [ ] **Step 3: Keep both workflows inactive until credentials and Dropbox target are verified**

Expected: both workflows exist in n8n and are visible, but not yet running continuously.

## Task 6: End-To-End Pilot

**Files:**
- Runtime output: `JCH_Inbox/00_INBOX/email_imports/*.md`
- Runtime state: `_local/n8n_mail_ingest_state.json`
- No source files should change during this task.

- [ ] **Step 1: Send controlled Gmail test mail**

Send a Gmail principal test message with subject:

```text
Test n8n Gmail PKA
```

Expected: n8n creates one markdown file in the synchronized drop folder.

- [ ] **Step 2: Run local importer into canonical [[inbox]]**

Run:

```bash
python3 scripts/n8n_mail_ingest.py
```

Expected output contains:

```text
imported	gmail-principal
```

- [ ] **Step 3: Send controlled Outlook JCHYTECH test mail**

Send an Outlook JCHYTECH test message with subject:

```text
Test n8n Outlook PKA
```

Expected: n8n creates one markdown file in the synchronized drop folder.

- [ ] **Step 4: Run local importer again**

Run:

```bash
python3 scripts/n8n_mail_ingest.py
```

Expected output contains:

```text
imported	outlook-jchytech
```

- [ ] **Step 5: Verify no secrets in generated files**

Run:

```bash
rg -n "token|secret|authorization|bearer|refresh_token|client_secret" JCH_Inbox/00_INBOX/email_imports _local/n8n_mail_ingest_state.json
```

Expected: no matches.

- [ ] **Step 6: Commit implementation docs if only planned source files changed**

Run:

```bash
git status --short
```

Expected: no unexpected source changes. Runtime files under `_local/` may be untracked and should not be committed.

## Self-Review

Spec coverage:

- Gmail principal and Outlook JCHYTECH are covered by Task 5 and Task 6.
- Dropbox-synced file-drop architecture is covered by Task 2, Task 3, and Task 5.
- Validation, deduplication, bounded storage, and promotional skipping are covered by Task 1 and Task 2.
- Acceptance tests from the spec are covered by Task 1, Task 4, and Task 6.
- Non-goals are preserved because no source mailbox mutation is planned.

Placeholder scan:

- No unfinished placeholder steps are used.
- Each code-writing step includes complete file content.

Type consistency:

- `MailIntake`, `ImportResult`, `parse_mail_markdown`, `should_skip_promotional`, `slugify`, and `import_drop_dir` are defined in Task 2 and used consistently by Task 1.
