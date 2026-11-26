# Conseil « protection des comptes & secrets PKA » — stance **Expansionniste**

> Dobby 🦉 · conseil du 2026-11-18 · Question motrice : **« Quel upside est-on en train de rater ? »**
> Lecture : `TEAM_Inbox/2026-11-18_dobby_analyse-transcript-protection-comptes.md` (§3.2–3.4, actions A1–A10), `MEMORY.md` (Ollama daemon headless sur M1, tunnel SSH M5:11435, Lupo RPi 5 / HA OS, Mosquitto, Tailscale), `JCH_PRIVATE/credentials-central.md`, `~/.config/pka-jch/api_keys` (0600).

---

## Verdict de stance

**La politique protège des comptes d'homme. Le PKA est une flotte.** Quatre machines, un daemon Ollama sur un M1 sans écran, une passerelle 4G dans le van, quatre scripts qui s'authentifient seuls chaque nuit. Le coffre n'est donc pas une armoire à mots de passe : c'est le **registre d'identité de la flotte**. C'est le bénéfice que le cadrage ne voit pas — et ce qui permet à JC, 70 ans, non-technique, de **continuer à déléguer** au lieu de se recroqueviller.

## U1 · Le coffre comme broker : la rotation devient un non-sujet

Les clés API sont copiées dans `mcp_ollama_server`, `graphify_llm_bridge`, `photo_keyworder` : chaque copie rend la rotation tributaire du code, donc le niveau C (« rotation automatisée ») paraît héroïque. Si le coffre est **interrogé par les scripts** (une commande, une clé, un bail), la rotation redevient une affaire de cinq minutes : on change la valeur, la flotte suit. **Le niveau C cesse d'être un chantier et devient une propriété.**

## U2 · Troisième catégorie : les identités machine

La règle « 2 clés physiques » ne s'applique pas au M1 headless ni au RPi du van : personne ne branche une YubiKey à 3 h du matin dans une camionnette. La politique risque de les laisser **hors périmètre** — or ils détiennent les secrets les plus actifs. L'option non envisagée : une classe **identité machine** avec sa propre règle (pas de clé physique, mais un secret dérivé par machine — `age`/sops, destinataire distinct —, portée limitée, révocable seule). Coût : une après-midi. Couverture : de ~8 comptes à ~8 comptes **+ 4 machines**, sans matériel.

## U3 · Moindre privilège = plafond de dépense

Dix clés API au même niveau : risque de facture autant que de fuite. Des clés **scopées par agent, avec quota**, font du coffre un garde-fou budgétaire : une boucle d'agent qui s'emballe s'arrête sur un plafond, pas sur une facture de 400 €. C'est l'argument qui parle réellement à JC — il craint la dépense, pas l'APT.

## U4 · Lupo comme démonstrateur, et le coffre comme actif multi-projets

Migrer `secrets.yaml` de HA vers le même coffre fait du RPi un **banc d'essai vivant** de la politique : on teste la reprise après perte sans risquer un compte souverain. Déjà instancié, le coffre se rejoue à coût marginal nul pour ARTEON, WILD, la vente occasion : un mécanisme, plusieurs locataires — un **standard PKA** plutôt qu'une corvée annuelle.

## U5 · L'enveloppe scellée : la continuité que personne ne nomme

« Codes de secours hors-ligne » protège de la perte d'une clé. Rien ne protège de **l'absence de JC**. Le même coffre peut porter une enveloppe scellée « si je ne suis pas là » — inventaire, procédure d'accès, personne de confiance. C'est l'option à coût quasi nul qui vaut plus que les deux YubiKey.

## Ce qui tuerait l'upside

- **Appliquer « 2 clés physiques » uniformément** jusqu'au RPi : on exclut la flotte et on garde les secrets actifs en clair.
- **Un coffre consulté à la main.** S'il n'est pas interrogé par les scripts, la rotation reste manuelle et le niveau C reste décoratif.
- **Coffrer sans inventaire des identités machine** : les comptes humains deviennent exemplaires, les daemons gardent des clés éternelles.

**Recommandation de stance : B, plus les clauses U1–U3 dès la V1** — elles coûtent moins que la troisième clé et changent la nature du dispositif.
