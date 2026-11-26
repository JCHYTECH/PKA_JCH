---
tags:
  - type/project
  - status/active
---
# Epson ET-8550_Workflow.md — Color Management Fix
## Premium Glossy Photo Paper / macOS / Epson Print Layout
[[Accès_au_driver_Mac_de]]
---
[[ET8550 Excès_de_magenta_dans_la]]
## Root Cause

**Auto Select** for the ICC profile in Print Layout silently picks the wrong profile when paper type is mismatched or unknown, causing color shifts without any user action.

---

## Correct Settings in Print Layout

| Parameter | Value |
|---|---|
| Color Type | Use ICC Profile |
| ICC Profile | `JN_E_ET8550_EpsonPremiumGlossyPhotoPaper_EPG_High` |
| Rendering Intent | Perceptual |
| Black Point Compensation | On |
| Media Type | Epson Premium Glossy |
| Quality | High |

---

## ICC Profile Installation

1. Download free profile from: **jimmynordstrom.se** (ET-8550 section)
2. File: `JN_E_ET8550_EpsonPremiumGlossyPhotoPaper_EPG_High.icm`
3. Double-click the `.icm` file — installs to `~/Library/ColorSync/Profiles/`
4. Restart Epson Print Layout
5. Select the profile manually in Color Settings (do not use Auto Select)

---

## macOS-Specific Risks

### AirPrint Driver Replacement
macOS system updates silently replace the Epson driver with [[Apple]]'s generic AirPrint driver. AirPrint does not handle custom ICC profiles correctly.

**Check:** System Settings > Printers — driver must say **Epson**, not AirPrint.

**Fix if AirPrint:** Remove printer, reinstall Epson driver, re-add printer, reboot.

### ColorSync
Do not set ColorSync to **Managed by Printer** — this bypasses your ICC profile and hands color control back to Epson's internal profiles.

---

## General Rule

Color management must be handled in **one place only**. If Print Layout manages color (Use ICC Profile), the source application must be set to **No Color Management** or **Printer Manages Colors** — not both active simultaneously.

---

## Preference File Locations (if reset needed)

```
~/Library/Preferences/com.epson.PrintLayout*
~/Library/Application Support/EPSON/PrintLayout/
~/Library/Containers/com.epson.PrintLayout*/
~/Library/Caches/com.epson.PrintLayout*
```
