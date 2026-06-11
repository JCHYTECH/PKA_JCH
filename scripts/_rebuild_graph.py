#!/usr/bin/env python3
"""Rebuild graphify graph from graph.json after semantic merge."""
import json, sys
sys.path.insert(0, '/Users/jchavauxm5/.local/share/uv/tools/graphifyy/lib/python3.13/site-packages')
from networkx.readwrite import json_graph
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json
from pathlib import Path

out = Path('graphify-out')
graph_json = out / 'graph.json'
raw = json.loads(graph_json.read_text(encoding='utf-8'))
G = build_from_json(raw)
print(f'Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges')

print('Clustering...')
communities = cluster(G)
cohesion = score_all(G, communities)
gods = god_nodes(G)
surprises = surprising_connections(G, communities)
labels = {cid: f'Community {cid}' for cid in communities}
questions = suggest_questions(G, communities, labels)

print('Generating report...')
report = generate(G, communities, cohesion, labels, gods, surprises,
                  {'warning': 'post-merge semantic rebuild'},
                  {'input': 0, 'output': 0}, '.', suggested_questions=questions)

(out / 'GRAPH_REPORT.md').write_text(report, encoding='utf-8')
to_json(G, communities, str(graph_json))
print(f'Done — {len(communities)} communities, GRAPH_REPORT.md + graph.json updated.')
