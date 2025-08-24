
"""
Very small schema helpers (no heavy deps). We validate basic types and keys.
"""

from typing import Dict, Any, List

MATCH_SCHEMA = {
    "score": float,
    "factors": list,
    "risks": list,
    "suggestions": list,
}

def validate_match_result(obj: Dict[str, Any]) -> bool:
    try:
        assert isinstance(obj, dict)
        assert "score" in obj and isinstance(obj["score"], (int, float))
        assert 0.0 <= float(obj["score"]) <= 1.0
        assert isinstance(obj.get("factors", []), list)
        assert isinstance(obj.get("risks", []), list)
        assert isinstance(obj.get("suggestions", []), list)
        for s in obj.get("suggestions", []):
            assert isinstance(s, dict)
            assert s.get("for") in ("initiator", "recipient")
            assert isinstance(s.get("text", ""), str)
        return True
    except AssertionError:
        return False
