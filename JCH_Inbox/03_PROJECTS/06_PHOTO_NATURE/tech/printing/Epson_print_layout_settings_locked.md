---
tags:
  - type/project
  - status/active
---
# Epson print layout settings locked

**Created:** 2026-04-07  
**Updated:** 2026-04-09  
**Messages:** 13

---

## Human
*2026-04-07 07:58*

Using [[Epson]] print layout it seems that somewhere settings are saved and block any further modification. Can you see if something is wrong in setup or int presence of temporary files

---

## Assistant
*2026-04-07 07:58*

```
This block is not supported on your current device yet.
```

I don't have direct access to your Mac's filesystem or running processes from here — the browser tools I have don't cover that. But I can walk you through the likely culprits for [[**Epson Print Layout**]] locking settings.

**Where [[Epson Print Layout]] stores its preferences on macOS:**

The most common locations for corrupted or locked preference files:

```
~/Library/Preferences/com.epson.PrintLayout*.plist
~/Library/Application Support/EPSON/PrintLayout/
~/Library/Containers/com.epson.PrintLayout*/
```

**What to try:**

1. **Quit Epson Print Layout completely** (check Activity Monitor to be sure — it sometimes has background processes).

2. **Delete the preference files:**
   ```bash
   rm ~/Library/Preferences/com.epson.PrintLayout*
   ```
   Or move them to Desktop first if you want to be cautious.

3. **Check the Containers folder** — if Epson Print Layout is sandboxed (Mac App Store version), its data lives here:
   ```bash
   ~/Library/Containers/
   ```
   Look for any folder with "epson" or "PrintLayout" in the name, open it, and delete the `Data/Library/Preferences/` contents.

4. **Temporary/cache files:**
   ```bash
   ~/Library/Caches/com.epson.PrintLayout*
   ```

**One specific issue worth checking:** Epson Print Layout has a known behavior where **media type or paper size settings get saved as a "last used" profile** and override manual changes. Check under *File > Page Setup* — if a custom preset is saved there, it can silently override the Print Layout panel settings.

Can you describe more precisely what's being blocked — is it paper size, color settings, media type, or something else? That would narrow it down.

---

## Human
*2026-04-07 07:59*

print colors are not changed or worst modified without request

---

## Assistant
*2026-04-07 07:59*

Color management conflicts are the most likely cause here. There are several layers that can interfere, and they often fight each other silently.

**The core problem: too many systems trying to manage color at once**

When colors print incorrectly or change without apparent reason, it's almost always one of these:

---

**1. Color management set in multiple places simultaneously**

This is the #1 culprit. Check that color management is handled in **only one place**:

- In **Epson Print Layout**: go to *Color Management* and check what's selected — it should be either *Epson Color Controls* or *ICM/ColorSync*, not both active in some way.
- In your **source application** (Photoshop, Lightroom, etc.): if *that* app is also applying a color profile, you get double conversion. Set it to *No Color Management* or *Printer Manages Colors* — whichever is the opposite of what Print Layout is doing.

The rule: **one system manages color, all others hand off**.

---

**2. macOS ColorSync intervening**

macOS ColorSync can silently remap colors if no explicit profile is assigned. Check:
- Open **ColorSync Utility** (in /Applications/Utilities/)
- Go to *Devices* > find your Epson printer > check what profile is assigned
- If it's set to something unexpected, that's your interference

---

**3. Saved Print Presets overriding your settings**

In the macOS Print dialog, any saved preset takes priority. When you open Print Layout, check:
- *File > Page Setup* — delete any custom presets and reset to defaults
- In the Print dialog itself, check the preset dropdown — set it to *Last Used Settings* or *Default* to rule this out

---

**4. Epson Print Layout "Color Mode" auto-switching**

Print Layout has a feature where selecting certain paper types (e.g., Epson Ultra Premium Photo Paper) automatically switches the color mode. If your paper type setting is wrong or keeps reverting, this can silently change color rendering.

---

**To isolate the issue:**

What is your workflow? Specifically — what application are you printing *from* (Lightroom, Photoshop, direct from Print Layout), and what color mode do you have selected in Print Layout when you notice the change?

---

## Human
*2026-04-07 08:06*

direct and where is color mode I see only collor setting

---

## Assistant
*2026-04-07 08:06*

"Color Setting" is the correct label in Print Layout — that's not a problem. The terminology varies by version.

A screenshot would help a lot here. Can you take a screenshot of the Print Layout window showing the Color Setting panel and paste it here? That way I can see exactly what options are visible and what's currently selected, rather than guessing at your specific version's layout.

In the meantime — when you say colors are modified without request, can you be more precise:

- **When** does the change happen — when you switch paper type, when you reopen the app, when you hit print?
- **What changes** — overall cast (too warm, too cool), saturation shift, or something else?
- **Which printer** model is this on?

---

## Human
*2026-04-07 08:08*

color settings/ Type : Use ICC Profile/ICC profile : Auto selecr/rendering intent : Perceptual/Black point compensation is on

---

## Assistant
*2026-04-07 08:08*

That configuration is the problem, specifically **"Auto Select" for the ICC profile**.

**Why "Auto Select" is unreliable:**

When set to Auto, Print Layout picks the ICC profile based on the paper type selected in the Media Settings panel. If the paper type is even slightly wrong, or if Print Layout doesn't have an exact match for your paper, it either picks the wrong profile or falls back to a generic one — silently. You get a color shift without touching any color setting yourself.

**What you should do:**

1. **Set the ICC profile explicitly** — don't let it auto-select. Choose the exact profile that matches your paper. Epson profiles follow a naming convention like `SPxxxxxx_PremiumLuster` etc. — the profile name should match your printer model + paper combination exactly.

2. If you don't have the right profile installed, download it from Epson's site for your specific printer model and paper type, install it (double-click the `.icc` file on macOS, it goes into `~/Library/ColorSync/Profiles/`), then restart Print Layout.

3. **Rendering intent Perceptual** is a reasonable choice for photos — no issue there.

4. **Black Point Compensation on** is also standard — leave it.

---

**The other risk with your current setup:**

"Use ICC Profile" means Print Layout is doing the color conversion. That's correct — but only if your source application is sending a properly tagged image with an embedded profile (sRGB or AdobeRGB typically). If the source file has no embedded profile, the conversion starts from an undefined state and results are unpredictable.

What printer model, and what paper are you using?

---

## Human
*2026-04-07 08:10*

ET8550 epson premium glossy

---

## Assistant
*2026-04-07 08:10*

The ET-8550 with Epson Premium Glossy Photo Paper is a well-defined combination. Epson provides a specific ICC profile for it.
```
This block is not supported on your current device yet.
```

Good — there is a specific ICC profile for your exact combination. Here's what to do:

**The profile you need:**

The profile for Epson Premium Glossy Photo Paper on the ET-8550 is `JN_E_ET8550_EpsonPremiumGlossyPhotoPaper_EPG_High.icm`, with Media Type set to **Epson Premium Glossy** and Quality set to **High**. It's available free from jimmynordstrom.se.

**Two additional issues specific to the ET-8550 on macOS worth knowing:**

1. macOS system updates can silently replace the official Epson driver with [[Apple]]'s generic AirPrint driver. When this happens, custom ICC profiles stop working correctly. The fix is to remove the printer, reinstall the Epson driver, re-add the printer, and reboot.

2. You do not want "Managed by Printer" selected in ColorSync — that passes color control to Epson's own printer profiles rather than your chosen ICC profile.

**Steps:**

1. Download the profile from jimmynordstrom.se
2. Double-click the `.icm` file — it installs into `~/Library/ColorSync/Profiles/`
3. Restart Print Layout
4. In Color Settings: change ICC Profile from **Auto Select** to the specific `JN_E_ET8550_EpsonPremiumGlossyPhotoPaper_EPG_High` profile
5. Make sure your Media Type in Print Layout is set to **Epson Premium Glossy**

Also worth verifying: open **System Settings > Printers** and confirm the driver listed for your ET-8550 is the Epson driver, not AirPrint. If it says AirPrint, that's a separate problem that needs fixing first.

---

## Human
*2026-04-09 06:06*

Summarize in .md

---

## Assistant
*2026-04-09 06:07*

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

All the key points in one file — driver check, profile install, and the correct Print Layout settings.

---

## Assistant
*2026-04-09 06:08*

```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Done. The file covers root cause, correct settings table, profile installation steps, macOS-specific risks, and preference file paths for a reset if needed.

---
