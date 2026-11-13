<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carte — Château de Neuschwanstein</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body { margin: 0; } #map { width: 100vw; height: 100vh; }
  .legend { background: white; padding: 8px 12px; border-radius: 4px; box-shadow: 0 1px 5px rgba(0,0,0,0.3); font: 13px/1.5 sans-serif; }
  .legend i { width: 14px; height: 14px; display: inline-block; margin-right: 6px; border-radius: 50%; vertical-align: middle; }
</style>
</head>
<body>
<div id="map"></div>
<script>
const map = L.map("map").setView([47.5575522, 10.7496959], 10);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 18,
}).addTo(map);

// Cercle 50 km
L.circle([47.5575522, 10.7496959], {
    radius: 50000,
    color: "#3388ff",
    fillColor: "#3388ff",
    fillOpacity: 0.08,
    weight: 2,
    dashArray: "6 8",
}).addTo(map);

// Point d'intérêt central
L.marker([47.5575522, 10.7496959])
    .bindPopup("<b>📍 Château de Neuschwanstein</b>")
    .addTo(map)
    .openPopup();

// Réserves naturelles (vert)
const reserveIcon = L.divIcon({ className: "", html: "🌿", iconSize: [24, 24], iconAnchor: [12, 12] });
L.marker([47.3962232, 10.9227601]).bindPopup("<b>🌿 Dorflinde</b><br>Réserve naturelle").addTo(map),
        L.marker([47.7056289, 10.9553599]).bindPopup("<b>🌿 Bichlbauernfilz mit Schwaigsee</b><br>Zone protégée").addTo(map),
        L.marker([47.6108315, 10.9975461]).bindPopup("<b>🌿 Naturpark Ammergauer Alpen</b><br>Zone protégée").addTo(map);

// Restaurants (orange)
const restoIcon = L.divIcon({ className: "", html: "🍽", iconSize: [24, 24], iconAnchor: [12, 12] });
L.marker([47.6755297, 10.7938162], {icon: restoIcon}).bindPopup("<b>🍽 Wirtshaus in der Lechaue</b><br>[[Cuisine]] variée").addTo(map),
        L.marker([47.5680689, 10.6956606], {icon: restoIcon}).bindPopup("<b>🍽 Beim Olivenbauer</b><br>Italian;regional").addTo(map),
        L.marker([47.5804766, 10.7101722], {icon: restoIcon}).bindPopup("<b>🍽 Mar Y Sol</b><br>[[Cuisine]] variée").addTo(map);

// Cercle 25 km (zone réserves)
L.circle([47.5575522, 10.7496959], {
    radius: 25000,
    color: "#228B22",
    fillColor: "#228B22",
    fillOpacity: 0.04,
    weight: 1,
    dashArray: "3 6",
}).addTo(map);

// Légende
const legend = L.control({ position: "bottomright" });
legend.onAdd = function() {
    const div = L.DomUtil.create("div", "legend");
    div.innerHTML = "<b>Légende</b><br>" +
        "<i style='background:#3388ff'></i> Zone 50 km<br>" +
        "<i style='background:#228B22'></i> Réserves 25 km<br>" +
        "<span style='font-size:16px'>🌿</span> Réserve naturelle<br>" +
        "<span style='font-size:16px'>🍽</span> Restaurant<br>" +
        "<span style='font-size:16px'>📍</span> Point d'intérêt";
    return div;
};
legend.addTo(map);
</script>
</body>
</html>