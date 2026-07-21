# Principes architecturaux — PKA_JCH

> Issu de `Prompt_Dobby_PKA_JCH_Master_Architecture.md` (JC, ~juin 2026)
> Formalisation : Dobby 🦉 — 2026-07-16
>
> **Toute décision technique ou organisationnelle doit être cohérente avec ces principes.**

---

## 1. Simplicité

La solution la plus simple est la meilleure. Une technologie n'est introduite que si son bénéfice est clairement démontré. Pas de sur-ingénierie.

## 2. Modularité

Chaque composant est indépendant et remplaçable. Un skill, un script, un agent — chacun fait une chose, bien. Les dépendances sont explicites et minimales.

## 3. Maintenabilité

Le code et la documentation doivent pouvoir être compris par un nouvel agent ou un humain sans le contexte complet. Tout document a un propriétaire et une date de dernière mise à jour.

## 4. Automatisation

Tout ce qui est répétitif doit être automatisé. Un script, un skill, ou un launchd. Si une tâche est faite 3 fois manuellement, elle mérite un script.

## 5. Documentation

Tout est documenté avant d'être codé. La documentation est la source de vérité — le code l'implémente. Un fichier sans date ni auteur est un fichier mort.

## 6. Indépendance fournisseur

PKA ne dépend d'aucun modèle, outil ou fournisseur unique. DeepSeek, Claude, Gemini, Qwen, outils locaux — chacun a son rôle, aucun n'est irremplaçable. Les données et la logique appartiennent à PKA, pas à un SaaS.
