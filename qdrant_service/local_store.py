from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, List

DATA_FILE = Path(__file__).resolve().parent.parent / "data.txt"
_DATASET: List[Dict[str, str]] = []


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def init_data() -> List[Dict[str, str]]:
    """Load the local healthcare dataset into memory."""
    global _DATASET
    if _DATASET:
        return _DATASET

    data: List[Dict[str, str]] = []
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or "|" not in line:
                continue
            question, answer = [part.strip() for part in line.split("|", 1)]
            data.append({"question": question, "answer": answer})

    _DATASET = data
    return _DATASET


def search_records(query: str, limit: int = 1) -> List[Dict[str, str]]:
    """Find the closest matching records using simple token overlap."""
    query_tokens = set(_tokenize(query))
    if not query_tokens:
        return []

    matches = []
    for entry in init_data():
        question_tokens = set(_tokenize(entry["question"]))
        overlap = len(query_tokens & question_tokens)
        if overlap == 0:
            continue
        matches.append(
            {
                "question": entry["question"],
                "answer": entry["answer"],
                "score": overlap / max(len(question_tokens), 1),
            }
        )

    matches.sort(key=lambda item: item["score"], reverse=True)
    return matches[:limit]


def search_data(query: str, limit: int = 1) -> List[str]:
    return [record["answer"] for record in search_records(query, limit=limit)]
