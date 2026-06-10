# Models Reference — PKA_JCH

> Derniere mise a jour : 2026-06-06
> Reference complete des modeles LLM disponibles, classes par type, avec forces et cas d'usage.

---

## LOCAL — M1 Ollama (Mac mini M1, 32 GB RAM)

| Modele | Taille | Force | Usage recommande | Projets |
|---|---|---|---|---|
| `deepseek-r1:14b` | 9.0 GB | Raisonnement profond | Logique complexe, diagnostics, debug | Vetalyx, WildNexus |
| `qwen2.5-coder:14b` | 9.0 GB | Code | Dev firmware, scripts, PWA | WildNexus, Faune Autour |
| `qwen3.5:latest` | 6.6 GB | Generaliste FR/EN | Taches courantes, backup general | Tous |
| `qwen3:30b-a3b` | 18 GB | Gros generaliste | Puissance locale — mais lourd pour 32 GB | Tous |
| `llama3.2:3b` | 2.0 GB | Ultra-rapide | Reponses instantanees, classification | Tous |
| `dobby-prompt:latest` | 9.0 GB | Fine-tune [[Dobby]] | Routine PKA : status, [[inbox]], orga | PKA ops |
| `llama3.2-vision:11b` | 7.8 GB | Vision | Analyse cameras-pieges, photos, composition | WildNexus, ARTEON |
| `mistral-nemo:latest` | 7.1 GB | **Francais natif** | Contrats Vetalyx, redaction FR, reglementaire | Vetalyx, ARTEON |
| `phi4:latest` | 9.1 GB | Scientifique/medical | Diagnostics, bio, analyses IVDR | Vetalyx |
| `mxbai-embed-large` | 669 MB | Embeddings | RAG local, recherche semantique docs projets | Tous |

### M5 Ollama (Mac M5)

| Modele | Taille | Force | Usage | Projets |
|---|---|---|---|---|
| `qwen3.6:latest` | 23 GB | Generaliste local | Usage M5 sans reseau | Tous |
| `gemma4:latest` | 9.6 GB | Google leger | Alternative locale rapide | Tous |

---

## CLOUD — APIs distantes

| Modele | Provider | Force | Usage recommande | Projets |
|---|---|---|---|---|
| **DeepSeek V4 Flash** | DeepSeek API | Rapide, bon, 1M ctx | **Quotidien principal** — tout usage general | Tous |
| **DeepSeek V4 Pro** | DeepSeek API | Raisonnement + profond | Problemes complexes, plans architecture | WildNexus, Vetalyx |
| **Claude Sonnet 4.6** | Anthropic API | Excellence redaction | Contenu editorial, articles photo | ARTEON |
| **Gemini** | Google API | Contexte 1M+, multimodal | Tres longs documents, analyse image | Vetalyx, ARTEON |
| **Qwen 3.7 Plus** | OpenRouter | Generaliste solide | Backup si DeepSeek sature | Tous |
| **Qwen 3.7 Max** | OpenRouter | Haut de gamme | Tache critique, si Claude indispo | Tous |

---

## TABLEAU REVERSE — « Si tu veux faire X, utilise Y en priorite »

| Si tu veux... | Utilise en priorite | Pourquoi |
|---|---|---|
| **Rediger un article ARTEON** | Claude Sonnet | Ecriture editoriale — le meilleur |
| **Analyser une photo / camera-piege** | Gemini (cloud) ou llama3.2-vision (local) | Vision — pas de cloud necessaire |
| **Coder du firmware LoRa / ESP32** | qwen2.5-coder:14b (M1) ou DeepSeek Flash | Code specialise rapide |
| **Coder une PWA / Faune Autour** | DeepSeek Flash | Rapide, bon en JS/TS |
| **Analyser un contrat Vetalyx** | Mistral Nemo (M1) + Claude | Francais juridique natif |
| **Lire un dossier reglementaire 200 pages** | Gemini (1M ctx) | Le seul a tout tenir en une fois |
| **Diagnostic allergie / bio** | Phi4 (M1) ou DeepSeek Pro | Raisonnement scientifique |
| **Tache rapide : meteo, note, [[email]]** | DeepSeek Flash ou llama3.2:3b | Instantane, cout zero |
| **Status PKA / [[inbox]] / orga** | [[Dobby]] + Qwen 3.7 Plus (OpenRouter) | Fine-tune [[Dobby]], bootstrap complet |
| **RAG / recherche dans les docs projets** | mxbai-embed-large (M1) | Embeddings, base de tout RAG |
| **Traduction EN-ZH** | Qwen 3.7 Plus (OpenRouter) ou Claude + [[Jade]] | Tres bon chinois |
| **Raisonnement logique / debug** | DeepSeek R1 (M1) | Raisonnement pur, pas cher |
| **Design / maquette / brainstorming** | Gemini | Multimodal, creatif |
| **Planifier un sprint / projet** | DeepSeek Flash | Structure, pas trop lent |
| **Electronique DIY (ESP32, Arduino, capteurs)** | DeepSeek Flash + qwen2.5-coder:14b (M1) | Code embarqué, schemas, debug |
| **Domotique / Home Assistant** | DeepSeek Flash | YAML, blueprints, automations |

---

## Regle de fonctionnement

A chaque tache, le modele utilise (DeepSeek V4 Flash par defaut) est confronte au tableau ci-dessus. Si un autre modele est significativement plus adapte (+10% de gain reel attendu), une suggestion motivee est faite a JCH qui decide. Le gain marginal (<5%) pour un surcout net ne justifie pas un switch.
