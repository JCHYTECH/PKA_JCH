---
type: dashboard
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - dashboard
owner: "[[Dobby]]"
project: PKA_JCH
---

# Dashboard PKA

## Inbox

```dataview
TABLE type, status, dateCreated, project
FROM "JCH_Inbox/00_INBOX"
SORT file.mtime DESC
```

## Daily recentes

```dataview
TABLE dateCreated, status, owner
FROM "wiki/Daily"
SORT file.mtime DESC
LIMIT 15
```

## Notes en review

```dataview
TABLE type, owner, project, file.mtime AS modified
WHERE status = "review"
SORT file.mtime DESC
```

## Notes actives

```dataview
TABLE type, owner, project, file.mtime AS modified
WHERE status = "active"
SORT file.mtime DESC
LIMIT 30
```

## Notes sans type

```dataview
TABLE file.folder, file.mtime AS modified
WHERE !type
SORT file.mtime DESC
LIMIT 50
```
