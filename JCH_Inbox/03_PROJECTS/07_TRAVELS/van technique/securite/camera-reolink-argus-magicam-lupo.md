Voici la synthèse complète de notre discussion, structurée et prête à être copiée-collée dans un fichier .md (Markdown).  
```
# Configuration Reolink Argus MagiCam pour Westfalia Kelsey
*Guide d'installation : Mode Dashcam (Route) & Mode Détecteur de mouvement (Arrêt)*

## 1. Matériel requis et spécifications

### Fixation extérieure haute résistance
L'aimant d'origine de la caméra n'est pas conçu pour un véhicule en mouvement. Pour rouler en toute sécurité (jusqu'à 130 km/h) sans rayer la carrosserie :
*   **Option 1 :** Support magnétique universel avec vis 1/4" de chez *The Sparky Shop*.
*   
```
```
**Option 2 :** Aimant en pot néodyme caoutchouté (diamètre de 66 mm recommandé pour une force d'attraction > 20 kg) avec tige filetée au pas standard de 1/4"-20.

```
```

### Stockage (Mode Boucle / Dashcam)
La caméra Reolink dispose de la fonction **"Overwrite" (Réécriture)**. Dès que la carte est pleine, elle efface automatiquement les fichiers les plus anciens.
*   **Type de carte obligatoire :** MicroSD de gamme **"High Endurance"** (ex: *SanDisk High Endurance* ou *Samsung PRO Endurance*) pour résister aux cycles d'écriture continus et aux températures extrêmes (-25°C à +85°C).
*   
```
```
**Estimation de l'autonomie (Base : 4h de route/jour en qualité 2K soit ~1,35 Go/heure) :**

```
```
    
```
```
*   **64 Go :** ~11 jours de voyage mémorisés (44h de vidéo)

```
```
    
```
```
*   **128 Go (Recommandé) :** ~22 jours de voyage mémorisés (88h de vidéo)

```
```
    *   **256 Go :** ~44 jours de voyage mémorisés (176h de vidéo)
    *   *Note : Le mode détection à l'arrêt consomme moins de 5% de l'espace global.*

### Alimentation et câblage
*   **Câble :** Câble plat USB-C (épaisseur < 2 mm) d'une longueur de **3 mètres**.
*   
```
```
**Chargeur :** Adaptateur allume-cigare USB-C puissant doté de la technologie *Power Delivery (PD)* délivrant **15W à 20W minimum** (5V/3A ou 9V/2A) pour compenser la consommation du mode dashcam en roulant.

```
```

---

## 2. Raccordement électrique sur Westfalia Kelsey

Le Westfalia Kelsey possède deux réseaux électriques distincts. Pour automatiser la bascule entre les modes Route et Arrêt, respectez impérativement ce branchement :

1.  **Utiliser la prise "Après-Contact" (ACC) :** Branchez le chargeur uniquement sur la prise allume-cigare d'origine du tableau de bord (gérée par la batterie moteur du porteur Ford/Mercedes).
    
```
```
*   *Pourquoi ?* Cette prise s'allume au démarrage et se coupe quelques minutes après l'arrêt du moteur. 

```
```
    
```
```
*   *Piège à éviter :* Ne pas brancher sur les prises arrière de la cellule (gérées par la centrale Westfalia), car elles alimentent en continu et videraient la batterie auxiliaire tout en bloquant la caméra en mode dashcam permanent.

```
```
2.  
```
```
**Cheminement du câble plat vers l'extérieur :**

```
```
    
```
```
*   Partir du tableau de bord, dissimuler le câble sous le tapis de sol ou les plastiques vers le côté passager.

```
```
    
```
```
*   Remonter le long du montant de la portière passager derrière le joint en caoutchouc noir.

```
```
    *   Faire sortir le câble par le **bas de la portière passager** en le pinçant dans le joint. La porte se ferme normalement, le câble est protégé, et cela évite les infiltrations d'eau par capillarité.
    
```
```
*   Laisser une petite boucle de mou (décharge de traction) juste avant le branchement USB-C sur la caméra extérieure.

```
```

---

## 3. Logique de fonctionnement automatique


```
[ DÉMARRAGE DU VAN ]  
│  
▼  
La prise allume-cigare s'active (12V) ──► La Reolink détecte l'alimentation secteur  
└──► FONCTION : Mode Dashcam (Enregistrement continu 24/7)  
└──► EN PARALLÈLE : Recharge de la batterie interne  
[ ARRÊT DU MOTEUR ]  
│  
▼  
La prise allume-cigare se coupe ───────► La Reolink bascule instantanément sur sa batterie interne  
└──► FONCTION : Mode Éco / Détecteur de mouvement (Veille active)  
└──► ACTION : Enregistre et notifie uniquement si un intrus approche  
```
---

## 4. Configuration de l'application Reolink

Avant le premier départ, vérifiez ces deux paramètres dans l'application mobile :
1.  **Paramètres de stockage :** Activez l'option **"Overwrite" (Réécriture)** et configurez-la sur **"Oldest"** pour écraser automatiquement les vidéos les plus anciennes lorsque la carte MicroSD atteint 100% de sa capacité.
2.  **Sécurité physique :** Installez toujours un petit câble de sécurité en acier ou en nylon (Leash) entre le corps de la caméra et un élément fixe (barre de toit, rétroviseur, joint de porte). Si l'aimant venait à être percuté par un débris, la caméra pendrait le long de la carrosserie au lieu de s'écraser sur la route.

```
Bon voyage et bonne route à bord de votre Westfalia Kelsey ! Si vous planifiez d'ajouter d'autres équipements ou si vous avez des questions sur l'**autonomie globale de la batterie du van**, faites-le-moi savoir !  
  
  
  
