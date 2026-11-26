---
date: 2026-11-17
source: dobby
domain: arteon/wildlens
type: plan
sujet: WildLens — premier produit fini
status: actif
lang: fr
---

# WildLens — Plan « produit fini »

> Dobby 🦉 — 2026-11-17. Décision JC : **WildLens = premier produit fini** d'ARTEON.
> Déplie le chantier 1 (Audience — WildLens) de `strategy/arteon-executive-summary.md`.
> Supersede `plan-action-wildlens.md` (15/11) ; synthétise `operations-creation-site-ghost.md` + `runbook-ghost-selfhost-hostinger.md`.

---

## 1. Définition de « produit fini » (Definition of Done)

**V1 — le journal tourne et envoie tout seul :**

- [ ] Site public `https://wildlens.arteon.be` (SSL, HTTP 200, zéro 404).
- [ ] Thème custom ARTEON (vert terrain `#3D5A3E`, Space Grotesk + Lora + IBM Plex Mono).
- [ ] 4 éditions publiées (#1 03-28, #2 07-02, #3 10-24, #4 10-31), conformes architecture v2 (The Frame / The Shift / The Field), EN.
- [ ] Newsletter fonctionnelle : abonnement + email de bienvenue + envoi hebdo (Mailgun).
- [ ] Cadence hebdo (samedi) automatisée — launchd `com.dobby.wildlens-weekly`.
- [ ] Backups (cron quotidien) + monitoring + snapshots hPanel.

**Hors V1 (après) :** multilingue FR/IT (V1.1) · acquisition Instagram + funnel monétisation (V1.2).

---

## 2. État réel (17/11)

**Fait :** VPS acheté (IP `2.25.8.208`, 86,97 €/an) · SSH durci · Ghost installé partiel (MySQL `ghost_prod` + user `ghost` créés).

**Reste :** DNS → SSL → Mailgun → migration → thème → publication → newsletter → backups.

---

## 3. Le chemin critique (ordre strict)

Le goulot est **unique** : le DNS. Tout le reste est bloqué derrière.

### A. Infra — DNS → SSL → Mailgun (séquentiel · goulot JC)

1. **DNS A** `wildlens` → `2.25.8.208` (registrar arteon.be) — **JC · LE PAS**. Vérif : `dig +short wildlens.arteon.be`.
2. **SSL** : `ghost setup ssl` (Forge, SSH `deploy`) — bloqué tant que le DNS ne résout pas.
3. **Mailgun** : compte + enregistrements TXT SPF/DKIM/MX/CNAME (JC) → config SMTP `ghost config set mail` (Forge) → test d'envoi.

**Gate A :** `curl -I https://wildlens.arteon.be` → 200, et une newsletter de test reçue.

### B. Contenu — migration → thème → publication (Forge/Dobby + feu vert JC)

4. Export Ghost(Pro) JSON (JC) → import VPS (Forge). **⚠️ 4 éditions réelles à migrer, pas 6** — `04-18` = transcript brut, `06-20` = template vide → archivées, à ne pas publier.
5. Thème custom ARTEON (upload Settings → Design → Change theme).
6. Publier #4 (feu vert JC) → puis #1, #2, #3. Vérif rendu mobile + URL canoniques.

**Gate B :** 4 éditions en ligne, rendu OK.

### C. Newsletter — membres → cadence (Forge + Dobby)

7. Ghost Members : abonnement + email de bienvenue + template (en-tête WildLens, footer ARTEON).
8. Cadence hebdo samedi (launchd déjà réactivé) + première édition publiée en rythme.

**Gate C :** un abonné test reçoit l'édition du samedi.

### D. Robustesse — backups + monitoring (Forge)

9. `ghost backup` + cron quotidien 3h ; snapshots hPanel hebdo ; copie hors VPS (M5/iCloud).
10. Monitoring (uptime, disque).

**Gate D :** un backup restauré en test.

### E. V1.1 — Multilingue (après V1 · Jade + Forge)

11. Traduction FR + IT des éditions (Jade) ; changeur de langue EN·FR·IT ; détection géoloc IP.

### F. V1.2 — Acquisition (après V1 · sur demande JC)

12. Instagram (couche découverte, publication **uniquement sur demande explicite**) ; funnel → presets + L'Instant Lu.

---

## 4. Rôles

- **JC** — DNS, compte Mailgun, export Ghost(Pro), feu vert publication, éditorial (The Frame).
- **Forge** — SSH VPS (SSL, mail, migration, thème, backups, monitoring, changeur langue).
- **Jade** — traductions FR/IT (V1.1).
- **Dobby** — coordination, conversion éditions, cadence hebdo, doc credentials.

---

## 5. Le « pas » (prochaine action concrète)

**JC pointe le record A `wildlens` → `2.25.8.208` chez le registrar d'arteon.be.** Rien d'autre ne peut avancer avant ça.

---

## 6. Gardes-fous WildLens

1. **Pas de site public vide** — rester privé jusqu'à 4 éditions en ligne.
2. **Pas de publication Instagram sans demande explicite JC.**
3. **4 éditions, pas 6** — ne pas republier transcript/template archivés.
4. **Credentials dans `JCH_PRIVATE/`**, jamais dans le repo public.
5. **Une inconnue à la fois** — finir V1 EN avant le multilingue.

---

*Sources : `plan-action-wildlens.md`, `operations-creation-site-ghost.md`, `runbook-ghost-selfhost-hostinger.md`, `wildlens/INDEX.md`, `thread-arteon.md`.*
