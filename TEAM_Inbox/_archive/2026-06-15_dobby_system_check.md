# PKA System Check

_Generated: 2026-06-15T20:25:48_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `GREEN`
- Pointer generation drift: `GREEN`
- File placement drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` _local/homeassistant/home-assistant.log: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/certifi/cacert.pem: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/pip/_vendor/packaging/_tokenizer.py: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/pip/_vendor/pygments/token.py: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/pip/_vendor/certifi/cacert.pem: mode 0644, expected 0600 or stricter
- `high` `permissions` JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/logs/collector.log: mode 0644, expected 0600 or stricter

