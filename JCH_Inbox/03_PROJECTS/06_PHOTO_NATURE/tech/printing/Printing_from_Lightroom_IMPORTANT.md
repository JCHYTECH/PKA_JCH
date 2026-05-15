---
tags:
  - type/project
  - status/active
---
# Printing from Lightroom IMPORTANT

**Created:** 2026-03-29 09:09  
**Updated:** 2026-03-29 09:16  
**Messages:** 9

---

## Human
*2026-03-29 09:09*

it is better to use directly printing panel of Lightroom or photoshop instead of using EPL ?

---

## Assistant
*2026-03-29 09:09*

Je vérifie rapidement les fonctions actuelles d’Epson Print Layout et des panneaux d’impression Adobe, puis je te donne une recommandation pratique pour ton cas ET8550 sur Mac.

---

## Assistant
*2026-03-29 09:09*

Yes—**for your case, I would generally prefer printing directly from Lightroom Classic or Photoshop rather than through Epson Print Layout**.

The key point is that **print quality is not inherently better with EPL**. What matters is a clean color-managed workflow with the correct ICC profile, correct paper setting, and only one color manager in the chain. Epson says EPL supports ICC-based color management, but Adobe’s print workflows also do this directly, including printer/paper profile selection and soft proofing. citeturn253356search4turn253356search8turn253356search2turn253356search5turn253356search13

For **your ET-8550 on Mac**, direct printing from Adobe is usually the safer choice because it gives you a more explicit path: in Photoshop you can set **“Photoshop Manages Colors”** and choose the exact printer profile; in Lightroom Classic you can choose the output profile in the **Print Job > Color Management** section. Adobe also ties this cleanly to soft proofing, so the profile used for preview matches the one used for print conversion. citeturn253356search2turn253356search5turn253356search13turn253356search14

In practical terms, **EPL is more useful for Epson-specific layout convenience**, previewing borders, panoramas, canvas options, and some simplified print handling. But since you have already seen confusing behavior with settings resetting on the Mac driver side, EPL adds one more layer where things can become opaque. In that situation, printing straight from Lightroom or Photoshop usually means **fewer hidden variables**. citeturn253356search4turn253356search8turn253356search3

My recommendation would be this: use **Lightroom Classic** when you want the most repeatable workflow from catalog to soft proof to print, especially for normal photo printing and series of images. Use **Photoshop** when you have done detailed local retouching and want to print a final master file with maximum control. Keep **EPL** mainly for special layout needs, not as your default route. citeturn253356search17turn253356search2turn253356search18

So the conclusion is simple: **for color reliability, I would choose Lightroom or Photoshop direct print over EPL on your setup**.

For you, the best order is:
1. Soft proof with the exact paper ICC.
2. Print from Lightroom or Photoshop with app-managed color.
3. In the Epson driver, use the correct media type and disable any extra color correction / vivid enhancement. Epson’s Mac documentation confirms color management can be adjusted or turned off in the printer software. citeturn253356search13turn253356search2turn253356search3

I can give you a **Mac-specific step-by-step workflow for Lightroom Classic direct printing with ET-8550**, including the exact settings to lock down the magenta/saturation problem.

---

## Human
*2026-03-29 09:10*

ok

---

## Assistant
*2026-03-29 09:10*

Je rassemble les réglages officiels Adobe/Epson pour te donner une séquence propre, centrée Mac + ET-8550, sans repasser par EPL.

---

## Assistant
*2026-03-29 09:11*

Good. Here is the workflow I would use as the **default route on your Mac with the ET-8550**. In practice, use **Lightroom Classic for routine printing** and switch to **Photoshop only for images you finished in Photoshop**. That gives you the clearest color-managed path and avoids the extra ambiguity of EPL. This is an inference from Adobe’s and Epson’s documented workflows rather than a claim that EPL is “worse” in absolute terms. citeturn473673view2turn365308view0turn579606view1

1. Prepare the file in Lightroom Classic, then soft-proof before printing. In the Develop module, enable **Soft Proofing** and choose the **exact ICC profile** for the ET-8550 + the paper you will actually use. Adobe recommends using the same ICC profile later in the Print module, and Lightroom can show out-of-gamut areas during proofing. If the profile does not appear, add it via **Profile > Other**. citeturn473673view1turn365308view1

2. In the Print module, set **Print To: Printer**. Start with Lightroom’s default **240 ppi**, which Adobe says is satisfactory for most high-end inkjet prints. Keep **Draft Mode Printing off**, because Draft Mode disables Lightroom’s color management and print sharpening. For sharpening, start conservatively: **Low** or **Standard**, and choose **Glossy** if you are on glossy/luster/semigloss paper, or **Matte** for matte/art papers. citeturn473673view0turn473673view2

3. In **Print Job > Color Management**, choose the **specific printer/paper ICC profile**, not “Managed by Printer,” when you want Lightroom to handle the conversion. Adobe explicitly warns that if Lightroom uses a custom printer profile, color management must be turned off in the printer driver to avoid double conversion. For rendering intent, start with **Relative** when the image has few out-of-gamut colors, and test **Perceptual** when the file contains many saturated colors such as strong blues or greens. citeturn473673view0turn473673view1

4. Then click **Printer…** and set the Mac/Epson driver correctly. Epson’s Mac documentation says that color management is controlled in the print dialog via **Color Matching** and **Color Options**. On **macOS 13 or later**, this is under **Printer Options > Color Matching** and then **Color Options**; on **macOS 12 or earlier**, those appear directly in the print-window pop-up menu. To let Lightroom manage color, choose **EPSON Color Controls**, then under **Color Options** set **Off (No Color Adjustment)**. Epson states that this turns off printer-side color management so the application alone manages color, and that an ICC profile is then required. citeturn579606view1turn859446view0

5. In that same Epson dialog, make sure the **media type matches the paper family** you are actually using. Also avoid Epson’s automatic enhancement modes such as **EPSON Vivid**, **Fix Photo**, or manual color adjustments for this workflow, because those are printer-side corrections and defeat a clean application-managed pipeline. citeturn859446view0

6. If you print from Photoshop instead, the equivalent path is straightforward: **File > Print > Color Management > Photoshop Manages Colors**, then choose the matching **Printer Profile** for that exact paper. Adobe says this often gives the best results when you have a custom profile for a specific printer/ink/paper combination. On Mac, Photoshop also offers **Send 16-bit Data** for the highest possible quality in smooth tonal transitions. After that, enter the Epson print settings and again turn off printer color management there. citeturn365308view0turn365308view2

So the practical rule is this: **Lightroom Classic = default print path**, **Photoshop = final master print path**, **EPL = only when you specifically need Epson’s layout conveniences**. For your magenta/saturation issues, the single most important point is still the same: **one color manager only**. Adobe and Epson both document that double color handling causes incorrect output. citeturn473673view0turn365308view0turn859446view0

A compact “safe preset” for you would be:

- Lightroom soft proof with the exact paper ICC  
- Print module: same ICC, Draft Mode off  
- 240 ppi to start  
- Print sharpening: Low or Standard  
- Epson driver: correct media type  
- Epson Color Controls > Color Options > **Off (No Color Adjustment)** citeturn473673view0turn473673view2turn859446view0

11:25 — Brussels time.

I can now give you the **exact ET-8550 Mac settings for Epson Premium Glossy and for a matte/baryta paper**, as two ready-to-use checklists.

---

## Human
*2026-03-29 09:12*

ok

---

## Assistant
*2026-03-29 09:12*

Je prépare deux checklists prêtes à l’emploi pour ton ET-8550 sur Mac: une pour Epson Premium Glossy, une pour baryté/matte, avec les seuls réglages qui comptent vraiment.

---

## Assistant
*2026-03-29 09:13*

Parfait. Voici les réglages de départ que je te conseille pour **l’ET-8550 sur Mac en impression directe depuis Lightroom Classic**. Le principe reste identique dans Photoshop. Dès que Lightroom gère la couleur avec un profil ICC, Adobe recommande de **désactiver la gestion couleur dans le driver**, et Epson indique que cela se fait via **Color Matching > EPSON Color Controls**, puis **Color Options > Off (No Color Adjustment)**. Sur macOS 13+, ces menus sont dans **Printer Options**. citeturn679175search0turn936403view0turn936403view1

Pour **Epson Premium Photo Paper Glossy**, prends ce preset de base. Dans Lightroom : **Soft Proofing** avec le profil ICC du papier exact, puis dans **Print Job** choisis le même profil ICC, **Draft Mode Printing off**, **240 ppi** pour commencer, et **Print Sharpening = Low ou Standard / Glossy**. Dans le driver Epson sur Mac : **Media Type = Premium Photo Paper Glossy**, puis **EPSON Color Controls > Off (No Color Adjustment)**. L’ET-8550 associe explicitement ce papier au type de support **Premium Photo Paper Glossy** dans le logiciel d’impression. citeturn679175search18turn679175search0turn936403view1turn936403view2

Pour ce papier glossy, mon point de départ visuel serait : **saturation légèrement réduite**, surtout dans les bleus, et prudence sur la vibrance. Le glossy renforce naturellement l’impact visuel, donc si ton fichier est déjà “fort”, le tirage peut vite devenir trop dense ou trop saturé. C’est un conseil pratique de workflow de tirage, pas une règle imposée par Epson. 

Pour le **matte**, il faut distinguer deux cas. Si tu utilises un papier type **Presentation Matte / Premium Presentation Matte**, dans Lightroom tu gardes exactement la même logique ICC, mais dans le driver tu choisis **Presentation Paper Matte** ou **Premium Presentation Paper Matte** selon le papier exact. L’ET-8550 expose bien ces deux types de support séparément. En matte, je partirais avec **Print Sharpening = Standard / Matte**, souvent plus adapté que Low. citeturn936403view2turn679175search18

Pour le **baryté**, je te conseille de ne pas le traiter comme un matte. Sur l’ET-8550, les familles de supports disponibles les plus proches d’un baryté photo sont plutôt **Ultra Premium Photo Paper Luster** et **Premium Photo Paper Semi-Gloss**. Donc, avec un baryté tiers, la bonne méthode est : **utiliser le profil ICC du fabricant du papier et suivre son media type recommandé** ; à défaut, commence par **Ultra Premium Photo Paper Luster**, puis teste **Premium Photo Paper Semi-Gloss** si le rendu est trop dur ou pas assez juste. C’est une recommandation de départ fondée sur les types de support que l’ET-8550 prend officiellement en charge. citeturn936403view2turn936403view4

Pour l’alimentation papier, l’ET-8550 accepte ces papiers photo dans les cassettes et dans le chargeur arrière, mais pour les formats **A3 et A3+**, Epson précise une limite de **5 feuilles à la fois** pour plusieurs papiers photo Epson de cette famille. Pour un baryté tiers ou un papier plus rigide, je privilégierais le **rear paper feeder** pour rester du côté le plus sûr mécaniquement. citeturn936403view3

Donc, en très simple :  
**Glossy Epson** = profil ICC glossy + **Media Type: Premium Photo Paper Glossy** + **Off (No Color Adjustment)**. citeturn936403view1turn936403view2  
**Matte Epson** = profil ICC matte + **Media Type: Presentation Paper Matte** ou **Premium Presentation Paper Matte** + **Off (No Color Adjustment)**. citeturn936403view1turn936403view2  
**Baryté tiers** = profil ICC du fabricant + media type recommandé par ce fabricant, sinon test initial en **Ultra Premium Photo Paper Luster**. citeturn936403view2turn936403view4

11:29

Envoie-moi le **nom exact du papier baryté** que tu envisages, et je te donnerai le preset précis de départ pour celui-là.

---
