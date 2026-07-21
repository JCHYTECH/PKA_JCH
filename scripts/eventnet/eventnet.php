<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EventNET — Indice sonore wildlife</title>
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
.section-title{font-size:1.05em;margin:20px 0 10px;color:#cbd5e1}
table{width:100%;border-collapse:collapse;background:#1e293b;border-radius:10px;overflow:hidden}
th{text-align:left;padding:10px 14px;background:#334155;font-size:0.8em;text-transform:uppercase;color:#94a3b8}
td{padding:10px 14px;font-size:0.9em;border-top:1px solid #334155}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.8em;font-weight:600}
.badge.anthropic{background:#581c87;color:#e9d5ff}
.badge.weather{background:#164e63;color:#a5f3fc}
.badge.orage{background:#7c2d12;color:#fca5a5}
.badge.tonnerre{background:#7c2d12;color:#fca5a5}
.badge.pluie{background:#1e3a5f;color:#93c5fd}
.badge.vent{background:#365314;color:#bef264}
.level-none{color:#94a3b8}
.level-low{color:#bef264}
.level-moderate{color:#fde68a}
.level-high{color:#fca5a5}
.metrics{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:8px;color:#cbd5e1;font-size:0.8em}
.metric{background:#0f172a;border-radius:8px;padding:5px 8px}
.score{font-family:monospace;color:#38bdf8}
.empty{text-align:center;color:#64748b;padding:40px}
.footer{text-align:center;margin-top:20px;color:#475569;font-size:0.7em}
.footer a{color:#38bdf8}
</style>
</head>
<body>

<h1>EventNET</h1>
<p class="sub">Indice de pollution sonore anthropique wildlife — rafraichissement 15s</p>

<?php
$db = new SQLite3('/home/jchavaux/BirdNET-Pi/eventnet/events.db');

$latestIndex = $db->querySingle("SELECT window_start, window_end, anthropic_noise_score, anthropic_noise_level, dominant_anthropic_source, anthropic_event_count, max_anthropic_score, avg_rms_dbfs, max_peak_dbfs, max_clipping_ratio FROM noise_index ORDER BY window_start DESC LIMIT 1", true);

$stats = $db->query("SELECT event_group, class_name_fr, COUNT(*) as cnt, ROUND(AVG(score),3) as avg, ROUND(MAX(score),3) as max FROM events GROUP BY event_group, class_name_fr ORDER BY event_group, cnt DESC");
$counts = ['weather' => [], 'anthropic' => []];
$total = 0;
while ($row = $stats->fetchArray(SQLITE3_ASSOC)) {
    $group = $row['event_group'] ?: 'weather';
    if (!isset($counts[$group])) $counts[$group] = [];
    $counts[$group][$row['class_name_fr']] = $row;
    $total += $row['cnt'];
}
?>

<?php if ($latestIndex): ?>
<div class="card">
<div class="label">Indice pollution sonore anthropique</div>
<div class="count level-<?= htmlspecialchars($latestIndex['anthropic_noise_level']) ?>"><?= number_format($latestIndex['anthropic_noise_score'], 0) ?></div>
<div class="label"><?= htmlspecialchars($latestIndex['anthropic_noise_level']) ?> — <?= htmlspecialchars($latestIndex['dominant_anthropic_source'] ?? 'aucune source dominante') ?></div>
<div class="metrics">
<span class="metric">RMS <?= $latestIndex['avg_rms_dbfs'] === null ? 'n/a' : number_format($latestIndex['avg_rms_dbfs'], 1) . ' dBFS' ?></span>
<span class="metric">Peak <?= $latestIndex['max_peak_dbfs'] === null ? 'n/a' : number_format($latestIndex['max_peak_dbfs'], 1) . ' dBFS' ?></span>
<span class="metric">Clip <?= $latestIndex['max_clipping_ratio'] === null ? 'n/a' : number_format($latestIndex['max_clipping_ratio'] * 100, 2) . '%' ?></span>
</div>
<div class="max">fenetre: <?= htmlspecialchars($latestIndex['window_start']) ?> → <?= htmlspecialchars($latestIndex['window_end']) ?> · evenements: <?= intval($latestIndex['anthropic_event_count']) ?></div>
</div>
<?php else: ?>
<div class="card"><div class="label">Indice pollution sonore anthropique</div><div class="count level-none">0</div><div class="label">en attente de donnees</div></div>
<?php endif; ?>

<?php foreach (['weather' => 'Meteo acoustique', 'anthropic' => 'Bruit anthropique'] as $group => $title): ?>
<h2 class="section-title"><?= $title ?></h2>
<div class="grid">
<?php foreach (($counts[$group] ?? []) as $name => $row): ?>
<div class="card">
<div class="count"><?= $row['cnt'] ?></div>
<div class="label"><?= htmlspecialchars($name) ?></div>
<div class="max">max: <?= $row['max'] ?></div>
</div>
<?php endforeach; ?>
<?php if (empty($counts[$group])): ?>
<div class="card"><div class="count">0</div><div class="label">Aucun evenement</div></div>
<?php endif; ?>
</div>
<?php endforeach; ?>

<?php
$latest = $db->query("SELECT timestamp, event_group, class_name_fr, score FROM events ORDER BY id DESC LIMIT 30");
$rows = [];
while ($r = $latest->fetchArray(SQLITE3_ASSOC)) $rows[] = $r;
if ($rows):
?>
<table>
<tr><th>Heure</th><th>Groupe</th><th>Evenement</th><th>Score</th></tr>
<?php foreach ($rows as $r):
    $time = explode('T', $r['timestamp'])[1] ?? $r['timestamp'];
?>
<tr>
<td><?= htmlspecialchars($time) ?></td>
<td><span class="badge <?= htmlspecialchars($r['event_group'] ?: 'weather') ?>"><?= htmlspecialchars($r['event_group'] ?: 'weather') ?></span></td>
<td><?= htmlspecialchars($r['class_name_fr']) ?></td>
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
