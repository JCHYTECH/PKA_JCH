from collections import Counter, defaultdict

from scripts import pka_kanban_schema


def validate_card(card: dict) -> dict:
    schema = pka_kanban_schema.load_schema()

    for field in schema["required_fields"]:
        if not card.get(field):
            raise ValueError(f"missing required field: {field}")

    if card["status"] not in schema["statuses"]:
        raise ValueError(f"unknown status: {card['status']}")

    return card


def build_summary(cards: list[dict]) -> dict:
    schema = pka_kanban_schema.load_schema()
    totals = Counter({status: 0 for status in schema["statuses"]})
    by_project = defaultdict(lambda: {"total": 0})
    blocked = 0
    awaiting_jch = 0

    for raw_card in cards:
        card = validate_card(raw_card)
        totals[card["status"]] += 1
        by_project[card["project"]]["total"] += 1

        if card["status"] == "En attente":
            blocked += 1
        if card["status"] == "En validation" and "en-attente-jch" in card.get("labels", []):
            awaiting_jch += 1

    return {
        "totals": dict(totals),
        "blocked": blocked,
        "awaiting_jch": awaiting_jch,
        "by_project": dict(by_project),
    }
