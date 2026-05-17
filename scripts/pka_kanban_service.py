from functools import lru_cache
from collections import Counter, defaultdict

from scripts import pka_kanban_schema


@lru_cache(maxsize=1)
def _schema() -> dict:
    return pka_kanban_schema.load_schema()


def validate_card(card: dict) -> dict:
    schema = _schema()

    for field in schema["required_fields"]:
        if not card.get(field):
            raise ValueError(f"missing required field: {field}")

    if card["status"] not in schema["statuses"]:
        raise ValueError(f"unknown status: {card['status']}")

    return card


def _status_rank(status: str) -> int:
    schema = _schema()
    return schema["statuses"].index(status)


def _normalized_labels(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return sorted(label for label in value if isinstance(label, str))
    return []


def _normalized_card(raw_card: dict) -> dict:
    card = validate_card(raw_card)
    labels = _normalized_labels(card.get("labels", []))
    normalized = dict(card)
    normalized["labels"] = labels
    normalized["awaiting_jch"] = card["status"] == "En validation" and "en-attente-jch" in labels
    normalized["blocked"] = card["status"] == "En attente"
    return normalized


def _iter_normalized_cards(cards: list[dict]) -> list[dict]:
    normalized_cards = []
    for raw_card in cards:
        try:
            normalized_cards.append(_normalized_card(raw_card))
        except ValueError:
            continue
    return normalized_cards


def build_summary(cards: list[dict]) -> dict:
    schema = _schema()
    totals = Counter({status: 0 for status in schema["statuses"]})
    by_project = defaultdict(lambda: {"total": 0})
    blocked = 0
    awaiting_jch = 0

    for card in _iter_normalized_cards(cards):
        totals[card["status"]] += 1
        by_project[card["project"]]["total"] += 1

        if card["blocked"]:
            blocked += 1
        if card["awaiting_jch"]:
            awaiting_jch += 1

    return {
        "totals": dict(totals),
        "blocked": blocked,
        "awaiting_jch": awaiting_jch,
        "by_project": dict(by_project),
    }


def build_card_list(
    cards: list[dict],
    project: str | None = None,
    status: str | None = None,
    owner: str | None = None,
    awaiting_jch_only: bool = False,
) -> list[dict]:
    filtered_cards = []

    for card in _iter_normalized_cards(cards):
        if project and card["project"] != project:
            continue
        if status and card["status"] != status:
            continue
        if owner and card["owner"] != owner:
            continue
        if awaiting_jch_only and not card["awaiting_jch"]:
            continue
        filtered_cards.append(card)

    return sorted(filtered_cards, key=lambda card: (_status_rank(card["status"]), card["title"].lower()))


def available_card_filters(cards: list[dict]) -> dict:
    normalized_cards = _iter_normalized_cards(cards)

    return {
        "projects": sorted({card["project"] for card in normalized_cards}),
        "statuses": [status for status in _schema()["statuses"] if any(card["status"] == status for card in normalized_cards)],
        "owners": sorted({card["owner"] for card in normalized_cards}),
    }
