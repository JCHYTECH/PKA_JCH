# GL-002 — Skill Inventory and Runtime Map

This guideline records where reusable skills live in the current PKA / local runtime setup, and which runtime can actually discover them.

---

## 1. Rule

A skill is only usable in the runtime that knows how to discover and load it.

- PKA documentation can point to skills.
- A skill file in one runtime does not become globally available everywhere.
- The common index is the durable memory of where each skill lives and what it is for.

---

## 2. Skill stores currently found

| Store | Runtime / context | Path | Status | Comment |
|---|---|---|---|---|
| Internal agent governance skills | PKA project docs | `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/internal-agent-governance/skills/` | approved / draft mix | Human-curated skill registry; not auto-loaded as a runtime skill pack. |
| WildNexus agent skills | PKA project docs | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/07_AGENTS/Agents/*/SKILL.md` | active project skills | Domain agents, including bioacoustics. |
| [[Claude]] video skill | [[Claude]] runtime | 
| [[Codex]] bioacoustics skill | [[Codex]] runtime | 
| Gemini skills | Gemini runtime | `.gemini/` | none found in scan | No local skill pack detected in the current workspace scan. |
| Repo-local skill packs | Workspace / repo tooling | `.agents/skills/` | mixed | Additional skill-like bundles present in the repo. Inventory separately if they become operationally important. |

---

## 3. Practical reading

- Use the skill where it is actually loaded.
- Use this guideline to know whether a skill exists, where it lives, and whether another runtime can see it.
- If a skill matters across runtimes, mirror the idea in PKA and document the actual runtime path explicitly.

---

## 4. Maintenance

- Update this file when a new skill store appears or an existing one changes runtime.
- Keep `wiki/Guidelines/INDEX.md` aligned with this guideline.
