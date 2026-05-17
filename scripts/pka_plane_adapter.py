import json
import os
from pathlib import Path
from urllib import request
from urllib import error


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PLACEHOLDER_API_BASE = "https://plane.example/api/v1"


def _config_path() -> Path:
    return ROOT / "JCH_Inbox" / "99_SYSTEM" / "pka_plane_config.json"


def _projects_dir() -> Path:
    return ROOT / "JCH_Inbox" / "03_PROJECTS"


def load_config() -> dict:
    data = json.loads(_config_path().read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("pka_plane_config.json must contain a JSON object")

    workspace_slug = data.get("workspace_slug")
    if not isinstance(workspace_slug, str) or not workspace_slug.strip():
        raise ValueError("pka_plane_config.json.workspace_slug must be a non-empty string")

    api_base = data.get("api_base")
    if not isinstance(api_base, str) or not api_base.strip():
        raise ValueError("pka_plane_config.json.api_base must be a non-empty string")
    if api_base.strip() == SCHEMA_PLACEHOLDER_API_BASE:
        raise ValueError("pka_plane_config.json.api_base must not use the scaffold placeholder")

    projects = data.get("projects")
    if not isinstance(projects, dict):
        raise ValueError("pka_plane_config.json.projects must be a mapping")

    return data


def plane_token() -> str | None:
    config = load_config()
    env_var = config.get("api_token_env")
    if not isinstance(env_var, str) or not env_var:
        return None
    return os.environ.get(env_var)


def _project_context(project_key: str) -> tuple[str, str, str, str]:
    config = load_config()
    token = plane_token()
    if not token:
        raise RuntimeError("Plane API token is not configured in the environment")

    project_id = _plane_project_id(config["projects"].get(project_key))
    if project_id is None:
        raise ValueError(f"Plane project mapping is unusable for {project_key}")

    api_base = config["api_base"].rstrip("/")
    workspace_slug = config["workspace_slug"].strip()
    return api_base, workspace_slug, project_id, token


def _plane_request(url: str, token: str, *, method: str = "GET", payload: dict | None = None) -> dict | list:
    headers = {"X-API-Key": token}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")

    plane_request = request.Request(url, headers=headers, method=method, data=body)
    try:
        with request.urlopen(plane_request) as response:
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Plane API request failed ({exc.code}): {raw[:240]}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Plane API request failed: {exc.reason}") from exc

    if not raw:
        return {}
    return json.loads(raw)


def normalize_issue(project_key: str, issue: dict) -> dict:
    assignee = issue.get("assignee")
    if not isinstance(assignee, dict):
        assignee = {}

    state = issue.get("state")
    if not isinstance(state, dict):
        state = {}

    label_details = issue.get("label_details")
    if not isinstance(label_details, list):
        label_details = []

    description = issue.get("description_html") or issue.get("description_stripped") or ""

    return {
        "title": issue.get("name", ""),
        "project": project_key,
        "status": state.get("name", ""),
        "owner": assignee.get("display_name") or "Unassigned",
        "labels": [label.get("name") for label in label_details if isinstance(label, dict) and label.get("name")],
        "type": "task",
        "priority": "normale",
        "description": description,
    }


def fetch_project_issues(project_key: str) -> list[dict]:
    api_base, workspace_slug, project_id, token = _project_context(project_key)
    endpoint = f"{api_base}/workspaces/{workspace_slug}/projects/{project_id}/issues/"
    payload = _plane_request(endpoint, token)

    if isinstance(payload, list):
        issues = payload
    elif isinstance(payload, dict):
        issues = payload.get("results", [])
    else:
        raise ValueError("Plane issues response must be a JSON list or object")

    if not isinstance(issues, list):
        raise ValueError("Plane issues response.results must be a list")

    return [normalize_issue(project_key, issue) for issue in issues if isinstance(issue, dict)]


def list_project_work_items(project_key: str) -> list[dict]:
    api_base, workspace_slug, project_id, token = _project_context(project_key)
    endpoint = f"{api_base}/workspaces/{workspace_slug}/projects/{project_id}/work-items/"
    payload = _plane_request(endpoint, token)
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        items = payload.get("results", [])
    else:
        raise ValueError("Plane work items response must be a JSON list or object")

    if not isinstance(items, list):
        raise ValueError("Plane work items response.results must be a list")
    return [item for item in items if isinstance(item, dict)]


def list_project_work_item_types(project_key: str) -> list[dict]:
    api_base, workspace_slug, project_id, token = _project_context(project_key)
    endpoint = f"{api_base}/workspaces/{workspace_slug}/projects/{project_id}/work-item-types/"
    payload = _plane_request(endpoint, token)
    if isinstance(payload, list):
        types = payload
    elif isinstance(payload, dict):
        types = payload.get("results", [])
    else:
        raise ValueError("Plane work item types response must be a JSON list or object")

    if not isinstance(types, list):
        raise ValueError("Plane work item types response.results must be a list")
    return [item for item in types if isinstance(item, dict)]


def list_project_modules(project_key: str) -> list[dict]:
    api_base, workspace_slug, project_id, token = _project_context(project_key)
    endpoint = f"{api_base}/workspaces/{workspace_slug}/projects/{project_id}/modules/"
    payload = _plane_request(endpoint, token)
    if isinstance(payload, list):
        modules = payload
    elif isinstance(payload, dict):
        modules = payload.get("results", [])
    else:
        raise ValueError("Plane modules response must be a JSON list or object")

    if not isinstance(modules, list):
        raise ValueError("Plane modules response.results must be a list")
    return [item for item in modules if isinstance(item, dict)]


def create_project_module(project_key: str, *, name: str, description: str = "", status: str = "backlog") -> dict:
    api_base, workspace_slug, project_id, token = _project_context(project_key)
    endpoint = f"{api_base}/workspaces/{workspace_slug}/projects/{project_id}/modules/"
    payload = {
        "name": name,
        "description": description,
        "status": status,
    }
    result = _plane_request(endpoint, token, method="POST", payload=payload)
    if not isinstance(result, dict):
        raise ValueError("Plane module create response must be a JSON object")
    return result


def create_project_work_item(
    project_key: str,
    *,
    name: str,
    description_html: str = "",
    type_id: str | None = None,
    module_id: str | None = None,
    parent_id: str | None = None,
    priority: str | None = None,
    start_date: str | None = None,
    target_date: str | None = None,
) -> dict:
    api_base, workspace_slug, project_id, token = _project_context(project_key)
    endpoint = f"{api_base}/workspaces/{workspace_slug}/projects/{project_id}/work-items/"
    payload: dict[str, object] = {"name": name}
    if description_html:
        payload["description_html"] = description_html
    if type_id:
        payload["type"] = type_id
    if module_id:
        payload["module"] = module_id
    if parent_id:
        payload["parent"] = parent_id
    if priority:
        payload["priority"] = priority
    if start_date:
        payload["start_date"] = start_date
    if target_date:
        payload["target_date"] = target_date

    result = _plane_request(endpoint, token, method="POST", payload=payload)
    if not isinstance(result, dict):
        raise ValueError("Plane work item create response must be a JSON object")
    return result


def _plane_project_id(entry: object) -> str | None:
    if not isinstance(entry, dict):
        return None
    value = entry.get("plane_project_id")
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def validate_project_registry() -> list[str]:
    config = load_config()
    projects = config.get("projects")
    mapped = projects if isinstance(projects, dict) else {}
    findings = []
    for item in sorted(_projects_dir().iterdir()):
        if item.is_dir() and item.name not in mapped:
            findings.append(f"03_PROJECTS project directory missing from Plane config: {item.name}")
            continue
        if item.is_dir() and _plane_project_id(mapped.get(item.name)) is None:
            findings.append(f"03_PROJECTS project directory has unusable Plane mapping: {item.name}")
    return findings
