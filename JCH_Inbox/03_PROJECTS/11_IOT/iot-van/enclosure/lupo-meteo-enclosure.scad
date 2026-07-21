// =============================================================================
// Lupo Van — Station Météo Intérieure : Boîtier Cheminée
// =============================================================================
// Designer  : Scarabée 🪲, Équipe PKA
// Date      : 2025-07-11
// Licence   : MIT
// Synopsis  : Boîtier paramétrique à deux chambres avec séparation thermique
//             pour ESP32-C3 Super Mini + BME688 + SHT31.
//             Flux d'air passif bas→haut (effet cheminée).
// =============================================================================

/* [Dimensions composants] */
// --- ESP32-C3 Super Mini ---
ESP32_W     = 22.5;  // largeur PCB (mm)
ESP32_D     = 18.0;  // profondeur PCB (mm)
ESP32_H     =  5.5;  // épaisseur avec composants (mm)
ESP32_USBC_W =  8.5; // largeur découpe USB-C (mm)
ESP32_USBC_H =  3.2; // hauteur découpe USB-C (mm)

// --- BME688 breakout ---
BME688_W    = 15.0;
BME688_D    = 12.0;
BME688_H    =  3.0;

// --- SHT31 breakout ---
SHT31_W     = 15.0;
SHT31_D     = 12.0;
SHT31_H     =  3.0;

/* [Tolérances] */
TOLERANCE   = 0.5;   // marge générique sur chaque dimension
WALL        = 2.0;   // épaisseur de paroi (mm)
SEPARATOR   = 2.0;   // épaisseur de la paroi thermique (mm)
FLOOR       = 2.0;   // épaisseur plancher/plafond (mm)

/* [Ventilation] */
VENT_SLOT_W = 2.0;   // largeur d'une fente de ventilation (mm)
VENT_SLOT_L = 12.0;  // longueur d'une fente (mm)
VENT_SPACING = 1.5;  // espacement entre fentes (mm)

/* [Fixation murale] */
M3_CLEARANCE = 3.4;  // diamètre trou de passage M3 (mm)
M3_HEAD_D    = 6.2;  // diamètre tête fraisée M3 (mm)
M3_HEAD_H    = 2.0;  // profondeur fraisure (mm)

/* [Couvercle] */
LID_THICKNESS = 2.0;  // épaisseur du couvercle (mm)
LID_SCREW_D   = 2.2;  // diamètre trou vis M2 couvercle (mm)

/* [Guide lumière LED] */
LED_HOLE_D    = 1.8;  // diamètre trou guide lumière (mm)

// =============================================================================
// Dimensions calculées
// =============================================================================

// Tolérances appliquées
eW = ESP32_W  + 2*TOLERANCE;
eD = ESP32_D  + 2*TOLERANCE;
eH = ESP32_H  + TOLERANCE;

bW = BME688_W + 2*TOLERANCE;
bD = BME688_D + 2*TOLERANCE;
bH = BME688_H + TOLERANCE;

sW = SHT31_W  + 2*TOLERANCE;
sD = SHT31_D  + 2*TOLERANCE;
sH = SHT31_H  + TOLERANCE;

// Chambre basse (capteurs côte à côte le long de X, gap central)
SENSOR_GAP    = 3.0;                        // espace entre les 2 capteurs
CHAMBER_LOW_W = bW + sW + SENSOR_GAP + 4;  // largeur interne chambre basse
CHAMBER_LOW_D = max(bD, sD) + 4;           // profondeur interne
CHAMBER_LOW_H = max(bH, sH) + 6;           // hauteur interne (air + jumpers)

// Chambre haute (ESP32)
CHAMBER_HIGH_W = eW + 6;   // largeur interne
CHAMBER_HIGH_D = eD + 6;   // profondeur interne
CHAMBER_HIGH_H = eH + 7;   // hauteur interne (PCB + USB-C marge)

// Boîtier externe (unifié sur largeur/profondeur max)
BOX_W = max(CHAMBER_LOW_W, CHAMBER_HIGH_W) + 2*WALL;
BOX_D = max(CHAMBER_LOW_D, CHAMBER_HIGH_D) + 2*WALL;
BOX_H = CHAMBER_LOW_H + SEPARATOR + CHAMBER_HIGH_H + 2*FLOOR;

// Origine des chambres en Z (fond du boîtier = Z=0)
LOW_Z_START  = FLOOR;
LOW_Z_END    = LOW_Z_START + CHAMBER_LOW_H;
SEP_Z_START  = LOW_Z_END;
SEP_Z_END    = SEP_Z_START + SEPARATOR;
HIGH_Z_START = SEP_Z_END;
HIGH_Z_END   = HIGH_Z_START + CHAMBER_HIGH_H;

// Positions capteurs (centrés dans la chambre basse)
BME688_X = -bW/2 - SENSOR_GAP/2;
BME688_Y = 0;
SHT31_X  =  sW/2 + SENSOR_GAP/2;
SHT31_Y  = 0;

// Position ESP32 (centré dans la chambre haute)
ESP32_X = 0;
ESP32_Y = 0;

// =============================================================================
// Modules utilitaires
// =============================================================================

// Arrondi 2D pour les angles (fraise à rayon r)
module rounded_square_2d(w, d, r) {
    offset(r = r) square([w - 2*r, d - 2*r], center = true);
}

// =============================================================================
// Module : Ventilation — grille de fentes horizontales
// =============================================================================
module vent_slots(panel_w, panel_d, slot_w, slot_len, spacing, count) {
    // Fentes parallèles à l'axe X (horizontales), empilées en Y
    total_h = count * slot_w + (count - 1) * spacing;
    start_y = -total_h / 2 + slot_w / 2;
    for (i = [0 : count - 1]) {
        translate([0, start_y + i * (slot_w + spacing), 0])
            cube([slot_len, slot_w, panel_d + 0.2], center = true);
    }
}

// =============================================================================
// Module : Trou de fixation M3 fraisé (axe X traversant pour face arrière)
// =============================================================================
module m3_countersunk_hole_x(thickness) {
    // Fraisure côté extérieur
    translate([-thickness/2 - 0.01, 0, 0])
        cylinder(d = M3_HEAD_D, h = M3_HEAD_H + 0.01, $fn = 32);
    // Trou de passage
    translate([-thickness - 0.01, 0, 0])
        cylinder(d = M3_CLEARANCE, h = thickness + 0.02, $fn = 32);
}

// =============================================================================
// Module : Corps principal du boîtier (creux, face avant ouverte)
// =============================================================================
module main_body() {
    difference() {
        // Extérieur plein
        translate([0, 0, BOX_H/2])
            cube([BOX_W, BOX_D, BOX_H], center = true);

        // Cavité intérieure (union des deux chambres + séparateur retiré)
        union() {
            // Chambre basse
            translate([0, 0, LOW_Z_START + CHAMBER_LOW_H/2])
                cube([CHAMBER_LOW_W, CHAMBER_LOW_D + 0.2, CHAMBER_LOW_H], center = true);
            // Chambre haute
            translate([0, 0, HIGH_Z_START + CHAMBER_HIGH_H/2])
                cube([CHAMBER_HIGH_W, CHAMBER_HIGH_D + 0.2, CHAMBER_HIGH_H], center = true);
        }

        // Ouverture façade (tout l'avant, pour le couvercle)
        translate([0, BOX_D/2 - WALL/2, BOX_H/2])
            cube([BOX_W - 2*WALL + 0.2, WALL + 0.2, BOX_H - 2*FLOOR + 0.2], center = true);

        // Découpe USB-C (face droite, chambre haute)
        translate([BOX_W/2, 0, HIGH_Z_START + CHAMBER_HIGH_H/2])
            cube([WALL + 0.2, ESP32_USBC_W, ESP32_USBC_H], center = true);

        // Guide lumière LED (face avant — sera dans le couvercle aussi)
        // Positionnée côté gauche de la chambre haute, en façade
        translate([-BOX_W/4, BOX_D/2 - WALL/2, HIGH_Z_START + CHAMBER_HIGH_H * 0.7])
            rotate([0, 90, 0])
                cylinder(d = LED_HOLE_D, h = WALL + 0.2, center = true, $fn = 24);

        // Ventilation basse (plancher — admission air frais)
        for (jx = [-1, 0, 1]) {
            translate([jx * 10, 0, FLOOR/2])
                cube([VENT_SLOT_L, VENT_SLOT_W, FLOOR + 0.2], center = true);
        }

        // Ventilation haute (plafond — évacuation air chaud)
        for (jx = [-1, 0, 1]) {
            translate([jx * 10, 0, BOX_H - FLOOR/2])
                cube([VENT_SLOT_L, VENT_SLOT_W, FLOOR + 0.2], center = true);
        }

        // Fixations murales M3 (face arrière, 2 points hauts)
        for (mz = [BOX_H * 0.75, BOX_H * 0.25]) {
            translate([0, -BOX_D/2, mz])
                rotate([0, 90, 0])
                    m3_countersunk_hole_x(WALL);
        }

        // Passages fils I2C dans la paroi séparatrice (4 fils)
        // Petit canal excentré pour ne pas gêner les capteurs
        translate([BOX_W/2 - WALL - 3, 0, SEP_Z_START])
            cube([4, 6, SEPARATOR + 0.2], center = true);
    }
}

// =============================================================================
// Module : Support capteurs (berceau dans la chambre basse)
// =============================================================================
module sensor_cradle() {
    // Plots de positionnement pour BME688
    color("LightGreen") {
        translate([BME688_X, BME688_Y, LOW_Z_START + 1])
            cube([bW, bD, 1], center = true);
        // Petits guides anti-glissement
        for (dx = [-bW/2 + 2, bW/2 - 2]) {
            for (dy = [-bD/2 + 2, bD/2 - 2]) {
                translate([BME688_X + dx, BME688_Y + dy, LOW_Z_START + 1.5])
                    cylinder(d = 2, h = 1.5, $fn = 16);
            }
        }
    }

    // Plots de positionnement pour SHT31
    color("LightBlue") {
        translate([SHT31_X, SHT31_Y, LOW_Z_START + 1])
            cube([sW, sD, 1], center = true);
        for (dx = [-sW/2 + 2, sW/2 - 2]) {
            for (dy = [-sD/2 + 2, sD/2 - 2]) {
                translate([SHT31_X + dx, SHT31_Y + dy, LOW_Z_START + 1.5])
                    cylinder(d = 2, h = 1.5, $fn = 16);
            }
        }
    }
}

// =============================================================================
// Module : Support ESP32 (berceau dans la chambre haute)
// =============================================================================
module esp32_cradle() {
    color("SlateBlue") {
        // Plateforme support
        translate([ESP32_X, ESP32_Y, HIGH_Z_START + 1.5])
            cube([eW, eD, 1.5], center = true);
        // Guides anti-glissement
        for (dx = [-eW/2 + 3, eW/2 - 3]) {
            for (dy = [-eD/2 + 3, eD/2 - 3]) {
                translate([ESP32_X + dx, ESP32_Y + dy, HIGH_Z_START + 2.5])
                    cylinder(d = 2.5, h = 2, $fn = 16);
            }
        }
    }
}

// =============================================================================
// Module : Couvercle clipsable avec vis M2 optionnelles
// =============================================================================
module lid() {
    lid_w = BOX_W - 2*WALL;
    lid_h = BOX_H - 2*FLOOR;
    overlap = 1.0; // recouvrement du couvercle sur le pourtour

    difference() {
        union() {
            // Plaque principale
            translate([0, BOX_D/2 - WALL/2 - LID_THICKNESS/2, BOX_H/2])
                cube([lid_w + overlap, LID_THICKNESS, lid_h + overlap], center = true);

            // Lèvre de centrage (pénètre dans l'ouverture)
            translate([0, BOX_D/2 - WALL - 0.5, BOX_H/2])
                cube([lid_w - 0.4, 1.5, lid_h - 0.4], center = true);

            // Ergots de clip (haut et bas, 2 chacun)
            for (zx = [-1, 1]) {
                for (zy = [-1, 1]) {
                    translate([zx * (lid_w/2 - 5), BOX_D/2 - WALL + 0.5, BOX_H/2 + zy * (lid_h/2 - 5)])
                        rotate([0, 45, 0])
                            cube([2, 2, 3], center = true);
                }
            }
        }

        // Trou guide lumière LED (aligné avec celui du corps)
        translate([-BOX_W/4, BOX_D/2 - WALL/2 - LID_THICKNESS/2, HIGH_Z_START + CHAMBER_HIGH_H * 0.7])
            rotate([0, 90, 0])
                cylinder(d = LED_HOLE_D, h = LID_THICKNESS + 0.2, center = true, $fn = 24);

        // Trous vis M2 (2 vis aux coins haut/bas)
        for (zy = [-1, 1]) {
            translate([0, BOX_D/2 - WALL/2 - LID_THICKNESS/2, BOX_H/2 + zy * (lid_h/2 - 6)])
                rotate([0, 90, 0])
                    cylinder(d = LID_SCREW_D, h = LID_THICKNESS + 0.2, center = true, $fn = 24);
        }
    }
}

// =============================================================================
// Assemblage final
// =============================================================================

// Corps principal
main_body();

// Berceaux intérieurs
sensor_cradle();
esp32_cradle();

// Couvercle (désactivé par défaut pour visualisation intérieure)
// Décommenter pour export STL complet :
// lid();

// =============================================================================
// Notes d'impression 3D
// =============================================================================
// - Matériau   : PETG (stabilité thermique, faible conductivité)
// - Imprimante : Prusa Mini+ (plateau 180×180 mm)
// - Orientation : Face arrière sur le plateau (trous de fixation visibles)
// - Support     : Aucun (design auto-porteur)
// - Remplissage : 15-20% gyroïde
// - Périmètres  : 2-3 (rigidité)
// - Buse        : 0.4 mm standard
// - Hauteur couche : 0.20 mm QUALITY
// =============================================================================
