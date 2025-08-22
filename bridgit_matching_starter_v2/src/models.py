from pydantic import BaseModel, Field
from typing import List, Optional

class Profile(BaseModel):
    currentCompany: Optional[str] = None
    gender: Optional[str] = None
    homeLocation: Optional[str] = None
    industry: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    occupation: Optional[str] = None
    pitches: Optional[List[str]] = None
    realTimeAvailability: Optional[bool] = False

class Context(BaseModel):
    place: Optional[str] = None
    city: Optional[str] = None
    event: Optional[str] = None
    time: Optional[str] = None

class Suggestion(BaseModel):
    for_: str = Field(alias="for")
    text: str

class MatchOutput(BaseModel):
    score: float
    factors: List[str]
    risks: List[str]
    suggestions: List[Suggestion]
