# Bridgit Matching Prototype runner
import json, sys
from pathlib import Path
from matchlib.scoring import load_profiles, top_k_for_all

ROOT = Path(__file__).resolve().parent
DATA_DEFAULT = ROOT / "data" / "sampleData_Bridgit.tsv"
DATA_FALLBACK = ROOT / "data" / "sample_profiles.tsv"
OUT = ROOT / "out" / "match_results.json"

data_path = DATA_DEFAULT if DATA_DEFAULT.exists() else DATA_FALLBACK
print(f"Using dataset: {data_path}")

profiles = load_profiles(str(data_path))
results = top_k_for_all(profiles, k=3)
OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Wrote {OUT}")
print("Open the JSON to inspect top-3 matches per visible user.")
