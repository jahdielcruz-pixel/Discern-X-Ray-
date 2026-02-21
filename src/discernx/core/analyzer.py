from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import re


@dataclass
class Claim:
    id: int
    text: str
    signals: List[str]
    risk_score: int  # 0-100


@dataclass
class AnalysisResult:
    input_text: str
    claims: List[Claim]
    overall_risk: int
    notes: List[str]


SENSATIONAL_PATTERNS = [
    r"\b(shocking|bombshell|exposed|they don’t want you to know|wake up)\b",
    r"\b(secret|cover[- ]?up|hidden truth)\b",
    r"\b(guaranteed|always|never|everyone knows)\b",
]

UNCERTAIN_SOURCING = [
    r"\b(i heard|people say|word is|rumor has it|someone told me)\b",
    r"\b(allegedly|supposedly)\b",
]

CALL_TO_ACTION = [
    r"\b(share this|send this to|before it’s deleted|spread the word)\b",
]

NUMERIC_CLAIM = r"\b\d+(\.\d+)?%?\b"

URL_PATTERN = r"https?://\S+|www\.\S+"


def split_into_candidate_claims(text: str) -> List[str]:
    # Simple approach: split by sentence-ish boundaries.
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts


def score_claim(claim: str) -> (int, List[str]):
    signals: List[str] = []
    score = 0

    if re.search(URL_PATTERN, claim, flags=re.I):
        signals.append("has_link")
        score -= 5  # link isn't proof, but it's better than none

    if re.search(NUMERIC_CLAIM, claim):
        signals.append("has_numbers")
        score += 10

    for pat in SENSATIONAL_PATTERNS:
        if re.search(pat, claim, flags=re.I):
            signals.append("sensational_language")
            score += 25
            break

    for pat in UNCERTAIN_SOURCING:
        if re.search(pat, claim, flags=re.I):
            signals.append("uncertain_sourcing")
            score += 20
            break

    for pat in CALL_TO_ACTION:
        if re.search(pat, claim, flags=re.I):
            signals.append("viral_call_to_action")
            score += 15
            break

    # Very short "claims" are often fragments and less reliable for analysis
    if len(claim.split()) < 6:
        signals.append("very_short")
        score += 10

    # Clamp 0-100
    score = max(0, min(100, score))
    return score, signals


def analyze_text(text: str, max_claims: int = 12) -> AnalysisResult:
    candidates = split_into_candidate_claims(text)
    candidates = candidates[:max_claims]

    claims: List[Claim] = []
    for idx, c in enumerate(candidates, start=1):
        risk, signals = score_claim(c)
        claims.append(Claim(id=idx, text=c, signals=signals, risk_score=risk))

    # Overall risk: average + bonus if many high-risk claims
    if claims:
        avg = sum(c.risk_score for c in claims) / len(claims)
        high = sum(1 for c in claims if c.risk_score >= 60)
        overall = int(min(100, avg + high * 5))
    else:
        overall = 0

    notes = [
        "MVP heuristics only (not fact-checking).",
        "High risk = more manipulation-style signals or weak sourcing markers.",
        "Next step: add source retrieval + citation checking + contradiction checks."
    ]

    return AnalysisResult(input_text=text, claims=claims, overall_risk=overall, notes=notes)


def to_dict(result: AnalysisResult) -> Dict[str, Any]:
    return {
        "input_text": result.input_text,
        "overall_risk": result.overall_risk,
        "notes": result.notes,
        "claims": [asdict(c) for c in result.claims],
    }