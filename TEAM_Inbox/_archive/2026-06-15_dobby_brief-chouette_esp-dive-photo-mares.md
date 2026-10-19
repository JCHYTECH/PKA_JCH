# Brief — Concordance ESP-DIVE × WildNexus : Faisabilité Photo en Mares

**De :** [[Dobby]] 🦉
**Pour :** [[Chouette]] 🦉 (#25)
**Date :** 2026-06-15
**Priorité :** MEDIUM
**Contexte :** JCH envisage d'utiliser un sous-marin ESP32 pour photographier la faune dans les mares. Analyse de faisabilité terrain.

---

## Contexte

ESP-DIVE est un sous-marin RC contrôlé par WiFi avec caméra FPV frontale OV2640 (800×600, 20 FPS), éclairage LED 12× blanc, ballasts à piston pour la profondeur. JCH veut évaluer si ce type de dispositif peut être adapté pour :
- Photographier insectes aquatiques, amphibiens, larves dans les mares
- Observer sans perturber (approche discrète)
- Compléter le dispositif WildNexus (piège photo terrestre) avec une dimension aquatique

## Caractéristiques terrain ESP-DIVE

| Paramètre | Valeur |
|-----------|--------|
| Autonomie | ~20-30 min (1000mAh, propulsion continue) |
| Portée WiFi | 5m (via câble coaxial vers antenne surface) |
| Profondeur max | Non spécifiée (pression tube acrylique) |
| Résolution photo | 800×600 SVGA (2MP effectif OV2640) |
| Éclairage | 12 LEDs blanches frontales |
| Contrôle | Smartphone en surface (WiFi AP) |
| Flottabilité | Ajustable via 2 pistons à seringue |
| Poids | Non spécifié (~500-800g estimé) |
| Dimensions | Tube acrylique 44×48×305mm |

## Questions pour [[Chouette]]

1. **Qualité photo suffisante ?** — 800×600 (0.5 MP) est très en dessous des standards photo naturaliste (JCH utilise Canon R10, 90D). Est-ce que cette résolution permet une identification d'espèce en mare ? Pour quel usage : détection, documentation, ou photo exploitable ?

2. **Perturbation de la faune** — Un sous-marin de 30cm avec 12 LEDs et moteurs est-il plus discret qu'une approche à guetter en bord de mare ? Les vibrations moteur et les LEDs risquent-elles de faire fuir la faune avant la photo ?

3. **Scénarios d'usage réalistes** — Quels types de mares (taille, clarté, profondeur) sont compatibles ? L'autonomie de 20-30 min permet-elle une session crédible ? Faut-il viser la photo subaquatique ou simplement une caméra immergée fixe (style piège photo aquatique) ?

4. **Contraintes saisonnières** — En Belgique/Italie, les mares sont souvent troubles (algues, vase). La visibilité subaquatique est-elle suffisante pour de la photo dans nos biotopes ? Quelles périodes sont favorables ?

5. **Alternative plus simple** — Plutôt qu'un sous-marin motorisé complexe, une caméra ESP32 étanche fixe posée au fond de la mare avec déclenchement PIR/détection de mouvement serait-elle plus pertinente ? C'est essentiellement un WildNexus aquatique.

6. **Sécurité** — Risques de perte du dispositif (accrochage, panne, zone hors WiFi) ? Solutions de récupération ?

## Livrable attendu

Avis terrain structuré : (a) faisabilité photo en mare avec ESP-DIVE, (b) alternative recommandée si non viable, (c) contraintes saisonnières et logistiques pour la Belgique et le Trentin. Format dans `TEAM_Inbox/`.

## Références

- PDF source : `JCH_Inbox/00_INBOX/ESP-DIVE_ Build an ESP32 RC Submarine...pdf`
- WildNexus P0 : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md`
- Setup photo JCH : Canon R10, 90D, RF 200-800mm (cf. MEMORY.md)
