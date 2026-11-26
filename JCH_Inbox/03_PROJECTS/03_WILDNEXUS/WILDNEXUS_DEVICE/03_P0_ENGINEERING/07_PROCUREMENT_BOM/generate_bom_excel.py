"""
Génère le fichier Excel WildNexus BOM P0 v0.4.
Révision documentaire : 2026-11-05 — statuts à rapprocher du stock, dépenses gelées.
"""
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ── Styles ──────────────────────────────────────────────────────────────────
HDR_FILL   = PatternFill("solid", fgColor="1F4E79")
HDR_FONT   = Font(color="FFFFFF", bold=True, size=10)
SUB_FILL   = PatternFill("solid", fgColor="2E75B6")
SUB_FONT   = Font(color="FFFFFF", bold=True, size=10)
ALT_FILL   = PatternFill("solid", fgColor="D6E4F0")
WARN_FILL  = PatternFill("solid", fgColor="FFF2CC")
OK_FILL    = PatternFill("solid", fgColor="E2EFDA")
RED_FILL   = PatternFill("solid", fgColor="FCE4D6")
TOTAL_FONT = Font(bold=True, size=10)
THIN       = Side(style="thin", color="BBBBBB")
BORDER     = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP       = Alignment(wrap_text=True, vertical="top")
CENTER     = Alignment(horizontal="center", vertical="top")

def style_header(cell, sub=False):
    cell.fill   = SUB_FILL if sub else HDR_FILL
    cell.font   = SUB_FONT if sub else HDR_FONT
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = BORDER

def style_cell(cell, alt=False, warn=False, ok=False, red=False, bold=False, center=False):
    if warn:   cell.fill = WARN_FILL
    elif ok:   cell.fill = OK_FILL
    elif red:  cell.fill = RED_FILL
    elif alt:  cell.fill = ALT_FILL
    cell.font      = Font(bold=bold, size=10)
    cell.alignment = CENTER if center else WRAP
    cell.border    = BORDER

def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def freeze(ws, cell="A2"):
    ws.freeze_panes = cell

# ════════════════════════════════════════════════════════════════════════════
# Feuille 1 — Option A (Banc rapide)
# ════════════════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "Option A — Banc rapide"
freeze(ws, "C3")

ws.merge_cells("A1:L1")
title = ws["A1"]
title.value = "WildNexus P0 — Option A | Base BOM v0.4, révision 2026-11-05 | Stock à contrôler | Achats gelés"
title.font  = Font(bold=True, size=12, color="1F4E79")
title.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 30

headers = ["#", "Composant", "Référence précise", "Fournisseur", "Qté",
           "Prix unitaire consigné (€)", "Total consigné (€)", "Délai historique", "Risque supply",
           "Statut documentaire", "Note", "Action requise"]
for c, h in enumerate(headers, 1):
    cell = ws.cell(row=2, column=c, value=h)
    style_header(cell)
ws.row_dimensions[2].height = 30

option_a = [
    ("A01", "MCU prototype", "ESP32-S3-DevKitC-1-N8R8 (8MB flash, 8MB PSRAM, USB-C)",
     "Mouser BE", 2, 16.00, 32.00, "3–5 j", "🟢 Bas", "⏸️ Variante à rapprocher du stock",
     "Le suivi Start.md consigne deux N16R8 reçus via Amazon, non cette variante N8R8.", "Vérifier la référence physique avant tout achat"),
    ("A02", "Caméra capteur (REJETÉ)", "Camemake CM_DVP_OV5640_UNIVERSAL — REJETÉ (MOQ 10)",
     "—", "—", "—", "—", "—", "—", "🔴 Rejeté",
     "Remplacé par A02a (ESP32-CAM) + A02b (OV5640 AliExpress)", "—"),
    ("A02a", "Caméra dév DVP", "Hailege 2pcs ESP32-CAM (OV2640 2MP DVP, LED flash, slot SD onboard)",
     "Amazon.de", 2, 12.50, 25.00, "2–3 j", "🟢 Bas", "✅ Commandé (2026-06)",
     "Outil DVP + SD onboard. Ne pas brancher OV5640 ici. Stock physique à contrôler.", ""),
    ("A02b", "Caméra finale P0 candidate", "OV5640 DVP M12 24-pin 5MP (ref 1005005710463218 ; alimentation et NoIR à confirmer)",
     "AliExpress", 4, 5.81, 23.24, "15–25 j", "🟡 Moyen", "✅ Commandé (2026-06)",
     "Relever le module, son régulateur et son interface avant câblage. Quantité réelle à rapprocher du stock.", ""),
    ("A02c", "Level shifter DVP proto", "Modules 8ch pré-assemblés (ref 1005010226529230, 3.3V↔1.8V)",
     "AliExpress", 2, 8.20, 16.39, "10–20 j", "🟢 Bas", "✅ Commandé (2026-06)",
     "Prototype seulement. Total historique conservé malgré l'arrondi du prix unitaire ; facture et réception à contrôler.", ""),
    ("A03", "LED IR 850 nm (RETIRÉ)", "Vishay VSLY3850 — RETIRÉ (850nm perceptible faune)",
     "—", "—", "—", "—", "—", "—", "🔴 Retiré",
     "IR 940nm uniquement (A04)", "—"),
    ("A04", "LED IR 940 nm", "Vishay VSLB3940 (×4 par nœud)",
     "Mouser BE", 10, 0.37, 3.74, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Référence à rapprocher du stock : le registre historique mentionne aussi Würth.", ""),
    ("A05", "PIR basse conso", "Panasonic EKMB1203111 (caractéristiques à confirmer par datasheet)",
     "Mouser BE", 2, 22.30, 44.60, "5–8 j", "🟢 Bas", "✅ Commandé #39492997",
     "Relever la référence physique : le stock historique mentionne EKMB1303111.", ""),
    ("A06", "Micro MEMS — interface à vérifier", "TDK MMICT5848-00-012 (interface déclarée I2S dans l'ancien BOM, datasheet non vérifiée)",
     "Mouser BE", 3, 2.04, 6.12, "3–7 j", "🟡 À confirmer", "✅ Commandé #39492997",
     "Ne pas déclarer compatible I2S ni substituer au SPH0645LM4H-B sans relever la référence et vérifier la datasheet.", ""),
    ("A07", "microSD 128 GB", "Carte 128 GB requise par ADR-004/017 ; référence et endurance à sélectionner",
     "Fournisseur à revalider", 1, 15.00, 15.00, "À revalider", "🟡 Moyen", "⏸️ Non considérée reçue — achat gelé",
     "Le coût provisoire de 15 € provient de la projection budget ; ce n'est pas un devis actuel.", "Réconcilier stock/budget puis arbitrage JCH"),
    ("A08", "Buck faible Iq", "TPS62840DLCR (Iq typique 60 nA ; entrée recommandée 1,8–6,5 V ; schéma à valider)",
     "Mouser BE", 5, 1.85, 9.25, "3–5 j", "🟢 Bas", "✅ Commandé #39492997 — réception à confirmer",
     "Prix historique. Le stock mentionne un backorder ; vérifier la quantité reçue et le schéma complet avant usage.", ""),
    ("A09", "Holder AA × 4", "Keystone 2463 (4× AA, fils) — configuration à revoir",
     "RS Belgium / Mouser BE", 4, 3.50, 14.00, "3–7 j", "🟡 Schéma ouvert", "⏸️ SUSPENDU avec SOP-10",
     "Ne pas assembler un pack 4S2P L91 : tension maximale et compatibilité du régulateur non démontrées.", "Revue ADR-005 et schéma avant achat/montage"),
    ("A10", "Inductance buck", "Würth 744043100 (10 µH, 1 A, 3×3 mm)",
     "Mouser BE", 5, 1.31, 6.55, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix historique ; vérifier l'adéquation au schéma validé.", ""),
    ("A11", "Passifs CMS", "Lot 0402/0603 : C 100nF/10µF/1µF ; R 10K/100K/1M",
     "Mouser BE", 1, 20.00, 20.00, "3–5 j", "🟢 Bas", "⏸️ À rapprocher du stock — achat gelé",
     "Lot historique — valeurs et quantités à recalculer depuis le schéma validé.", ""),
    ("A12", "MOSFET power gating", "Vishay SI2302CDS-T1-GE3 (N-ch, SOT-23, 20V)",
     "Mouser BE", 5, 0.71, 3.55, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Référence à rapprocher du stock et du schéma de coupure ; l'ancien registre mentionne Nexperia.", ""),
    ("A13", "Nordic PPK2", "Nordic Power Profiler Kit II (nRF-PPK2)",
     "Mouser BE", 1, 83.57, 83.57, "Reçu", "🟢 Bas", "✅ Reçu Mouser #39411684",
     "Montant enregistré, HT/TTC/port à rapprocher ; ne pas ajouter une seconde ligne PPK2.", "Ne pas racheter"),
    ("A14", "Breadboard + Dupont", "Kit proto 830 pts + câbles — Miuzei Kit",
     "—", "—", "—", "—", "—", "—", "✅ Consigné reçu",
     "Prix et contenu à rapprocher de la facture dans le budget consolidé.", ""),
    ("A15", "Alimentation labo (RETIRÉ)", "Ligne historique retirée ; configuration d'alimentation/mesure PPK2 à documenter",
     "—", "—", "—", "—", "—", "—", "🔴 Retiré",
     "Ne pas alimenter un montage non validé au prétexte que le PPK2 peut sourcer.", ""),
    ("A16", "Piles AA lithium", "Energizer Ultimate Lithium L91 AA × 16",
     "Carrefour / Action / Amazon", 16, 1.80, 29.00, "Immédiat", "🟡 Schéma ouvert", "⏸️ SUSPENDU avec SOP-10",
     "Total historique conservé malgré l'arrondi unitaire. Li-FeS2, non Li-ion. Aucun pack avant revue de tension.", "Revue ADR-005 et autorisation JCH"),
    ("A17", "Dissipateur OV5640", "ATS-HK127-R0 ou mini radiateur alu 14×14×5mm",
     "Mouser BE", 4, 1.31, 5.24, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Besoin thermique et compatibilité boîtier à mesurer, pas une validation du capteur.", ""),
    ("A18", "Lentille M12 2.8mm", "Objectif M12 2.8mm NoIR f/1.8, champ à mesurer",
     "Arducam / Lensation", 2, 25.00, 50.00, "5–10 j", "🟡 Moyen", "⏸️ À revalider — achat gelé",
     "Prix historique non devis. Comparer les focales et la correction IR sur images réelles.", "Sélection et devis avant arbitrage"),
    ("A19", "ESP32-S3 basse conso candidat", "NULA DeepSleep ESP32-S3 (WROOM-1-N8R8, consommation à mesurer)",
     "Soldered.com (Croatie)", 1, 25.00, 25.00, "5–10 j", "🟡 À mesurer", "⏸️ À rapprocher du stock — achat gelé",
     "Aucune valeur de deep sleep n'est retenue sans mesure PPK2 de la configuration réelle.", ""),
    ("A20", "Breakout nu ESP32-S3", "Freenove Breakout Board WROOM/WROVER + module ESP32-S3-WROOM-1",
     "Amazon.de / Freenove", 1, 15.00, 15.00, "3–7 j", "🟢 Bas", "⏸️ À rapprocher du stock — achat gelé",
     "Alternative candidate ; mesures et compatibilité à établir. FTDI externe requis.", ""),
]

total_a = 0
for r, row in enumerate(option_a, 3):
    alt  = (r % 2 == 0)
    warn = "⚠️" in str(row[9]) or "⚠️" in str(row[10]) or "🔴" in str(row[9])
    ok   = "✅" in str(row[9])
    red  = "🔴" in str(row[9]) or "RETIRÉ" in str(row[1])
    for c, val in enumerate(row, 1):
        cell = ws.cell(row=r, column=c, value=val)
        style_cell(cell, alt=alt, warn=warn, ok=(ok and not warn), red=red)
    if isinstance(row[6], (int, float)):
        total_a += row[6]
    ws.row_dimensions[r].height = 45

r_sub = len(option_a) + 3
ws.merge_cells(f"A{r_sub}:F{r_sub}")
sub = ws[f"A{r_sub}"]
sub.value = "Sous-total des lignes historiques Option A — ni dépense ni reliquat certifié"
sub.font  = Font(bold=True, color="FFFFFF")
sub.fill  = PatternFill("solid", fgColor="2E75B6")
sub.alignment = Alignment(horizontal="right", vertical="center")
tot = ws.cell(row=r_sub, column=7, value=f"~{total_a:.2f} €")
tot.font = Font(bold=True, color="FFFFFF")
tot.fill = PatternFill("solid", fgColor="2E75B6")
tot.alignment = CENTER

set_col_widths(ws, [5, 22, 38, 20, 5, 9, 9, 9, 10, 18, 50, 28])

# ════════════════════════════════════════════════════════════════════════════
# Feuille 2 — Option B (Terrain compact)
# ════════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("Option B — Terrain")
freeze(ws2, "C3")

ws2.merge_cells("A1:L1")
t2 = ws2["A1"]
t2.value = "WildNexus P0 — Option B | Base BOM v0.4, révision 2026-11-05 | Candidats à revalider | Achats gelés"
t2.font  = Font(bold=True, size=12, color="1F4E79")
t2.alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 30

for c, h in enumerate(headers, 1):
    cell = ws2.cell(row=2, column=c, value=h)
    style_header(cell)
ws2.row_dimensions[2].height = 30

option_b = [
    ("B01", "Lentille M12 IR-corrigée", "Lensation LS-6028 f/1.8 6mm / Evetar M12B0618W-IR — à confirmer",
     "Lensation.de", 2, 40.00, 80.00, "5–10 j", "🟡 Moyen", "⏸️ Après M-02 — devis requis",
     "Ancien prix de cadrage, non un devis. Sélectionner l'optique sur images réelles jour/nuit.", "Devis puis arbitrage JCH"),
    ("B02", "Module LoRa P0", "RAK3172-T EU868 (SX1262, IPEX ; conformité et température à vérifier)",
     "RAK Store EU", 2, 14.00, 28.00, "5–10 j", "🟡 À revalider", "⏸️ Après M-02 — achat gelé",
     "Vérifier EU868 + IPEX explicite et présence réelle dans le panier avant prix.", ""),
    ("B03", "Antenne LoRa 868 MHz", "Molex 211140-0100 (flex, IPEX, ~100mm)",
     "Mouser BE", 2, 2.15, 4.30, "3–7 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix historique ; contrôler la référence et la connectique du stock.", ""),
    ("B04", "Boîtier visé IP67", "Hammond 1554A (150×100×60mm) ABS — cible IP67 à valider",
     "RS Belgium / Mouser", 2, 16.00, 32.00, "3–7 j", "🟡 Moyen", "⏸️ Après layout — ADR-006 proposé",
     "La référence fournisseur ne prouve pas l'étanchéité du boîtier modifié et équipé.", "Layout, datasheet et revue avant achat"),
    ("B05", "BME688 capteur env.", "Bosch BME688 (T/P/H/gaz, I2C/SPI)",
     "Mouser BE", 2, 7.44, 14.88, "3–7 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix historique ; capteur optionnel dans le prototype P0.", ""),
    ("B06", "SHT31-DIS humidité", "Sensirion SHT31-DIS-B (±2% RH, I2C)",
     "Mouser BE", 2, 3.87, 7.74, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix historique ; contrôler la référence du stock.", ""),
    ("B07", "Connecteur étanche", "Presse-étoupe M16 IP68 nylon ×4",
     "RS Belgium / Mouser", 4, 2.00, 8.00, "3–7 j", "🟡 Moyen", "⏸️ Après layout — achat gelé",
     "Passage câble sangle/antenne ; IP à valider sur l'ensemble monté.", ""),
    ("B08", "Silica gel + joints", "Sachets 5g silica gel ×10 + joint torique EPDM 140×3",
     "Conrad / Amazon", 1, 10.00, 10.00, "Immédiat", "🟡 À revalider", "⏸️ À rapprocher du stock",
     "Maintenance terrain ; dimensions et prix historiques à vérifier.", ""),
    ("B09", "Sangle UV terrain", "Sangle polyester UV 20mm × 50cm + boucle inox",
     "Conrad / Camping", 4, 4.00, 16.00, "Immédiat", "🟡 À revalider", "⏸️ À rapprocher du stock",
     "Fixation tronc à tester sans promesse de durée ou de tenue.", ""),
    ("B10", "Gateway LoRa candidate", "LILYGO T-Beam SUPREME (SX1262, ESP32-S3 ; variante EU868 et GPS à confirmer)",
     "LILYGO / AliExpress", 1, 35.00, 35.00, "10–15 j", "🟡 Revue radio requise", "⏸️ Après architecture WP05",
     "Ne pas retenir la version 1 W/+32 dBm sans revue réglementaire et radio. Chiffrer une gateway P0 minimale ; la STATION commerciale reste P1.", "Revue WP05 et arbitrage JCH"),
]

total_b = 0
for r, row in enumerate(option_b, 3):
    alt  = (r % 2 == 0)
    warn = "⚠️" in str(row[9]) or "⚠️" in str(row[10])
    ok   = "✅" in str(row[9])
    for c, val in enumerate(row, 1):
        cell = ws2.cell(row=r, column=c, value=val)
        style_cell(cell, alt=alt, warn=warn, ok=(ok and not warn))
    total_b += row[6]
    ws2.row_dimensions[r].height = 45

r_sub2 = len(option_b) + 3
ws2.merge_cells(f"A{r_sub2}:F{r_sub2}")
sub2 = ws2[f"A{r_sub2}"]
sub2.value = "Sous-total des lignes historiques Option B — ni dépense ni reliquat certifié"
sub2.font  = Font(bold=True, color="FFFFFF")
sub2.fill  = PatternFill("solid", fgColor="2E75B6")
sub2.alignment = Alignment(horizontal="right", vertical="center")
tot2 = ws2.cell(row=r_sub2, column=7, value=f"~{total_b:.2f} €")
tot2.font = Font(bold=True, color="FFFFFF")
tot2.fill = PatternFill("solid", fgColor="2E75B6")
tot2.alignment = CENTER

set_col_widths(ws2, [5, 22, 38, 20, 5, 9, 9, 9, 10, 18, 50, 28])

# ════════════════════════════════════════════════════════════════════════════
# Feuille 3 — Budget consolidé
# ════════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("Budget consolidé")

ws3.merge_cells("A1:D1")
t3 = ws3["A1"]
t3.value = "WildNexus P0 — Budget provisoire | Enveloppe 1 000 € | Seuil de pause 900 € atteint"
t3.font  = Font(bold=True, size=12, color="1F4E79")
t3.alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 30

total_ab = total_a + total_b
engaged_global = 610
remaining_basket = 279
sd_projection = 15
projection = engaged_global + remaining_basket + sd_projection
reserve = 1000 - projection

budget_rows = [
    ("Bloc", "Montant", "Nature", "Note", True),
    ("Lignes visibles dédupliquées", "~332,75 €", "Justification partielle", "Avec PPK2 à 83,57 € ; hors postes non chiffrés et ports non identifiés", False),
    ("Somme historique Option A", f"~{total_a:.2f} €", "Lignes de liste", "Mélange de commandes et candidats ; ne pas l'assimiler à une dépense", False),
    ("Somme historique Option B", f"~{total_b:.2f} €", "Lignes de liste", "Prix et références anciens à revalider", False),
    ("Somme historique A + B", f"~{total_ab:.2f} €", "Réconciliation", "Ne s'additionne pas à l'engagé global : chevauchements possibles", False),
    ("Engagé global consigné", "~610 €", "Projection héritée", "Écart avec les lignes visibles à justifier par les factures", False),
    ("Panier restant", "~279 €", "Achat gelé", "Contenu, stock et prix à revalider", False),
    ("microSD 128 GB", "~15 €", "Achat gelé", "Hypothèse de projection, non un devis", False),
    ("TOTAL PROVISOIRE ENGAGÉ / PRÉVU", f"~{projection} €", "Pause obligatoire", "Seuil interne de 900 € dépassé : réconciliation puis autorisation JCH", True),
    ("Réserve théorique sur 1 000 €", f"~{reserve} €", "Non disponible sans arbitrage", "Source : 08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md", True),
]

for r, (label, est, rev, note, bold) in enumerate(budget_rows, 2):
    is_hdr = bold and r == 2
    for c, val in enumerate([label, est, rev, note], 1):
        cell = ws3.cell(row=r, column=c, value=val)
        if is_hdr:
            style_header(cell)
        elif bold:
            cell.font = TOTAL_FONT
            cell.fill = RED_FILL if reserve < 0 else WARN_FILL
        else:
            alt = (r % 2 == 0)
            style_cell(cell, alt=alt)

set_col_widths(ws3, [38, 20, 30, 65])

# ════════════════════════════════════════════════════════════════════════════
# Feuille 4 — Statut ADR & Stratégie paniers
# ════════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("ADR & Paniers")
freeze(ws4, "A3")

ws4.merge_cells("A1:E1")
t4 = ws4["A1"]
t4.value = "WildNexus P0 — ADR & paniers fournisseurs | Base v0.4, révision 2026-11-05 — achats gelés"
t4.font  = Font(bold=True, size=12, color="1F4E79")
t4.alignment = Alignment(horizontal="center", vertical="center")
ws4.row_dimensions[1].height = 22

adr_headers = ["ADR", "Sujet", "Statut documentaire", "Impact shortlist et réserves", "Lignes BOM"]
for c, h in enumerate(adr_headers, 1):
    cell = ws4.cell(row=2, column=c, value=h)
    style_header(cell)

adr_rows = [
    ("ADR-001", "ESP32-S3", "✅ Accepté", "A01/A19/A20 : références et variantes N8R8/N16R8 à contrôler", "A01, A19, A20"),
    ("ADR-002", "Caméra OV5640/IR", "✅ Accepté", "A02a/A02b/A18 : chaîne optique et IR à tester", "A02a, A02b, A18"),
    ("ADR-003", "LoRa P2P EU868", "✅ Accepté", "B02/B03 : gateway minimale P0 ; B10 banc seulement", "B02, B03, B10"),
    ("ADR-004", "Stockage local", "✅ Accepté", "A07 : microSD 128 GB ; référence et endurance à sélectionner", "A07"),
    ("ADR-005", "Alimentation AA + buck", "✅ Accepté", "A08–A10/A16 : SOP-10 suspendue, revue du schéma préalable", "A08–A10, A16"),
    ("ADR-006", "Boîtier IP67", "🟡 Proposé", "B04 : IP67 est une cible à tester, pas une certification acquise", "B04"),
    ("ADR-007", "Détection PIR", "✅ Accepté", "A05 : référence EKMB1203111 et présence physique à contrôler", "A05"),
    ("ADR-008", "Interfaces capteurs", "✅ Accepté", "A06 : micro TDK à identifier, interface non validée ; B05/B06 à tester", "A06, B05, B06"),
    ("ADR-009", "Architecture Sat/Base/Cloud", "✅ Accepté", "Pas d'achat Pi/cloud P0 ; gateway minimale à démontrer", "—"),
    ("ADR-010", "Sécurité, RGPD et Edge AI", "🟡 Accepté sous réserve", "Aucun média sur LoRa ; benchmark IA et revue juridique requis", "A01, A02b"),
    ("ADR-011", "Provisioning et cycle de vie des clés", "🟡 Proposé", "Procédure de provisioning et diversification à valider", "—"),
    ("ADR-012", "Stratégie de test P0", "✅ Accepté", "Tests hôte distincts des validations sur cible encore requises", "—"),
    ("ADR-013", "Couche acoustique", "✅ Accepté", "Deux micros à identifier ; stéréo, interface et pipelines à démontrer", "A06"),
    ("ADR-014", "Format payload LoRa", "✅ Accepté", "Contrat 48/16 octets à tester avec une gateway réelle", "B02, B03"),
    ("ADR-015", "Architecture plugin P1", "⚪ Backlog — non rédigé", "Hors P0 ; aucun achat associé", "—"),
    ("ADR-016", "Firmware intégré P0", "✅ Accepté", "Architecture documentaire ; GPIO, conflits et cycles à tester", "A01, A06"),
    ("ADR-017", "Métadonnées et fichiers audio", "✅ Accepté", "WAV/JSON et compatibilité des pipelines à vérifier sur fichiers réels", "A06, A07"),
    ("ADR-018", "Synchronisation temporelle", "⚪ Identifié — à rédiger", "Aucune synchronisation image/audio revendiquée ; aucun achat RTC P0", "—"),
]

for r, row in enumerate(adr_rows, 3):
    alt = (r % 2 == 0)
    ok  = "✅" in row[2]
    for c, val in enumerate(row, 1):
        cell = ws4.cell(row=r, column=c, value=val)
        style_cell(cell, alt=alt, ok=ok)

# Paniers fournisseurs
prow = len(adr_rows) + 4
ws4.merge_cells(f"A{prow}:F{prow}")
sub_t = ws4.cell(row=prow, column=1, value="Paniers historiques — rapprochement et autorisation JCH requis avant tout achat")
sub_t.font = Font(bold=True, color="FFFFFF")
sub_t.fill = SUB_FILL
sub_t.alignment = Alignment(horizontal="center", vertical="center")

panier_headers = ["Panier", "Fournisseur", "Composants", "Seuil port gratuit historique", "Priorité", "Note"]
for c, h in enumerate(panier_headers, 1):
    cell = ws4.cell(row=prow+1, column=c, value=h)
    style_header(cell, sub=True)

paniers = [
    ("P1", "Mouser BE", "A01, A04, A05, A06, A08, A10, A12, A17, B03, B05, B06", "≥50 € — à revalider", "⏸️ Gelé — rapprochement requis", "Commandes #39411684 et #39492997 à réconcilier avec factures et stock"),
    ("P2", "DigiKey BE", "A07 microSD 128 GB, référence/endurance à sélectionner ; A13 exclu", "≥50 € — à revalider", "⏸️ Gelé — rapprochement requis", "PPK2 reçu via Mouser #39411684 — ne pas racheter"),
    ("P3", "Arducam / Lensation", "A18 lentille M12 2.8 mm, B01 lentille IR 6 mm", "Devis à revalider", "⏸️ Gelé — rapprochement requis", "Contacter seulement après autorisation JCH"),
    ("P4", "Nordic Semi EU", "Aucun — A13 PPK2 déjà reçu", "Conditions à revalider", "⏸️ Gelé — rapprochement requis", "Ne pas racheter ; reçu via Mouser #39411684"),
    ("P5", "RAK Store EU", "B02 RAK3172-T EU868", "Conditions à revalider", "⏸️ Gelé — rapprochement requis", "Gateway et radio à valider selon WP05"),
    ("P6", "Soldered.com", "A19 NULA DeepSleep ESP32-S3", "Conditions à revalider", "⏸️ Gelé — rapprochement requis", "Référence, stock et consommation réelle à contrôler"),
    ("P7", "RS Belgium", "A09 suspendu SOP-10 ; B04 boîtier ; B07 presse-étoupe", "Conditions à revalider", "⏸️ Gelé — rapprochement requis", "Aucun montage A09 sans revue du schéma d'alimentation"),
    ("P8", "AliExpress", "A02a, A02b, A02c ; B10 LILYGO T-Beam", "Délais et conditions à revalider", "⏸️ Gelé — rapprochement requis", "B10 : revue WP05/réglementaire préalable ; vendeur officiel à vérifier"),
]

for r, row in enumerate(paniers, prow+2):
    alt = (r % 2 == 0)
    for c, val in enumerate(row, 1):
        cell = ws4.cell(row=r, column=c, value=val)
        style_cell(cell, alt=alt)

set_col_widths(ws4, [6, 22, 65, 24, 32, 45])

# ── Sauvegarde ─────────────────────────────────────────────────────────────
output = Path(__file__).resolve().parent / "WILDNEXUS_BOM_P0_v0.4.xlsx"
wb.save(output)
print(f"✅ BOM généré : {output}")
print(f"   Somme historique Option A : ~{total_a:.2f} €")
print(f"   Somme historique Option B : ~{total_b:.2f} €")
print(f"   Projection provisoire : ~{projection} € / 1 000 €")
print(f"   Réserve théorique : ~{reserve} €")
print("   Achats gelés : réconciliation et autorisation JCH requises.")
