
"""
Simple safety scrubber.
- Removes mentions of protected attributes and risky topics from query text.
- Enforces opt-in language.
"""

import re
from typing import Dict, Any, Tuple, List

PROTECTED_TERMS = [
    r"\brace\b", r"\breligion\b", r"\bpolitics?\b", r"\bsexual\s*orientation\b",
    r"\bhealth\b", r"\bdisab(ility|led)\b", r"\bage\b", r"\bnationality\b",
    r"\bethnicity\b",
]
RISKY_TOPICS = [
    r"\bsalary\b", r"\bdrug(s)?\b", r"\bgambling\b",
]
OPT_IN_PHRASES = [
    "totally fine if not", "no worries if not", "up for", "open to"
]

def scrub_text(text: str) -> Tuple[str, List[str]]:
    risks = []
    clean = text
    for pat in PROTECTED_TERMS + RISKY_TOPICS:
        if re.search(pat, clean, flags=re.I):
            risks.append(f"redacted:{pat}")
            clean = re.sub(pat, "[redacted]", clean, flags=re.I)
    return clean, risks

def ensure_opt_in(s: str) -> str:
    if any(p in s.lower() for p in OPT_IN_PHRASES):
        return s
    # Append a light opt-in suffix if missing
    return s.rstrip(".") + " — totally fine if not."

def scrub_profiles_and_context(initiator: Dict[str, Any], recipient: Dict[str, Any], context: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    risks = []
    # Scrub do_not_mention list from context by marking them as risky
    for item in context.get("do_not_mention", []):
        risks.append(f"do_not_mention:{item}")

    def scrub_fields(d: Dict[str, Any]) -> Dict[str, Any]:
        out = {}
        for k, v in d.items():
            if isinstance(v, str):
                vv, r = scrub_text(v)
                if r: risks.extend(r)
                out[k] = vv
            elif isinstance(v, list):
                nv = []
                for x in v:
                    if isinstance(x, str):
                        xx, r = scrub_text(x)
                        if r: risks.extend(r)
                        nv.append(xx)
                    else:
                        nv.append(x)
                out[k] = nv
            else:
                out[k] = v
        return out

    return scrub_fields(initiator), scrub_fields(recipient), context, list(set(risks))
