# Bridgit Matching Prototype (v2)

This is a self-contained prototype for scoring matches between profiles.

## Run
```bash
cd bridgit_matching_proto_v2
python run_prototype.py
```
- If `data/profiles.tsv` exists, it will be used.
- Otherwise, the script falls back to `data/sample_profiles.tsv` (included).

## Input format (TSV columns)
```
birthday	currentCompany	gender	homeLocation	industry	interests	occupation	pitches	realTimeAvailability	searchDistanceType	visibility	visibilityGender
YYYY-MM-DD	Company	male|female|other	City, State, Country	free text	["A","B"]	free text	["pitch1","pitch2"]	TRUE|FALSE	<ignored>	TRUE|FALSE	TRUE|FALSE
```

## Output
- `out/match_results.json` — top-3 matches per visible profile with explanations.

## Notes
- No external packages required (pure Python).
- You can paste your full dataset as `data/profiles.tsv` with the above header.
