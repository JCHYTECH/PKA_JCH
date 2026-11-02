"""
Génère le fichier Excel WildNexus BOM P0 v0.4
Mis à jour : 2026-06-16 — commandes A02a/b/c + A21 FTDI, +A02d P1, prix réels
"""
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
# Feuille 1 — Option A (Banc rapide) v0.2c
# ════════════════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "Option A — Banc rapide"
freeze(ws, "C3")

ws.merge_cells("A1:L1")
title = ws["A1"]
title.value = "WildNexus P0 — Option A : Banc rapide  |  Mis à jour : 2026-06-16 (v0.4)"
title.font  = Font(bold=True, size=12, color="1F4E79")
title.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 22

headers = ["#", "Composant", "Référence précise", "Fournisseur", "Qté",
           "Prix unit. TTC (est.)", "Total (est.)", "Délai", "Risque supply",
           "Statut", "Note", "Action requise"]
for c, h in enumerate(headers, 1):
    cell = ws.cell(row=2, column=c, value=h)
    style_header(cell)
ws.row_dimensions[2].height = 30

option_a = [
    ("A01", "MCU prototype", "ESP32-S3-DevKitC-1-N8R8 (8MB flash, 8MB PSRAM, USB-C)",
     "Mouser BE", 2, 16.00, 32.00, "3–5 j", "🟢 Bas", "⬜ À commander",
     "Acheter 2 pour banc M-02 redondant", "Commander groupé Mouser"),
    ("A02", "Caméra capteur (REJETÉ)", "Camemake CM_DVP_OV5640_UNIVERSAL — REJETÉ (MOQ 10)",
     "—", "—", "—", "—", "—", "—", "🔴 Rejeté",
     "Remplacé par A02a (ESP32-CAM) + A02b (OV5640 AliExpress)", "—"),
    ("A02a", "Caméra dév DVP 🆕", "Hailege 2pcs ESP32-CAM (OV2640 2MP DVP, LED flash, slot SD onboard)",
     "Amazon.de", 2, 12.50, 25.00, "2–3 j", "🟢 Bas", "✅ Commandé",
     "Outil DVP + SD onboard. Ne pas brancher OV5640 ici.", ""),
    ("A02b", "Caméra finale P0 🆕", "OV5640 DVP M12 24-pin 5MP (ref 1005005710463218, plage 1.8–12.8V → LDO probable)",
     "AliExpress", 4, 5.81, 23.24, "15–25 j", "🟡 Moyen", "✅ Commandé",
     "LDO probable (plage large). NoIR à confirmer réception.", ""),
    ("A02c", "Level shifter DVP proto 🆕", "Modules 8ch pré-assemblés (ref 1005010226529230, 3.3V↔1.8V)",
     "AliExpress", 2, 8.20, 16.39, "10–20 j", "🟢 Bas", "✅ Commandé",
     "Proto uniquement — remplacé par A02d SN74AVC16T245 en production.", ""),
    ("A03", "LED IR 850 nm (RETIRÉ)", "Vishay VSLY3850 — RETIRÉ (850nm perceptible faune)",
     "—", "—", "—", "—", "—", "—", "🔴 Retiré",
     "IR 940nm uniquement (A04)", "—"),
    ("A04", "LED IR 940 nm", "Vishay VSLB3940 (×4 par nœud)",
     "Mouser BE", 10, 0.37, 3.74, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel Mouser 0.37€/pièce", ""),
    ("A05", "PIR basse conso", "Panasonic EKMB1203111 (FOV 86°H×84°V, 2–3 µA, EKMB1303111 indispo)",
     "Mouser BE", 2, 22.30, 44.60, "5–8 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel 22.30€/pièce", ""),
    ("A06", "Micro MEMS I2S", "TDK MMICT5848-00-012 (I2S digital, remplace SPH0645 obsolète)",
     "Mouser BE", 3, 2.04, 6.12, "3–7 j", "🟢 Bas", "✅ Commandé #39492997",
     "Remplacement Knowles SPH0645LM4H-B (obsolète)", ""),
    ("A07", "microSD", "M-02 : SanDisk Extreme 32GB (~10€) / M-03 : Swissbit pSLC SFSD016GN1AM1TB-E (~49€)",
     "Local / Amazon", 3, 10.00, 30.00, "Immédiat", "🟢 Bas", "⬜ Banc → consumer OK. Terrain → Swissbit",
     "NE PAS acheter microSD no-name", "Commander Swissbit pour M-03"),
    ("A08", "Buck faible Iq", "TPS62840DLCR (Iq 60 nA, 2.5–5.5V → 3V, 750mA)",
     "Mouser BE", 5, 1.85, 9.25, "3–5 j", "🟢 Bas", "✅ Commandé #39492997 (5 dispo, 5 backlog)",
     "Prix réel Mouser 2026-06-12 : 1.85€/pièce", ""),
    ("A09", "Holder AA × 4", "Keystone 2463 (4× AA, 6V, fils) — 2 holders/nœud",
     "RS Belgium / Mouser BE", 4, 3.50, 14.00, "3–7 j", "🟢 Bas", "⬜ À commander",
     "2 holders × 4 AA = 8 AA en 2 blocs parallèles (4S2P)", ""),
    ("A10", "Inductance buck", "Würth 744043100 (10 µH, 1 A, 3×3 mm)",
     "Mouser BE", 5, 1.31, 6.55, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel Mouser 1.31€/pièce", ""),
    ("A11", "Passifs CMS", "Lot 0402/0603 : C 100nF/10µF/1µF ; R 10K/100K/1M",
     "Mouser BE", 1, 20.00, 20.00, "3–5 j", "🟢 Bas", "⬜ À commander",
     "Lot prototypage — couvre buck, micro, PIR, LED driver", ""),
    ("A12", "MOSFET power gating", "Vishay SI2302CDS-T1-GE3 (N-ch, SOT-23, 20V)",
     "Mouser BE", 5, 0.71, 3.55, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel Mouser 0.71€/pièce. OBLIGATOIRE — OV5640 standby consomme.", ""),
    ("A13", "Nordic PPK2", "Nordic Power Profiler Kit II (NRF-PPK2)",
     "Mouser BE / Nordic EU", 1, 83.57, 83.57, "5–10 j", "🟢 Bas", "✅ Reçu Mouser #39411684",
     "⚠️ Non négociable — sans PPK2, ADR-005 non vérifiable", ""),
    ("A14", "Breadboard + Dupont", "Kit proto 830 pts + câbles — Miuzei Kit (reçu 2026-06-10)",
     "—", "—", "—", "—", "—", "—", "✅ Reçu",
     "Déjà reçu", ""),
    ("A15", "Alimentation labo (RETIRÉ)", "RETIRÉ — PPK2 fait source + mesure",
     "—", "—", "—", "—", "—", "—", "🔴 Retiré",
     "Économie 35€", ""),
    ("A16", "Piles AA lithium", "Energizer Ultimate Lithium L91 AA × 16",
     "Carrefour / Action / Amazon", 16, 1.80, 29.00, "Immédiat", "🟢 Bas", "⬜ À acheter",
     "16 piles = 2 nœuds 8 AA chacun", ""),
    ("A17", "Dissipateur OV5640 🆕", "ATS-HK127-R0 ou mini radiateur alu 14×14×5mm",
     "Mouser BE", 4, 1.31, 5.24, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "OV5640 chauffe en actif. Prévenir throttling en boîtier.", ""),
    ("A18", "Lentille M12 2.8mm 🆕", "Objectif M12 2.8mm NoIR f/1.8, champ ~90-100°",
     "Arducam / Lensation", 2, 25.00, 50.00, "5–10 j", "🟡 Moyen", "⬜ À commander",
     "Tests comparatifs focaux : 2.8mm (coulée) vs 6mm (télé)", ""),
    ("A19", "ESP32-S3 basse conso 🆕", "NULA DeepSleep ESP32-S3 (WROOM-1-N8R8, 7µA deep sleep)",
     "Soldered.com (Croatie)", 1, 25.00, 25.00, "5–10 j", "🟢 Bas", "⬜ À commander",
     "Mesure deep sleep réel hors overhead DevKit. Ajout 2026-06-16.", ""),
    ("A20", "Breakout nu ESP32-S3 🆕", "Freenove Breakout Board WROOM/WROVER + module ESP32-S3-WROOM-1",
     "Amazon.de / Freenove", 1, 15.00, 15.00, "3–7 j", "🟢 Bas", "⬜ À commander",
     "Alternative éco à NULA. Mesure module nu. FTDI externe requis.", ""),
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
sub.value = "Sous-total Option A"
sub.font  = Font(bold=True, color="FFFFFF")
sub.fill  = PatternFill("solid", fgColor="2E75B6")
sub.alignment = Alignment(horizontal="right", vertical="center")
tot = ws.cell(row=r_sub, column=7, value=f"~{total_a:.0f} €")
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
t2.value = "WildNexus P0 — Option B : Additions terrain compact  |  2026-06-16 (v0.4)"
t2.font  = Font(bold=True, size=12, color="1F4E79")
t2.alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 22

for c, h in enumerate(headers, 1):
    cell = ws2.cell(row=2, column=c, value=h)
    style_header(cell)
ws2.row_dimensions[2].height = 30

option_b = [
    ("B01", "Lentille M12 IR-corrigée", "Lensation LS-6028 f/1.8 6mm / Evetar M12B0618W-IR",
     "Lensation.de", 2, 40.00, 80.00, "5–10 j", "🟡 Moyen", "⬜ Après M-02",
     "Ne pas descendre sous 30€/lentille. Demander devis.", "Devis obligatoire"),
    ("B02", "Module LoRa P0", "RAK3172-T EU868 (SX1262, CE, IPEX, −40/+85°C)",
     "RAK Store EU", 2, 14.00, 28.00, "5–10 j", "🟢 Bas", "⬜ Après M-02",
     "Vérifier EU868 + IPEX explicite", ""),
    ("B03", "Antenne LoRa 868 MHz", "Molex 211140-0100 (flex, IPEX, ~100mm)",
     "Mouser BE", 2, 2.15, 4.30, "3–7 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel Mouser 2.15€/pièce", ""),
    ("B04", "Boîtier IP67 P0", "Hammond 1554A (150×100×60mm) ABS/IP67",
     "RS Belgium / Mouser", 2, 16.00, 32.00, "3–7 j", "🟡 Moyen", "⬜ Après layout A",
     "Commander après layout validé", ""),
    ("B05", "BME688 capteur env.", "Bosch BME688 (T/P/H/gaz, I2C/SPI)",
     "Mouser BE", 2, 7.44, 14.88, "3–7 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel Mouser 7.44€/pièce", ""),
    ("B06", "SHT31-DIS humidité", "Sensirion SHT31-DIS-B (±2% RH, I2C)",
     "Mouser BE", 2, 3.87, 7.74, "3–5 j", "🟢 Bas", "✅ Commandé #39492997",
     "Prix réel Mouser 3.87€/pièce", ""),
    ("B07", "Connecteur étanche", "Presse-étoupe M16 IP68 nylon ×4",
     "RS Belgium / Mouser", 4, 2.00, 8.00, "3–7 j", "🟢 Bas", "⬜ Après layout",
     "Passage câble sangle/antenne", ""),
    ("B08", "Silica gel + joints", "Sachets 5g silica gel ×10 + joint torique EPDM 140×3",
     "Conrad / Amazon", 1, 10.00, 10.00, "Immédiat", "🟢 Bas", "⬜ À acheter",
     "Maintenance terrain", ""),
    ("B09", "Sangle UV terrain", "Sangle polyester UV 20mm × 50cm + boucle inox",
     "Conrad / Camping", 4, 4.00, 16.00, "Immédiat", "🟢 Bas", "⬜ À acheter",
     "Fixation tronc", ""),
    ("B10", "Station base LoRa 🆕", "LILYGO T-Beam SUPREME 1W (SX1262, +32dBm, ESP32-S3, GPS, 868MHz)",
     "LILYGO / AliExpress", 1, 35.00, 35.00, "10–15 j", "🟡 Moyen", "⬜ Après M-02",
     "Station base haute puissance. Vérifier variante EU868.", ""),
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
sub2.value = "Sous-total Option B"
sub2.font  = Font(bold=True, color="FFFFFF")
sub2.fill  = PatternFill("solid", fgColor="2E75B6")
sub2.alignment = Alignment(horizontal="right", vertical="center")
tot2 = ws2.cell(row=r_sub2, column=7, value=f"~{total_b:.0f} €")
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
t3.value = "WildNexus P0 — Budget consolidé  |  Enveloppe : 1 000 €  |  2026-06-16 (v0.4)"
t3.font  = Font(bold=True, size=12, color="1F4E79")
t3.alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 22

total_ab = total_a + total_b
port = 55
marge = 80
reserve = 1000 - total_ab - port - marge

budget_rows = [
    ("Bloc", "v0.1", "v0.4 (prix réels)", "Note", True),
    (f"Option A — Banc rapide", "~396 €", f"~{total_a:.0f} €", "+A19-A21, commandes 2026-06-16, prix réels", False),
    (f"Option B — Additions terrain", "~203 €", f"~{total_b:.0f} €", "+B10 (LILYGO T-Beam)", False),
    ("Frais de port (4–5 colis)", "~50 €", f"~{port} €", "Mouser + DigiKey + RAK + Lensation + Nordic + Soldered", False),
    ("Marge casse / reprise", "~80 €", f"~{marge} €", "", False),
    ("TOTAL estimé A + B", "~729 €", f"~{total_ab + port + marge} €", "⚠️ Sous seuil 900 €", True),
    ("Réserve restante (enveloppe 1 000 €)", "~271 €", f"~{reserve} €",
     "✅ Budget tenu" if reserve > 0 else "🔴 DÉPASSEMENT", True),
]

for r, (label, est, rev, note, bold) in enumerate(budget_rows, 2):
    is_hdr = bold and r == 2
    for c, val in enumerate([label, est, rev, note], 1):
        cell = ws3.cell(row=r, column=c, value=val)
        if is_hdr:
            style_header(cell)
        elif bold and ("TOTAL" in label or "Réserve" in label):
            cell.font = TOTAL_FONT
            if "Réserve" in label and reserve < 0:
                cell.fill = RED_FILL
            elif "Réserve" in label:
                cell.fill = OK_FILL
        else:
            alt = (r % 2 == 0)
            style_cell(cell, alt=alt)

set_col_widths(ws3, [28, 18, 22, 55])

# ════════════════════════════════════════════════════════════════════════════
# Feuille 4 — Statut ADR & Stratégie paniers
# ════════════════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("ADR & Paniers")
freeze(ws4, "A3")

ws4.merge_cells("A1:E1")
t4 = ws4["A1"]
t4.value = "WildNexus P0 — Statut ADR & Stratégie paniers fournisseurs  |  2026-06-16 (v0.4)"
t4.font  = Font(bold=True, size=12, color="1F4E79")
t4.alignment = Alignment(horizontal="center", vertical="center")
ws4.row_dimensions[1].height = 22

adr_headers = ["ADR", "Sujet", "Statut", "Impact shortlist", "Lignes BOM"]
for c, h in enumerate(adr_headers, 1):
    cell = ws4.cell(row=2, column=c, value=h)
    style_header(cell)

adr_rows = [
    ("ADR-001", "ESP32-S3",            "✅ Accepté", "A01 — DevKit + A19 NULA + A20 Freenove", "A01, A19, A20"),
    ("ADR-002", "Caméra OV5640/IR",    "✅ Accepté", "A02a ESP32-CAM + A02b OV5640 + A18 lentille", "A02a, A02b, A18"),
    ("ADR-003", "LoRa P2P EU868",      "✅ Accepté", "B02 RAK3172-T + B03 antenne + B10 T-Beam", "B02, B03, B10"),
    ("ADR-004", "microSD industrielle", "✅ Accepté", "A07 Swissbit DigiKey", "A07"),
    ("ADR-005", "AA + buck faible Iq", "✅ Accepté", "A08–A10 buck/inductance + A09 holders + A16 piles", "A08–A10, A16"),
    ("ADR-006", "Boîtier IP67",        "✅ Accepté", "B04 Hammond P0 ; impression 3D organique P1 hors budget", "B04"),
    ("ADR-007", "Détection PIR",       "✅ Accepté", "A05 EKMB1203111", "A05"),
    ("ADR-008", "Capteurs extensible", "✅ Accepté", "A06 TDK mic + B05 BME688 + B06 SHT31", "A06, B05, B06"),
    ("ADR-009", "Architecture Sat/Base/Cloud", "✅ Accepté", "Pas d'achat Pi/cloud P0", "—"),
    ("ADR-010", "Edge AI",             "✅ Accepté", "A01 ESP32-S3 + caméra", "A01, A02b"),
]

for r, row in enumerate(adr_rows, 3):
    alt = (r % 2 == 0)
    ok  = "✅" in row[2]
    for c, val in enumerate(row, 1):
        cell = ws4.cell(row=r, column=c, value=val)
        style_cell(cell, alt=alt, ok=ok)

# Paniers fournisseurs
prow = len(adr_rows) + 4
ws4.merge_cells(f"A{prow}:E{prow}")
sub_t = ws4.cell(row=prow, column=1, value="Stratégie paniers fournisseurs (commande groupée)")
sub_t.font = Font(bold=True, color="FFFFFF")
sub_t.fill = SUB_FILL
sub_t.alignment = Alignment(horizontal="center", vertical="center")

panier_headers = ["Panier", "Fournisseur", "Composants", "Seuil port gratuit", "Priorité", "Note"]
for c, h in enumerate(panier_headers, 1):
    cell = ws4.cell(row=prow+1, column=c, value=h)
    style_header(cell, sub=True)

paniers = [
    ("P1", "Mouser BE",       "A01 MCU, A04 IR, A05 PIR, A06 mic, A08 buck, A10 induct, A12 MOSFET, A17 dissip, B05 BME688, B06 SHT31, B03 antenne", "≥50 €", "🔴 En premier", "Déjà commandé #39411684 + #39492997"),
    ("P2", "DigiKey BE",      "A07 microSD Swissbit, A13 PPK2 (si pas Mouser)", "≥50 €", "🔴 En premier", "PPK2 déjà reçu Mouser"),
    ("P3", "Arducam / Lensation", "A18 lentille M12 2.8mm, B01 lentille IR 6mm", "Devis requis", "🟡 Après M-02 banc", "Contacter avant paiement"),
    ("P4", "Nordic Semi EU",  "A13 PPK2 (si pas Mouser)", "Direct UE", "🔴 En premier", "Déjà reçu Mouser"),
    ("P5", "RAK Store EU",    "B02 RAK3172-T EU868", "Direct UE", "🟡 Après M-02 banc", ""),
    ("P6", "Soldered.com",    "A19 NULA DeepSleep ESP32-S3", "Direct UE (Croatie)", "🔴 En premier", "Ajout 2026-06-16"),
    ("P7", "RS Belgium",      "A09 holders AA, B04 boîtier Hammond, B07 presse-étoupe", "Livraison BE", "🟡 Après layout A validé", ""),
    ("P8", "AliExpress",      "A02a ESP32-CAM, A02b OV5640, A02c level shifter, B10 LILYGO T-Beam", "Varie", "🟡 Commander tôt (délais longs)", "Vérifier vendeur officiel LILYGO"),
]

for r, row in enumerate(paniers, prow+2):
    alt = (r % 2 == 0)
    for c, val in enumerate(row, 1):
        cell = ws4.cell(row=r, column=c, value=val)
        style_cell(cell, alt=alt)

set_col_widths(ws4, [6, 22, 65, 20, 18, 35])

# ── Sauvegarde ─────────────────────────────────────────────────────────────
output = "/Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/WILDNEXUS_BOM_P0_v0.4.xlsx"
wb.save(output)
print(f"✅ BOM généré : {output}")
print(f"   Option A : ~{total_a:.0f} €")
print(f"   Option B : ~{total_b:.0f} €")
print(f"   Budget total : ~{total_ab + port + marge} € / 1 000 €")
print(f"   Réserve : ~{reserve} €")
