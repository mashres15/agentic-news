"""
Scores summaries based on user-defined keyword weights.
"""
import re
from typing import Dict, Any


class Profiler:
    def __init__(self, profile: Dict[str, float]) -> None:
        self.profile = profile

    def score(self, text: str) -> float:
        score = 0.0
        for kw, weight in self.profile.items():
            if re.search(rf"{re.escape(kw)}", text, re.IGNORECASE):
                score += weight
        return score