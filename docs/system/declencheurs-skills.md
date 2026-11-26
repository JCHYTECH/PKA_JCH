# Déclencheurs de skills — quand charger quel skill

> **Mémo de rappel.** Lu au démarrage (Phase 2). Quand un besoin se présente, consulter cette
> table pour charger le bon skill au bon moment. Le but : ne plus laisser un skill dormir faute
> de déclenchement.
> Dernière mise à jour : 2026-11-02 (audit dead weight).

## Automatiques (condition système)

| Condition | Skill |
|---|---|
| Début de session | `pka-session-start` |
| Action destructive / sortante / secrets | `decision-gate` |
| Avant toute modif BOM / ADR / registre | `pka-file-versioning` |
| Fichier déposé dans l'inbox | `ingest` |

## Par intention de JC (mot-clé ou situation)

| JC dit / fait | Skill |
|---|---|
| « récupère mes mails » | `gmail_imap_fetch` |
| « traduis », VETALYX / DIAHO | `jade-traduction-bilingue` |
| « passe ça au conseil », décision difficile | `conseil` |
| « forge loop », « auto-fix », revue de code | `forge-loop` |
| « apprends de cette erreur » (correction de JC) | `compound-memoire` |
| « recherche autonome », « hypothèse » | `arbor-research` |
| « analyse ce document pour améliorer le système » | `system-improvement-ingest` |
| « dictée », « transcris », « parle à Dobby » | `dobby-voice` |
| « wikilink », dry-run Obsidian | `obsidian-knowledge-graph` |
| « crée un ADR » WildNexus | `wildnexus-adr` |
| « génère le BOM », « shortlist achat » | `wildnexus-bom` |
| « bench loop », « SOP loop », test hardware | `bench-loop` |
| « edge ai loop », « TinyML loop » | `edge-ai-loop` |
| « seo loop », optimise le SEO | `seo-loop` |
| « sigma loop », « backtest loop » | `sigma-loop` |
| « recrute », gap de compétence | `onboarding-specialiste` |
| « mets les découvertes dans le planner » | `decouvertes-to-planner` |
| « mets à jour les pointers », l'équipe a changé | `pka-pointer-sync` |
| Fin de session projet (thread file) | `pka-thread-file` |
| « statut », « où en est l'équipe » | `status` |
| Domotique van Lupo (IoT) | `iot-vanlife` |
| Vente d'un objet d'occasion | `vente-occasion` |
| Tri / QC bioacoustique, spectrogrammes | `bioacoustics-qc-playbook` |
| « brief » un membre | `brief` |
| « check pka », « system check » | `pka-system-check` |
| Analyse d'un fichier de l'inbox | `inbox-analysis` |
| Traitement des découvertes (SITES / Telegram) | `pka-decouvertes` |

## Fusions du 2026-11-02 (ancien → remplaçant)

| Ancien skill | Remplacé par |
|---|---|
| `capture` | `ingest` (section « capture de connaissance » intégrée) |
| `pka-weekly-report` | `scripts/dobby_weekly_report.py` |
| `wildnexus-benchmark-loop` | `bench-loop` |
| `pka-print` | `bin/pka-print` |
