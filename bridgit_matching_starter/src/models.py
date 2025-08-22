from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Profile:
    data: Dict[str, Any]

@dataclass
class Context:
    data: Dict[str, Any]

@dataclass
class MatchRequest:
    profile_a: Profile
    profile_b: Profile
    context: Context

@dataclass
class MatchResult:
    score: float
    factors: List[str]
    risks: List[str]
    suggestions: List[Dict[str, str]]
