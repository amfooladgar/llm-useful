import csv, re, math, ast, datetime, json
from collections import Counter
from pathlib import Path

STOPWORDS = set(["the","and","of","in","to","for","a","an","on","with","at","by","from","about","into","as","is","are","be","this","that","it","i","im","i’m","you","we","they","their","our","your"])

def tokenize(text: str):
    if text is None:
        return []
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    toks = [t for t in text.split() if t and t not in STOPWORDS]
    return toks

def bow(text: str):
    return Counter(tokenize(text))

def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    inter = set(a.keys()) & set(b.keys())
    num = sum(a[t]*b[t] for t in inter)
    den = (sum(v*v for v in a.values()))**0.5 * (sum(v*v for v in b.values()))**0.5
    return 0.0 if den == 0 else num/den

def parse_jsonish_list(s):
    if s is None:
        return []
    s = s.strip()
    try:
        val = ast.literal_eval(s)
        if isinstance(val, list):
            return [str(x) for x in val if str(x).strip()]
    except Exception:
        pass
    if '"' in s:
        items = [x.strip().strip('"') for x in s.split(',')]
        return [i for i in items if i and i != '[]']
    return [s] if s else []

def jaccard(list_a, list_b):
    A = set([x.strip().lower() for x in list_a if x and x != '[]'])
    B = set([x.strip().lower() for x in list_b if x and x != '[]'])
    if not A and not B:
        return 0.0
    return len(A & B) / len(A | B)

def parse_bool(x):
    return True if str(x).strip().upper() == "TRUE" else False

def parse_date(d):
    d = str(d).strip()
    if d == "0" or d.lower() == "null" or d == "":
        return None
    try:
        return datetime.date.fromisoformat(d)
    except Exception:
        return None

def calc_age(dob):
    if not dob: return None
    today = datetime.date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return years

NY_ALIASES = {"nyc":"new york","new york city":"new york"}

def normalize_city(raw):
    s = str(raw or "").lower()
    for k,v in NY_ALIASES.items():
        s = s.replace(k, v)
    s = s.replace("united states", "usa").replace("u.s.", "usa").replace("us", "usa")
    s = s.replace("ş", "s").replace("швейцарія", "switzerland")
    parts = [p.strip() for p in s.split(",")]
    city = parts[0] if parts else ""
    region = parts[1] if len(parts) > 1 else ""
    country = parts[-1] if parts else ""
    return city, region, country

def location_score(locA, locB):
    a_city, a_region, a_country = normalize_city(locA)
    b_city, b_region, b_country = normalize_city(locB)
    if a_city and b_city and a_city == b_city:
        return 1.0
    if a_region and b_region and a_region == b_region and a_region != "":
        return 0.8
    if a_country and b_country and a_country == b_country and a_country != "":
        return 0.5
    return 0.0

def age_compat(ageA, ageB):
    if ageA is None or ageB is None:
        return 0.5
    gap = abs(ageA - ageB)
    if gap <= 5: return 1.0
    if gap <= 10: return 0.8
    if gap <= 15: return 0.6
    if gap <= 20: return 0.4
    return 0.2

def industry_tokens(raw):
    s = str(raw or "").lower()
    synonyms = {
        "tech":"technology",
        "technik":"technology",
        "technolog":"technology",
        "finance":"finance",
        "finanzen":"finance",
        "verkauf":"sales",
        "gesundhei":"health",
        "health":"health",
        "sales":"sales"
    }
    toks = set()
    for k,v in synonyms.items():
        if k in s:
            toks.add(v)
    for w in ["technology","finance","health","sales"]:
        if w in s: toks.add(w)
    return toks

def token_set_sim(a_tokens, b_tokens):
    if not a_tokens and not b_tokens: return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens) if (a_tokens|b_tokens) else 0.0

def occupation_sim(a_occ, b_occ):
    return cosine(bow(a_occ), bow(b_occ))

def pitches_text(pitches_list):
    if isinstance(pitches_list, list):
        return " ".join([str(x) for x in pitches_list])
    return str(pitches_list or "")

WEIGHTS = {
    "location": 0.25,
    "pitches": 0.25,
    "industry": 0.10,
    "occupation": 0.05,
    "interests": 0.10,
    "availability": 0.15,
    "age": 0.10
}

COLUMNS = ["birthday","currentCompany","gender","homeLocation","industry","interests","occupation","pitches","realTimeAvailability","searchDistanceType","visibility","visibilityGender"]

def load_profiles(tsv_path: str):
    profiles = []
    with open(tsv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            profile = {
                "birthday": parse_date(row.get("birthday","")),
                "currentCompany": (row.get("currentCompany","") or "").strip(),
                "gender": (row.get("gender","") or "").strip().lower(),
                "homeLocation": (row.get("homeLocation","") or "").strip(),
                "industry_raw": row.get("industry",""),
                "industry_tokens": industry_tokens(row.get("industry","")),
                "interests": parse_jsonish_list(row.get("interests","[]")),
                "occupation": row.get("occupation",""),
                "pitches": parse_jsonish_list(row.get("pitches","[]")),
                "pitches_text": pitches_text(parse_jsonish_list(row.get("pitches","[]"))),
                "realTimeAvailability": parse_bool(row.get("realTimeAvailability","FALSE")),
                "searchDistanceType": str(row.get("searchDistanceType","")).strip().lower(),
                "visibility": parse_bool(row.get("visibility","TRUE")),
                "visibilityGender": parse_bool(row.get("visibilityGender","TRUE"))
            }
            profile["age"] = calc_age(profile["birthday"])
            profiles.append(profile)
    return profiles

def jaccard(list_a, list_b):
    A = set([x.strip().lower() for x in list_a if x and x != '[]'])
    B = set([x.strip().lower() for x in list_b if x and x != '[]'])
    if not A and not B:
        return 0.0
    return len(A & B) / len(A | B)

def match_score(A, B):
    if not (A["visibility"] and B["visibility"]):
        return None

    loc = location_score(A["homeLocation"], B["homeLocation"])
    pit = cosine(bow(A["pitches_text"]), bow(B["pitches_text"]))
    ind = token_set_sim(A["industry_tokens"], B["industry_tokens"])
    occ = occupation_sim(A["occupation"], B["occupation"])
    ints = jaccard(A["interests"], B["interests"])
    ava = 1.0 if (A["realTimeAvailability"] and B["realTimeAvailability"]) else 0.0
    agec = age_compat(A["age"], B["age"])

    score = (
        WEIGHTS["location"] * loc +
        WEIGHTS["pitches"] * pit +
        WEIGHTS["industry"] * ind +
        WEIGHTS["occupation"] * occ +
        WEIGHTS["interests"] * ints +
        WEIGHTS["availability"] * ava +
        WEIGHTS["age"] * agec
    )

    if A["currentCompany"] and A["currentCompany"] != "0" and A["currentCompany"].lower() == B["currentCompany"].lower():
        score = min(1.0, score + 0.03)

    factors = []
    risks = []

    if loc >= 0.8: factors.append("Near each other (same city/region)")
    if pit >= 0.6: factors.append("Aligned goals in pitches")
    if ind >= 0.5: factors.append("Similar or related industries")
    if occ >= 0.5: factors.append("Similar roles")
    if ints >= 0.3: factors.append(f"Shared interests ({int(100*ints)}% overlap)")
    if ava >= 1.0: factors.append("Both available now")

    if A["age"] and B["age"] and abs(A["age"]-B["age"]) >= 15:
        risks.append("Large age gap")
    if pit < 0.3:
        risks.append("Unclear or different goals")
    if occ < 0.2:
        risks.append("Different roles or seniority")

    shared_ints = list(set([i for i in A["interests"] if i.lower() in [x.lower() for x in B["interests"]]]))
    opener_topic = shared_ints[0] if shared_ints else (B["occupation"] or "projects")
    sugg_initiator = f"Noticed we both like {opener_topic}. Up for a quick chat?"
    sugg_recipient = f"Happy to connect if helpful—I can share about {B['occupation'] or 'my work'}."

    return {
        "score": round(float(score), 4),
        "factors": factors[:4],
        "risks": risks[:3],
        "suggestions": [
            {"for":"initiator","text": sugg_initiator},
            {"for":"recipient","text": sugg_recipient}
        ]
    }

def top_k_for_all(profiles, k=3):
    outputs = []
    for i, A in enumerate(profiles):
        if not A["visibility"]:
            continue
        scored = []
        for j, B in enumerate(profiles):
            if i == j: 
                continue
            res = match_score(A,B)
            if res is None:
                continue
            scored.append((res["score"], j, res))
        if not scored:
            continue
        scored.sort(reverse=True, key=lambda x: x[0])
        top = scored[:k]
        outputs.append({
            "user_index": i,
            "me": {
                "homeLocation": A["homeLocation"],
                "occupation": A["occupation"],
                "interests": A["interests"][:5],
            },
            "matches": [
                {"other_index": j, "score": s, "summary": r}
                for (s,j,r) in top
            ]
        })
    return outputs
