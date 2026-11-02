import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import pka_plane_adapter
from scripts.dashboard_server import ensure_plane_api_token

PROJECT_KEY = "03_WILDNEXUS"
GOVERNANCE_DIR = (
    ROOT / "JCH_Inbox" / "03_PROJECTS" / PROJECT_KEY / "WILDNEXUS_DEVICE" / "00_GOVERNANCE"
)
BACKLOG_PATH = GOVERNANCE_DIR / "wildnexus-plane-seed-backlog.md"
OPERATING_MODEL_PATH = GOVERNANCE_DIR / "wildnexus-plane-operating-model.md"
GANTT_JSON_PATH = GOVERNANCE_DIR / "wildnexus-plane-gantt.json"


def parse_seed_backlog(path: Path) -> dict[str, list[str] | dict[str, list[str]]]:
    sections: dict[str, list[str] | dict[str, list[str]]] = {
        "milestones": [],
        "epics": [],
        "tasks": {},
    }
    current_group: str | None = None
    current_section: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            current_group = None
            continue
        if line.startswith("### "):
            current_group = line[4:].strip()
            if current_section == "Seed Tasks":
                sections["tasks"][current_group] = []
            continue
        if not line.startswith("- `") or not line.endswith("`"):
            continue
        item = line[3:-1]
        if current_section == "Milestone Items":
            sections["milestones"].append(item)
        elif current_section == "Epic Items":
            sections["epics"].append(item)
        elif current_section == "Seed Tasks" and current_group:
            sections["tasks"][current_group].append(item)

    return sections


def module_name_from_epic(epic_name: str) -> str | None:
    if not epic_name.startswith("EPIC: "):
        return None
    body = epic_name[len("EPIC: "):]
    parts = body.split(" - ", 1)
    if len(parts) != 2:
        return None
    return f"{parts[0]} - {parts[1]}"


def build_description(title: str, group: str | None = None) -> str:
    pieces = [f"<p><strong>{html.escape(title)}</strong></p>"]
    if group:
        pieces.append(f"<p>Seeded from <code>{html.escape(group)}</code> in <code>{BACKLOG_PATH.name}</code>.</p>")
    else:
        pieces.append(f"<p>Seeded from <code>{BACKLOG_PATH.name}</code>.</p>")
    pieces.append(f"<p>Operating model reference: <code>{html.escape(OPERATING_MODEL_PATH.name)}</code>.</p>")
    return "".join(pieces)


def type_lookup(types: list[dict]) -> tuple[str | None, str | None]:
    default_type_id = None
    epic_type_id = None
    for item in types:
        item_id = item.get("id")
        if not isinstance(item_id, str):
            continue
        if item.get("is_default") and default_type_id is None:
            default_type_id = item_id
        if item.get("is_epic") and epic_type_id is None:
            epic_type_id = item_id
    return default_type_id, epic_type_id


def sync_modules(existing_modules: list[dict], epic_names: list[str], apply: bool) -> dict[str, str]:
    module_ids: dict[str, str] = {}
    for item in existing_modules:
        name = item.get("name")
        item_id = item.get("id")
        if isinstance(name, str) and isinstance(item_id, str):
            module_ids[name] = item_id

    for epic_name in epic_names:
        module_name = module_name_from_epic(epic_name)
        if not module_name or module_name in module_ids:
            continue
        if not apply:
            print(f"[dry-run] create module: {module_name}")
            continue
        try:
            created = pka_plane_adapter.create_project_module(
                PROJECT_KEY,
                name=module_name,
                description=f"WildNexus P0 module seeded from {BACKLOG_PATH.name}.",
                status="backlog",
            )
        except RuntimeError as exc:
            if "Modules are not enabled for this project" not in str(exc):
                raise
            print("[info] Plane modules are disabled for this project; continuing without module assignment.")
            return {}
        created_id = created.get("id")
        if isinstance(created_id, str):
            module_ids[module_name] = created_id
            print(f"[created] module: {module_name}")
    return module_ids


def delete_all_work_items(apply: bool) -> None:
    items = pka_plane_adapter.list_project_work_items(PROJECT_KEY)
    if not items:
        print("[info] No existing work items to delete.")
        return
    for item in items:
        iid = item.get("id")
        name = item.get("name", "?")
        if not isinstance(iid, str) or not iid:
            continue
        if not apply:
            print(f"[dry-run] delete: {name}")
            continue
        pka_plane_adapter.delete_work_item(PROJECT_KEY, iid)
        print(f"[deleted] {name}")


def _set_state(work_item_id: str, state: str, apply: bool, label: str) -> None:
    if not state:
        return
    if not apply:
        print(f"[dry-run] state: {label} → {state}")
        return
    try:
        pka_plane_adapter.set_work_item_state(PROJECT_KEY, work_item_id, state)
        print(f"[state] {label} → {state}")
    except Exception as exc:  # noqa: BLE001 - state is cosmetic, never block the seed
        print(f"[warn] state not set for {label}: {exc}")


def sync_work_items(seed: dict[str, list[str] | dict[str, list[str]]], gantt: dict, apply: bool) -> None:
    dates = gantt.get("dates", {})
    existing_items = pka_plane_adapter.list_project_work_items(PROJECT_KEY)
    existing_by_name = {
        item["name"]: item["id"]
        for item in existing_items
        if isinstance(item.get("name"), str) and isinstance(item.get("id"), str)
    }
    try:
        types = pka_plane_adapter.list_project_work_item_types(PROJECT_KEY)
    except RuntimeError as exc:
        if "404" not in str(exc):
            raise
        print("[info] Plane instance does not expose work-item-types; creating items without explicit type.")
        types = []
    default_type_id, epic_type_id = type_lookup(types)
    modules = sync_modules(pka_plane_adapter.list_project_modules(PROJECT_KEY), seed["epics"], apply)

    id_by_name: dict[str, str] = dict(existing_by_name)
    epic_ids: dict[str, str] = {}

    for milestone in seed["milestones"]:
        info = dates.get(milestone, {})
        if milestone in existing_by_name:
            id_by_name[milestone] = existing_by_name[milestone]
            print(f"[skip] existing milestone item: {milestone}")
            continue
        if not apply:
            print(f"[dry-run] create milestone item: {milestone} ({info.get('start', '')} → {info.get('end', '')})")
            continue
        created = pka_plane_adapter.create_project_work_item(
            PROJECT_KEY,
            name=milestone,
            description_html=build_description(milestone, "Milestone Items"),
            type_id=default_type_id,
            start_date=info.get("start"),
            target_date=info.get("end"),
        )
        created_id = created.get("id")
        if isinstance(created_id, str):
            id_by_name[milestone] = created_id
            _set_state(created_id, info.get("state"), apply, milestone)
        print(f"[created] milestone item: {created.get('name', milestone)}")

    for epic in seed["epics"]:
        info = dates.get(epic, {})
        if epic in existing_by_name:
            epic_ids[epic] = existing_by_name[epic]
            id_by_name[epic] = existing_by_name[epic]
            print(f"[skip] existing epic item: {epic}")
            continue
        module_name = module_name_from_epic(epic)
        module_id = modules.get(module_name) if module_name else None
        if not apply:
            print(f"[dry-run] create epic item: {epic} ({info.get('start', '')} → {info.get('end', '')})")
            continue
        created = pka_plane_adapter.create_project_work_item(
            PROJECT_KEY,
            name=epic,
            description_html=build_description(epic, "Epic Items"),
            type_id=epic_type_id or default_type_id,
            module_id=module_id,
            start_date=info.get("start"),
            target_date=info.get("end"),
        )
        created_id = created.get("id")
        if isinstance(created_id, str):
            epic_ids[epic] = created_id
            id_by_name[epic] = created_id
            _set_state(created_id, info.get("state"), apply, epic)
        print(f"[created] epic item: {created.get('name', epic)}")

    tasks = seed["tasks"]
    for group, titles in tasks.items():
        epic_name = f"EPIC: {group}"
        epic_id = epic_ids.get(epic_name) or existing_by_name.get(epic_name)
        module_id = modules.get(group)
        for title in titles:
            if title in existing_by_name:
                id_by_name[title] = existing_by_name[title]
                print(f"[skip] existing task item: {title}")
                continue
            if not apply:
                print(f"[dry-run] create task item: {title}")
                continue
            created = pka_plane_adapter.create_project_work_item(
                PROJECT_KEY,
                name=title,
                description_html=build_description(title, group),
                type_id=default_type_id,
                module_id=module_id,
                parent_id=epic_id,
            )
            created_id = created.get("id")
            if isinstance(created_id, str):
                id_by_name[title] = created_id
            print(f"[created] task item: {created.get('name', title)}")


def apply_relations(gantt: dict, id_by_name: dict[str, str], apply: bool) -> None:
    for dep in gantt.get("dependencies", []):
        from_name = dep.get("from")
        to_name = dep.get("to")
        rel_type = dep.get("type", "blocked_by")
        if not isinstance(from_name, str) or not isinstance(to_name, str):
            continue
        from_id = id_by_name.get(from_name)
        to_id = id_by_name.get(to_name)
        if not from_id or not to_id:
            print(f"[skip] relation missing id: {from_name} -> {to_name}")
            continue
        if not apply:
            print(f"[dry-run] relation: {from_name} {rel_type} {to_name}")
            continue
        try:
            pka_plane_adapter.create_work_item_relation(PROJECT_KEY, from_id, rel_type, [to_id])
            print(f"[created] relation: {from_name} {rel_type} {to_name}")
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"[warn] relation failed {from_name} {rel_type} {to_name}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed WildNexus Plane items from the local markdown backlog.")
    parser.add_argument("--apply", action="store_true", help="Create missing modules and work items in Plane.")
    parser.add_argument("--replace", action="store_true", help="Delete existing work items before seeding (fresh re-seed).")
    parser.add_argument("--gantt", type=str, default=str(GANTT_JSON_PATH), help="Path to the gantt JSON (dates + dependencies).")
    args = parser.parse_args()

    ensure_plane_api_token()
    gantt_path = Path(args.gantt)
    gantt: dict = {"dates": {}, "dependencies": []}
    if gantt_path.exists():
        data = json.loads(gantt_path.read_text(encoding="utf-8"))
        gantt = {"dates": data.get("dates", {}), "dependencies": data.get("dependencies", [])}

    if args.replace:
        delete_all_work_items(apply=args.apply)

    seed = parse_seed_backlog(BACKLOG_PATH)
    sync_work_items(seed, gantt, apply=args.apply)

    # Re-read the work items to build a complete id_by_name (created + pre-existing).
    id_by_name = {
        item["name"]: item["id"]
        for item in pka_plane_adapter.list_project_work_items(PROJECT_KEY)
        if isinstance(item.get("name"), str) and isinstance(item.get("id"), str)
    }
    apply_relations(gantt, id_by_name, apply=args.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
