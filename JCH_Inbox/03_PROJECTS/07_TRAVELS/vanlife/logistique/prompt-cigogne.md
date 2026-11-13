# Prompt [[Cigogne]] 🦩 — Template de brief

> À utiliser à chaque nouvelle destination. Copier-coller, remplir les champs, envoyer.
> [[Dobby]] ou JCH peuvent initier.

---

## Brief voyage

**[[Cigogne]]**, prépare une fiche destination pour :

- **Destination :** [Nom de la région / ville principale]
- **Saison :** [printemps / été / automne / hiver]
- **Durée :** [X] jours sur place + [Y] étapes mi-chemin
- **Contraintes :** [ex: éviter juillet-août, max 4h de route par jour, Anne veut nager...]

---

## Ta mission

1. **Scoute les spots nuit** — lance `camping_scout.py` niveau 2 sur chaque point de nuit (cf. [procédure](./[[procedure-camping-scout-cigogne]].md))
2. **Remplis le template** — fiche complète au format `TEMPLATE.md` avec toutes les sections
3. **Sélectionne les spots** — max 2 par nuit (un principal ★ + une alternative), filtrés par :
   - Distance < 3 km du centre
   - Score JCH ≥ 7 si possible
   - Services (vidange, eau) pour 1 nuit sur 2 minimum
   - Toujours une option gratuite en backup
4. **Vérifie la méthodo** — applique la checklist stationnement (cf. [methodologie-stationnement](./[[methodologie-stationnement]].md)) pour chaque réserve naturelle
5. **Propose des étapes mi-chemin** si le trajet Liège → destination dépasse 400 km (3 options aller, 3 retour)
6. **Dépose la fiche** dans `destinations/Nom_Destination.md`

---

## Contraintes permanentes

- 📷 JCH : photo wildlife à l'aube/crépuscule, réserves naturelles prioritaires
- 🏛️ Anne : monuments, sculpture, villages de caractère, baignade
- 🚐 Van : Stylevan Equinox IV Ford
- 🥐/🥪/🍽️ : petit-déj et déj dans le van, dîner resto (emplacement, vue, locaux)
- 🌧️ Plans B : chaque étape extérieure doit avoir une alternative couverte
- 🗺️ Google Maps : lien 🔗 dans chaque tableau
- ⏰ Départ : 10h00 · Départ étape : 9h00

---

## Format de sortie attendu

Fiche Markdown complète avec sections :
- Attraits (JCH / Anne / communs)
- Étapes mi-chemin (si >400 km)
- Logistique van — spots nuit (table avec GPS, km, prix, services, score)
- Distances entre étapes
- Spots photo (avec GPS)
- Patrimoine & culture (Anne)
- Repas & restaurants (1 par soir + alternative)
- Baignade
- Météo & plans B
- Planning jour par jour
- Retour d'expérience (à remplir après séjour)

---

## Exemple rempli

```markdown
**Cigogne**, prépare une fiche destination pour :

- **Destination :** Normandie — Baie du Mont-Saint-Michel & Côte Fleurie
- **Saison :** printemps ou automne
- **Durée :** 3 jours sur place + 2 étapes mi-chemin
- **Contraintes :** éviter juillet-août (affluence), Anne veut nager en mer
```
