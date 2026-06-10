# n8n Mail Ingest Pilot Design

Date: 2026-06-10
Owner: [[Dobby]]
Specialists: [[Pie]], [[Forge]], [[Castor]]

## Goal

Use n8n as a visible trigger layer for incoming mail from Gmail principal and Outlook JCHYTECH, while keeping PKA_JCH as the authority for intelligence, routing, storage, and audit.

The pilot must prove one narrow workflow:

1. A new mail arrives in Gmail principal or Outlook JCHYTECH.
2. n8n detects the event and applies only a light pre-filter.
3. n8n writes a normalized markdown file to a Dropbox-synced PKA landing folder.
4. The local PKA inbox flow imports that file under `JCH_Inbox/00_INBOX/email_imports/`.
5. [[Dobby]] and [[Pie]] can process the resulting intake file using existing PKA rules.

## Non-Goals

- n8n does not replace `email_digest.py`, `gmail_gatekeeper.py`, or `outlook_gatekeeper.py`.
- n8n does not become the source of truth for mail classification.
- n8n does not store long-term mail archives.
- n8n does not perform specialist routing beyond source tagging and obvious spam suppression in this pilot.
- The pilot does not auto-delete, archive, move, or label source mailbox messages.

## Existing Context

PKA already has local mail logic:

- `scripts/gmail_gatekeeper.py`: strict Gmail gatekeeper for the Dobby mailbox, with whitelist and explicit-user-processing semantics.
- `scripts/email_digest.py`: Gmail digest, scoring, contacts lookup, Pie analysis, project labels, and routing.
- `scripts/outlook_gatekeeper.py`: Microsoft Graph unread-mail processing for Outlook/JCHYTECH.

The n8n pilot should orchestrate these systems without duplicating their internal judgment.

## Architecture

There are two n8n workflows:

1. `PKA Mail Ingest - Gmail Principal`
2. `PKA Mail Ingest - Outlook JCHYTECH`

Each workflow follows the same structure:

1. Mail trigger receives a new-message event.
2. n8n extracts stable metadata:
   - source
   - provider message id
   - thread/conversation id when available
   - received date
   - sender name
   - sender email
   - subject
   - body preview or bounded body text
   - attachment metadata only
3. n8n applies a conservative pre-filter:
   - skip obvious no-reply/newsletter/promotional patterns
   - never delete or mutate mailbox state
4. n8n writes the normalized markdown file to a Dropbox-synced landing folder watched by PKA.
5. PKA imports the markdown file and records enough metadata for later deduplication.

## Intake File Format

Files are written to:

`JCH_Inbox/00_INBOX/email_imports/`

Filename pattern:

`YYYY-MM-DD_<source>_<sender-slug>_<subject-slug>.md`

Minimum content:

```markdown
# Email importé

**Source :** gmail-principal | outlook-jchytech
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

## Data Boundaries

The first pilot stores only a bounded body preview or bounded plain-text body. Attachments are not downloaded by default. Attachment metadata may be captured so [[Dobby]] can decide whether to fetch them later.

No credentials, OAuth tokens, webhook secrets, or source mailbox secrets are written into the workspace. Secrets remain in n8n credentials or local secret storage.

## Deduplication

The PKA intake layer must treat `(source, provider_message_id)` as the natural deduplication key.

If the same mail event arrives twice, PKA should not create duplicate markdown files. It may update a local state file under `_local/` or `tmp/`, but canonical project files should receive only one intake note per message.

## Error Handling

If Dropbox write fails, n8n should keep the workflow execution error visible and retry according to n8n defaults or a small bounded retry policy.

If an imported markdown file is malformed, PKA should reject it without moving it into the canonical inbox path.

If source metadata is missing, PKA should still accept the mail only when source, sender, subject, and received date are present.

## Testing

Pilot acceptance requires:

1. One Gmail principal test mail creates exactly one markdown intake file.
2. One Outlook JCHYTECH test mail creates exactly one markdown intake file.
3. Replaying the same payload does not create a duplicate.
4. A promotional/no-reply test message is skipped or marked as low priority without mailbox mutation.
5. No secrets appear in generated markdown, logs, or git diff.

## Rollout

Phase 1 is manual and visible:

1. Configure both n8n workflows.
2. Send one controlled test mail to Gmail principal.
3. Send one controlled test mail to Outlook JCHYTECH.
4. Inspect generated markdown files in the Dropbox landing folder and then in `JCH_Inbox/00_INBOX/email_imports/`.
5. Let [[Dobby]] and [[Pie]] process those files through the existing inbox flow.

Only after this pilot is validated should n8n trigger automatic specialist routing or Plane task creation.

## Implementation Decisions

- PKA intake uses a file drop through Dropbox or the existing synchronized landing mechanism, not a public local HTTP endpoint.
- Gmail principal uses metadata plus bounded body preview for the first run.
- Outlook JCHYTECH uses n8n Microsoft credentials for event detection; local PKA Microsoft Graph credentials remain available for later deep processing if needed.
