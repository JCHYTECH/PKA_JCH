# Prémortem — Service de correction photo « Naturaliste »

> Stance **Prémortem** · conseil du 2026-11-16 · hypothèse de travail : **nous sommes le 2027-05-16, le service a été lancé et il est mort.**
> Objet : post-mortem à froid de `strategy/service-correction-photo-conception.md` (V0, archi A batch / B temps réel).

---

## POST-MORTEM — Service de correction photo ARTEON (2026-11-16 → 2027-05-16)

**Statut : arrêté le 2027-01-20, après ~9 semaines de vie et 34 photos traitées.** 0 vente du pack attribuable au service, 0 € de revenu direct, ~3 semaines-homme d'ingénierie consommées.

**Cause n°1 — Personne n'a jamais envoyé de photo (échec de distribution, pas de technique).** Le service est un lead magnet sans entonnoir amont : au 16/11, Ghost était en pause/404 et aucune publication Instagram n'était autorisée. Construire l'étape 2 d'un funnel dont l'étape 1 n'existe pas : on a livré une porte d'entrée sur un couloir vide. 34 photos = 20 de test (M4) + 14 de proches sollicités à la main.

**Cause n°2 — La chaîne MCP Lightroom n'est pas un service, c'est un rituel humain déguisé.** Chaque maillon exige un humain ou une GUI : le plugin doit être démarré par un clic dans *File → Plug-in Manager → Start Server* à chaque relance de Lightroom ; `set_develop_settings` exige une **photo sélectionnée dans l'UI** ; les écritures doivent être sérialisées (« le catalogue n'aime pas les écritures concurrentes ») avec retry ~250 ms sur catalogue occupé. Résultat : le « batch » a tourné en pilotage manuel — exactement ce que le projet devait supprimer. Un crash Lightroom ou une mise à jour macOS = file bloquée sans alerte.

**Cause n°3 — Le catalogue personnel de JC est devenu le goulot et le risque.** Ingérer des photos de clients dans le catalogue de production de JC, c'est mélanger 20 ans de travail personnel avec des JPEG inconnus. On a bricolé une collection « _INBOX_SERVICE », puis on a arrêté d'importer par peur de le corrompre. Aucune isolation (catalogue jetable par lot) n'avait été prévue en V0 : c'est le manque le plus coûteux, découvert en production.

**Cause n°4 — La correction ne tenait pas la promesse « regard de zoologiste ».** Un preset applique expo/WB/courbe/grading. Il ne recadre pas, ne retire pas une branche devant l'œil, ne redresse pas un horizon, ne gère pas le bruit d'un JPEG de smartphone. Sur les RAW de JC, l'avant/après était superbe ; sur les photos réelles reçues (JPEG, téléphone, sujet mou), il était plat et parfois pire que l'original. La question ouverte n°2 de la V0 (« la correction auto suffit-elle comme preuve expert ? ») a reçu sa réponse : **non**. Le différentiel perçu ne justifiait pas 29 €.

**Cause n°5 — Aucun payeur n'a été identifié, et le précédent L'Instant Lu n'a pas servi de leçon.** Gratuit → conversion vers le pack non mesurable (pas de trafic) ; payant → 5–9 € pour un service à 15–25 min de temps JC, ou à $0,174 d'API avec une qualité contestée. Le conseil du 15/11 avait déjà dit **NO-GO** sur la critique photo à l'acte pour exactement ces raisons (prix < coût réel, promesse non tenable, badge gelé). On a reconstruit le même objet avec un rendu d'image en plus.

**Coût d'opportunité — le vrai dommage.** Les 3 semaines sont allées à `/recommend` + orchestrateur + ingestion/restitution, prélevées sur le seul actif qui avait du cash à 30 jours : landing + Gumroad + 10 presets (plan-reorientation, Phase 1). À +6 mois : 0 vente de pack, alors que le chemin « vendre ce qui est déjà produit » n'était ni risqué ni incertain. Les 8 étapes roadmap non closes sont toujours non closes.

**Signal d'alerte rétrospectif.** La V0 le disait : « la chaîne est réalisable dès aujourd'hui en pilotage manuel ». C'était le test à faire **avant** d'écrire une ligne d'orchestrateur : 20 photos traitées à la main en 5 h, avant/après montrés à 10 photographes. Ce test coûtait une journée, il aurait tué le projet ou l'aurait sauvé.

**Ce qui aurait dû être retenu :** GO sur le **test manuel** uniquement (M4 en premier, pas en dernier) ; NO-GO sur l'automatisation tant que 3 demandes spontanées/semaine ne sont pas observées ; et jamais de service tant que Ghost/Instagram ne produisent pas de trafic mesurable.

---

*Prémortem — les causes sont des hypothèses, pas des prédictions ; elles valent par les tests qu'elles rendent obligatoires.*
