#!/bin/bash
# run_all_batches.sh — Loop extraction par lots + merge progressif + rebuild
cd /Users/jchavauxm5/PKA_JCH

MODEL="qwen2.5-coder:14b"
BATCH_SIZE=50
TOTAL=1307
LOG="graphify-out/batch_progress.log"

log() { echo "[$(date +%H:%M:%S)] $@" >> "$LOG"; echo "[$(date +%H:%M:%S)] $@"; }

log "=== Démarrage extraction par lots ==="
log "Modèle: $MODEL, $TOTAL fichiers, lots de $BATCH_SIZE, skip initial 100"

SKIP=100
BATCH_NUM=3

while [ $SKIP -lt $TOTAL ]; do
    OUTFILE="graphify-out/semantic_batch_${BATCH_NUM}.json"
    
    log "Lot $BATCH_NUM: fichiers $SKIP à $((SKIP + BATCH_SIZE))..."
    
    python3 -u scripts/graphify_llm_bridge.py \
        --model "$MODEL" \
        --skip "$SKIP" \
        --max-files "$BATCH_SIZE" \
        --output "$OUTFILE" >> "$LOG" 2>&1
    
    RC=$?
    if [ $RC -ne 0 ]; then
        log "❌ Lot $BATCH_NUM échoué (code $RC)"
    else
        python3 -u -c "
import json
from pathlib import Path
graph_path = Path('graphify-out/graph.json')
batch_path = Path('$OUTFILE')
with open(graph_path) as f: graph = json.load(f)
with open(batch_path) as f: batch = json.load(f)
existing_ids = {n['id'] for n in graph.get('nodes', [])}
nn = sum(1 for n in batch.get('nodes', []) if n['id'] not in existing_ids)
for n in batch.get('nodes', []):
    if n['id'] not in existing_ids:
        existing_ids.add(n['id'])
        graph.setdefault('nodes', []).append(n)
existing_edges = {(e['source'], e['target'], e.get('relation','')) for e in graph.get('links', [])}
ne = 0
for e in batch.get('edges', []):
    key = (e['source'], e['target'], e.get('relation',''))
    if key not in existing_edges:
        existing_edges.add(key)
        graph.setdefault('links', []).append(e)
        ne += 1
graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False))
print(f'+{nn} nodes, +{ne} edges -> total {len(graph[\"nodes\"])} nodes')
" >> "$LOG" 2>&1
        log "✅ Lot $BATCH_NUM mergé"
    fi
    
    SKIP=$((SKIP + BATCH_SIZE))
    BATCH_NUM=$((BATCH_NUM + 1))
done

log ""
log "=== Extraction terminée — rebuild ==="
python3 -u scripts/_rebuild_graph.py >> "$LOG" 2>&1
log "=== Rebuild terminé — $(date) ==="
