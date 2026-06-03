<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EventNET — Meteo acoustique</title>
<meta http-equiv="refresh" content="15">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0f172a;color:#e2e8f0;padding:20px;min-height:100vh}
h1{font-size:1.5em;margin-bottom:4px}
h1 span{color:#38bdf8}
.sub{color:#64748b;font-size:0.85em;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:24px}
.card{background:#1e293b;border-radius:10px;padding:16px;text-align:center}
.card .icon{font-size:2em;margin-bottom:6px}
.card .count{font-size:2em;font-weight:700}
.card .label{font-size:0.8em;color:#94a3b8;margin-top:4px}
.card .max{font-size:0.75em;color:#64748b}
table{width:100%;border-collapse:collapse;background:#1e293b;border-radius:10px;overflow:hidden}
th{text-align:left;padding:10px 14px;background:#334155;font-size:0.8em;text-transform:uppercase;color:#94a3b8}
td{padding:10px 14px;font-size:0.9em;border-top:1px solid #334155}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.8em;font-weight:600}
.badge.orage{background:#7c2d12;color:#fca5a5}
.badge.tonnerre{background:#7c2d12;color:#fca5a5}
.badge.pluie{background:#1e3a5f;color:#93c5fd}
.badge.vent{background:#365314;color:#bef264}
.score{font-family:monospace;color:#38bdf8}
.empty{text-align:center;color:#64748b;padding:40px}
.footer{text-align:center;margin-top:20px;color:#475569;font-size:0.7em}
.footer a{color:#38bdf8}
</style>
</head>
<body>

<h1>EventNET</h1>
<p class="sub">Detection acoustique meteo — rafraichissement 15s</p>

<?php
$db = new SQLite3('/home/jchavaux/BirdNET-Pi/eventnet/events.db');
$stats = $db->query("SELECT class_name_fr, COUNT(*) as cnt, ROUND(AVG(score),3) as avg, ROUND(MAX(score),3) as max FROM events GROUP BY class_name_fr ORDER BY cnt DESC");
$counts = [];
$total = 0;
while ($row = $stats->fetchArray(SQLITE3_ASSOC)) {
    $counts[$row['class_name_fr']] = $row;
    $total += $row['cnt'];
}
$icons = ['Tonnerre'=>'Thunder','Orage'=>'Storm','Pluie'=>'Rain','Pluie (surface)'=>'Droplets','Vent'=>'Wind','Vent (micro)'=>'Mic'];
$badges = ['Tonnerre'=>'tonnerre','Orage'=>'orage','Pluie'=>'pluie','Pluie (surface)'=>'pluie','Vent'=>'vent','Vent (micro)'=>'vent'];
?>

<div class="grid">
<?php foreach ($counts as $name => $row): ?>
<div class="card">
<div class="icon"><?= $icons[$name] ?? 'Note' ?></div>
<div class="count"><?= $row['cnt'] ?></div>
<div class="label"><?= htmlspecialchars($name) ?></div>
<div class="max">max: <?= $row['max'] ?></div>
</div>
<?php endforeach; ?>
<?php if (empty($counts)): ?>
<div class="card"><div class="icon">Clock</div><div class="count">0</div><div class="label">En attente...</div></div>
<?php endif; ?>
</div>

<?php
$latest = $db->query("SELECT timestamp, class_name_fr, score FROM events ORDER BY id DESC LIMIT 30");
$rows = [];
while ($r = $latest->fetchArray(SQLITE3_ASSOC)) $rows[] = $r;
if ($rows):
?>
<table>
<tr><th>Heure</th><th>Evenement</th><th>Score</th></tr>
<?php foreach ($rows as $r):
    $time = explode('T', $r['timestamp'])[1] ?? $r['timestamp'];
    $badge = $badges[$r['class_name_fr']] ?? 'pluie';
?>
<tr>
<td><?= htmlspecialchars($time) ?></td>
<td><span class="badge <?= $badge ?>"><?= htmlspecialchars($r['class_name_fr']) ?></span></td>
<td class="score"><?= number_format($r['score'], 3) ?></td>
</tr>
<?php endforeach; ?>
</table>
<?php else: ?>
<div class="empty">Aucune detection pour l'instant.</div>
<?php endif; ?>

<div class="footer">
Total : <strong><?= $total ?></strong> evenements — <a href="http://100.66.110.60">BirdNET-Pi</a>
</div>
</body>
</html>
