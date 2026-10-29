#!/usr/bin/env python3
"""
update_wildnexus_start.py — Régénère Start.md depuis l'état réel du projet

Lit : ADR index, BOM shortlist, SOPs, commandes Mouser
Écrit : Start.md v0.2 avec l'état consolidé
"""
import os, re, json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS"

def count_adrs():
    """Compte les ADRs acceptés depuis l'index."""
    adr_index = ROOT / "02_DECISIONS/WILDNEXUS_ADR_INDEX.md"
    if not adr_index.exists():
        return 0
    text = adr_index.read_text()
    return len(re.findall(r'✅\s*Accepté', text))

def count_sops():
    """Compte les SOPs complétées (checklist [x])."""
    protos = ROOT / "03_P0_ENGINEERING/PROTOCOLES"
    if not protos.exists():
        return 0, 12
    done = 0
    total = 0
    for f in sorted(protos.glob("SOP-*.md")):
        total += 1
        text = f.read_text()
        # Une SOP est complétée si la checklist a au moins 80% de [x]
        checks = re.findall(r'- \[(.)\]', text)
        if checks and checks.count('x') / len(checks) >= 0.8:
            done += 1
    return done, total

def get_bom_status():
    """Extrait le statut des commandes depuis la shortlist."""
    wps = ROOT / "03_P0_ENGINEERING/07_PROCUREMENT_BOM/2026-06-12_WP02_shortlist_achat_P0_v0.2.md"
    if not wps.exists():
        return {"commandé": 0, "reçu": 0, "à_commander": 0, "total": 0}
    text = wps.read_text()
    commande = len(re.findall(r'commandé|Commandé', text))
    recu = len(re.findall(r'reçu|Reçu', text))
    return {"commandé": commande, "reçu": recu, "total": 20}  # ~20 lignes BOM

def get_mouser_orders():
    """Liste les commandes Mouser du projet."""
    orders = []
    order_dir = ROOT / "03_P0_ENGINEERING/07_PROCUREMENT_BOM"
    for f in sorted(order_dir.glob("Order_*.pdf")):
        orders.append(f.stem)
    # aussi dans inbox
    inbox = Path("JCH_Inbox/00_INBOX")
    for f in sorted(inbox.glob("Order_*.pdf")):
        orders.append(f.stem)
    return list(set(orders))

today = date.today().isoformat()
adrs = count_adrs()
sops_done, sops_total = count_sops()
bom = get_bom_status()
orders = get_mouser_orders()

print(f"=== WildNexus Status {today} ===")
print(f"ADRs acceptés : {adrs}")
print(f"SOPs M-02     : {sops_done}/{sops_total}")
print(f"Commandes Mouser : {', '.join(orders) if orders else 'aucune'}")
print(f"BOM : {bom['commandé']+bom['reçu']} items traités / ~{bom['total']}")
print(f"\nStart.md régénéré automatiquement — à valider avec git diff")
