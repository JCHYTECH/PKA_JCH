import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_STATUSES = [
    "A qualifier",
    "Pret",
    "En cours",
    "En attente",
    "En validation",
    "Termine",
    "Archive",
]
CANONICAL_TYPES = [
    "task",
    "decision",
    "document",
    "bug",
    "idea",
    "follow-up",
    "deliverable",
]
CANONICAL_REQUIRED_FIELDS = [
    "title",
    "project",
    "type",
    "owner",
    "priority",
    "status",
    "description",
]
CANONICAL_RECOMMENDED_FIELDS = [
    "lead_specialist",
    "model_used",
    "decision_owner",
    "blocking_reason",
    "expected_outcome",
    "source_link",
]
CANONICAL_LABEL_FAMILIES = {
    "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
    "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
    "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
    "level": ["strategique", "tactique", "operationnel"],
}
CANONICAL_CREATION_ROLES = ["Dobby", "Forge"]
CANONICAL_GOVERNANCE_RULES = {
    "lowercase_only": True,
    "state_labels_forbidden": True,
}
ALLOWED_SEPARATORS = {"-", "_"}


def _load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return data


def _require_mapping(data: dict, key: str, source: str) -> dict:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{source} must define '{key}' as an object")
    return value


def _require_string_list(data: dict, key: str, source: str) -> list[str]:
    if key not in data:
        raise ValueError(f"{source} is missing required key '{key}'")
    value = data[key]
    if not isinstance(value, list):
        raise ValueError(f"{source} must define '{key}' as a list")
    if not all(isinstance(item, str) for item in value):
        raise ValueError(f"{source} must define '{key}' as a list of strings")
    return value


def _validate_schema_shape(data: dict) -> dict:
    source = _schema_path().name
    if _require_string_list(data, "statuses", source) != CANONICAL_STATUSES:
        raise ValueError(f"{source}.statuses must match the canonical order")
    if _require_string_list(data, "types", source) != CANONICAL_TYPES:
        raise ValueError(f"{source}.types must match the canonical order")
    if _require_string_list(data, "required_fields", source) != CANONICAL_REQUIRED_FIELDS:
        raise ValueError(f"{source}.required_fields must match the canonical order")
    if _require_string_list(data, "recommended_fields", source) != CANONICAL_RECOMMENDED_FIELDS:
        raise ValueError(f"{source}.recommended_fields must match the canonical order")
    return data


def _validate_governance_shape(data: dict) -> dict:
    source = _governance_path().name
    labels = _require_mapping(data, "labels", source)
    rules = _require_mapping(data, "rules", source)

    expected_families = ("nature", "domain", "context", "level")
    for family in expected_families:
        _require_string_list(labels, family, f"{source}.labels")

    if tuple(labels.keys()) != expected_families:
        raise ValueError(f"{source}.labels must contain families in canonical order: {expected_families}")

    if "lowercase_only" not in rules or not isinstance(rules["lowercase_only"], bool):
        raise ValueError(f"{source}.rules must define 'lowercase_only' as a boolean")
    if rules["lowercase_only"] != CANONICAL_GOVERNANCE_RULES["lowercase_only"]:
        raise ValueError(f"{source}.rules.lowercase_only must match the canonical value")
    if "separator" not in rules or not isinstance(rules["separator"], str):
        raise ValueError(f"{source}.rules must define 'separator' as a string")
    if rules["separator"] not in ALLOWED_SEPARATORS:
        raise ValueError(f"{source}.rules.separator must be one of {sorted(ALLOWED_SEPARATORS)}")
    if "state_labels_forbidden" not in rules or not isinstance(rules["state_labels_forbidden"], bool):
        raise ValueError(f"{source}.rules must define 'state_labels_forbidden' as a boolean")
    if rules["state_labels_forbidden"] != CANONICAL_GOVERNANCE_RULES["state_labels_forbidden"]:
        raise ValueError(f"{source}.rules.state_labels_forbidden must match the canonical value")
    if "creation_roles" not in rules or not isinstance(rules["creation_roles"], list):
        raise ValueError(f"{source}.rules must define 'creation_roles' as a list")
    if not all(isinstance(item, str) for item in rules["creation_roles"]):
        raise ValueError(f"{source}.rules must define 'creation_roles' as a list of strings")

    return data


def _canonical_state_label(value: str) -> str:
    return value.strip().lower().replace(" ", "-").replace("_", "-")


def _label_pattern(separator: str) -> re.Pattern[str]:
    escaped = re.escape(separator)
    return re.compile(rf"^[a-z0-9]+(?:{escaped}[a-z0-9]+)*$")


def _validate_governance_rules(data: dict) -> dict:
    labels = data["labels"]
    rules = data["rules"]
    expected_separator = rules["separator"]
    lowercase_only = rules["lowercase_only"]
    state_labels_forbidden = rules["state_labels_forbidden"]
    canonical_states = {_canonical_state_label(status) for status in CANONICAL_STATUSES}
    pattern = _label_pattern(expected_separator)
    flattened_labels = []

    for family, family_labels in labels.items():
        for label in family_labels:
            if lowercase_only and label != label.lower():
                raise ValueError(f"{_governance_path().name}.labels.{family} labels must be lowercase")
            if not pattern.fullmatch(label):
                raise ValueError(
                    f"{_governance_path().name}.labels.{family} labels must use '{expected_separator}' as separator"
                )
            if state_labels_forbidden and _canonical_state_label(label) in canonical_states:
                raise ValueError(f"{_governance_path().name}.labels.{family} state-like labels are forbidden")
        flattened_labels.extend(family_labels)

    if len(flattened_labels) != len(set(flattened_labels)):
        raise ValueError("duplicate labels are forbidden")

    for family, family_labels in labels.items():
        if family_labels != CANONICAL_LABEL_FAMILIES[family]:
            raise ValueError(f"{_governance_path().name}.labels.{family} must match the canonical order")

    if rules["creation_roles"] != CANONICAL_CREATION_ROLES:
        raise ValueError(f"{_governance_path().name}.rules.creation_roles must match the canonical order")

    return data


def _schema_path() -> Path:
    return ROOT / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_schema.json"


def _governance_path() -> Path:
    return ROOT / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"


def load_schema() -> dict:
    data = _validate_schema_shape(_load_json(_schema_path()))
    if data["statuses"] != CANONICAL_STATUSES:
        raise ValueError("canonical status order drift")
    return data


def load_governance() -> dict:
    data = _validate_governance_shape(_load_json(_governance_path()))
    data = _validate_governance_rules(data)
    return data
