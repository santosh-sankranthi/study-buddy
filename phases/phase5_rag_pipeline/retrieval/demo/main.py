"""DEMO -- Retrieval with Minimum Confidence Thresholds.

Live-code target: call retrieve() from app.vector_store with min_similarity=0.3,
showing how on-topic queries succeed while off-topic queries return None.

Run:
    python phases/phase5_rag_pipeline/retrieval/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import retrieve

print("=" * 60)
print("RETRIEVAL WITH CONFIDENCE THRESHOLD DEMO")
print("=" * 60)

# 1. On-topic query
query_on_topic = "How does the electron transport chain generate ATP?"
print(f"\n1. On-topic query: '{query_on_topic}'")
results_on = retrieve(query_on_topic, k=2, min_similarity=0.3)
if results_on:
    print(f"  Retrieved {len(results_on)} relevant chunk(s):")
    for r in results_on:
        sim = round(1.0 - r["distance"], 4)
        print(f"    Similarity: {sim} | File: {r['metadata'].get('filename')} | {r['text'][:60]}...")
else:
    print("  No chunks passed the similarity threshold.")

# 2. Irrelevant query
query_off_topic = "What is the capital city of Australia?"
print(f"\n2. Off-topic query: '{query_off_topic}'")
results_off = retrieve(query_off_topic, k=2, min_similarity=0.3)
if results_off:
    print(f"  Retrieved {len(results_off)} chunk(s).")
else:
    print("  ✅ Correctly returned None! No irrelevant chunks passed the confidence threshold.")
