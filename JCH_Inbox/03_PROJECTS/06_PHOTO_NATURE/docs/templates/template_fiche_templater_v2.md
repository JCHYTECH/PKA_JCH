---
tags:
  - type/project
  - status/active
---
<%*
const scientific = await tp.system.prompt("Nom scientifique (ex: Acrida ungarica)");
const subspecies = await tp.system.prompt("Sous-espèce (optionnel)");
const family = await tp.system.prompt("Famille");
const order = await tp.system.prompt("Ordre");
const className = await tp.system.prompt("Classe");
const genus = await tp.system.prompt("Genre");
const species = await tp.system.prompt("Espèce (ex: Acrida ungarica)");
const common = await tp.system.prompt("Noms communs");
const location = await tp.system.prompt("Lieu d'observation");
const imageName = await tp.system.prompt("Nom du fichier image déjà importé dans Obsidian (ex: acrida.jpg)");

const safeName = (scientific + (subspecies ? "_" + subspecies : "")).replace(/\s+/g, "_");
await tp.file.rename(safeName);

const titleLine = subspecies ? `${scientific} *${subspecies}*` : scientific;
const subspeciesLine = subspecies ? `- Sous-espèce : ${subspecies}` : "";

tR += `---
type: espece
scientific_name: ${scientific}
subspecies: ${subspecies}
family: ${family}
order: ${order}
class: ${className}
genus: ${genus}
species: ${species}
common_names: ${common}
location: [[${location}]]
image: ${imageName}
date: ${tp.date.now("YYYY-MM-DD")}
---

# ${titleLine}

📸 ![[${imageName}]]

## Taxonomie
- [[${className}]]
- [[${order}]]
- [[${family}]]
- [[${genus}]]
- [[${species}]]

## Identification
- **Nom scientifique** : ${scientific}
${subspeciesLine}
- **Noms communs** : ${common}

## Description
...

## Habitat
...

## Répartition
...

## Classification
- Classe : ${className}
- Ordre : ${order}
- Famille : ${family}
- Genre : ${genus}
- Espèce : ${species}
${subspeciesLine}

## Note naturaliste
...

## Observation
- **Lieu** : [[${location}]]
- **Date** : ${tp.date.now("YYYY-MM-DD")}
- **Conditions** :
- **Comportement observé** :

## Tags
#faune #observation #macro #teleobjectif
`;
%>
