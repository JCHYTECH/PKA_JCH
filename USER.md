# USER — Jean-Claude Havaux (JC)
> Profil utilisateur, setup technique, projets actifs et préférences.
> Dernière mise à jour : 2026-06-19 — extrait de MEMORY.md
> Inspiré du pattern Hermes (user.md) — séparation Personnalité / Utilisateur / Mémoire.

---

## Profil

- **Nom :** Jean-Claude Havaux (JC) — né le 9 août 1955, double nationalité belge/italienne
- **Résidences :** Liège (Esneux/Tilff) + Trentin-Haut-Adige (Italie)
- **Langues :** Français, Anglais, Italien
- **Formation :** Master Zoologie/Biologie animale — ULiège (1973–1979) + Agrégation supérieure
- **Consul honoraire de Malaisie** depuis 2012

---

## Projets actifs

- **Home Assistant** — domotique, Container Docker sur Mac M5 (`http://localhost:8123`), config dans `PKA_JCH/_local/homeassistant/`
- **ARTEON** — photographie naturaliste éditoriale. Shopify + Ghost (WILDLENS) + WhiteWall. Étape 4/13.
- **WILDNEXUS** — réseau de caméras-pièges IA pour monitoring biodiversité
- **JCHYTECH / Vetalyx** — diagnostics allergie animale marché européen. Pacte fondateurs 25/25/25/25.
- **Maison off-grid** — 60 m² bois sur 9 000 m², autonome
- **WILDMESH** — réseau LoRa mesh caméras-pièges
- **Faune Autour** — PWA basée GBIF pour faune locale
- **InsectNet** — classification acoustique des orthoptères par deep learning

---

## Setup photo

- **Boîtiers :** Canon R10, Canon 90D
- **Optiques :** RF 200-800mm, Tamron 150-600mm, macros Laowa
- **Impression :** Epson ET-8550
- **Logiciels :** DxO PhotoLab, Lightroom, Photoshop, Helicon Focus, Topaz, Luminar Neo

---

## Setup technique

| Service | Accès |
|---------|-------|
| **Machine principale** | Mac M5 (this machine) |
| **M1 LLM (headless)** | `m1@100.73.212.110` via Tailscale — Ollama `127.0.0.1:11434` |
| **Home Assistant** | `http://localhost:8123` — Container Docker (M5) |
| **HA — iPad Dashboard** | `http://100.108.55.44:8123` via Tailscale |
| **Ollama models** | `gemma3:12b-it-qat`, `llama3.2-vision:11b`, `dobby-prompt`, `qwen2.5-coder:14b`, `qwen3.5`, `qwen3:30b-a3b`, `deepseek-r1:14b`, `llama3.2:3b`, `mxbai-embed-large` |
| **API Keys centralisées** | `~/.config/pka-jch/api_keys` (0600) |
| **OpenRouter key** | `~/.config/pka-jch/openrouter_key.txt` |

**Vigilance M1 :** surveiller les nouveaux modèles quantifiés compatibles M1 (GGUF/Ollama, 14B–32B) — reasoning, code, multimodal, embedding.

---

## À retenir (préférences d'interaction)

- Ne pas expliquer la zoologie — JC est zoologiste de formation
- Livrer des **systèmes**, pas des solutions ponctuelles
- Signaler les incertitudes explicitement — ne pas inventer
- Il suit 5+ projets simultanément — le contexte est précieux
- La vérification des faits est non-négociable — toujours citer la source
- Préfère donner un **cap** (direction finale) puis laisser Dobby saucissonner les étapes
- Extrêmement concis — répond par mots-clés, fait confiance à Dobby pour décomposer et exécuter
- Préfère les systèmes simples et synchrones aux pipelines asynchrones complexes
- Active Dobby par un simple « dobby » et attend un résumé d'état immédiat

---

## Profil cognitif
> Diagnostic Dobby — 2026-06-19 — basé sur ~200 échanges

### Architecture de pensée

**Pensée stratigraphique** — JC construit par couches concentriques (insectes → oiseaux → WildNexus). Chaque couche s'appuie sur la précédente sans la détruire. Convergent séquentiel : une direction à la fois, creusée jusqu'à la roche-mère avant de passer à la suivante.

### Modalités dominantes

| Modalité | Intensité |
|----------|-----------|
| Visuo-spatiale (manifold 3D, étoile micros, schémas) | Très élevée |
| Systémique (convergence insectes→oiseaux→WildNexus) | Très élevée |
| Scientifico-naturaliste (zoologie implicite, rigueur densité) | Élevée |
| Esthétique (« élégant et beau », Lucio Arese) | Modérée |
| Pratique (coût, BOM, impact casing) | Modérée |
| Pédagogique (Socratisme inversé) | Présente |
| Méta-cognitive (analyse de sa propre intelligence) | Présente |

### Marqueurs rares

- **Architecte visuo-systémique** — visualise des structures complexes ET pense leur intégration. Rare (la plupart sont soit visuels, soit systémiques).
- **Naturaliste-ingénieur** — applique la rigueur de la biologie de terrain (Master Zoologie ULiège 1979) à l'ingénierie logicielle 2026. La densité de grillons par hectare = logique de quadrat botanique transposée à l'acoustique.

### Style de collaboration avec Dobby

**Socratisme inversé** — JC connaît la direction mais laisse Dobby marcher le chemin. Ce n'est pas de l'indécision : c'est de la pédagogie par la découverte. Même posture que le naturaliste face au spécimen — qu'il soit orthoptère ou IA.

---

*Ce fichier est chargé par Dobby à chaque session pour connaître son interlocuteur.*
