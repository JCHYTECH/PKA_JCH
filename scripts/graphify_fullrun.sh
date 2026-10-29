#!/bin/bash
# graphify_fullrun.sh — Extraction sémantique complète + merge + rebuild
cd /Users/jchavauxm5/PKA_JCH
LOG="graphify-out/fullrun.log"

log() { echo "$@" >> "$LOG"; }

log "=== graphify full run — $(date) ==="
log "Model: qwen2.5-coder:14b"
log ""

log "📦 Étape 1/3 : Extraction sémantique..."
python3 -u scripts/graphify_llm_bridge.py --model qwen2.5-coder:14b >> "$LOG" 2>&1
RC=$?
if [ $RC -ne 0 ]; then
    log "❌ Extraction failed with code $RC"
    exit $RC
fi

log ""
log "🔗 Étape 2/3 : Fusion dans le graph..."
python3 -u -c "
import json
from pathlib import Path
graph_path = Path('graphify-out/graph.json')
sem_path = Path('graphify-out/semantic_extraction.json')
with open(graph_path) as f:
    graph = json.load(f)
with open(sem_path) as f:
    semantic = json.load(f)
existing_ids = {n['id'] for n in graph.get('nodes', [])}
new_nodes = sum(1 for n in semantic.get('nodes', []) if n['id'] not in existing_ids)
for n in semantic.get('nodes', []):
    if n['id'] not in existing_ids:
        existing_ids.add(n['id'])
        graph.setdefault('nodes', []).append(n)
existing_edges = {(e['source'], e['target'], e.get('relation','')) for e in graph.get('links', [])}
new_edges = 0
for e in semantic.get('edges', []):
    key = (e['source'], e['target'], e.get('relation',''))
    if key not in existing_edges:
        existing_edges.add(key)
        graph.setdefault('links', []).append(e)
        new_edges += 1
graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False))
print(f'+{new_nodes} semantic nodes, +{new_edges} INFERRED edges merged')
" >> "$LOG" 2>&1

log ""
log "🔄 Étape 3/3 : Rebuild (clustering + report)..."
python3 -u scripts/_rebuild_graph.py >> "$LOG" 2>&1

log ""
log "=== Full run terminé — $(date) ==="
