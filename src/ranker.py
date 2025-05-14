"""
Ranks articles based on profile scores.
"""
from typing import List, Dict, Any
from .profiler import Profiler


class Ranker:
    @staticmethod
    def rank(items: List[Dict[str, Any]], profile: Dict[str, float]) -> List[Dict[str, Any]]:
        profiler = Profiler(profile)
        scored = [(profiler.score(it['summary']), it) for it in items]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [it for _, it in scored]