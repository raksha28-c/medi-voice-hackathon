from __future__ import annotations

from typing import List

from mock_qdrant import search_symptoms as search_mock_symptoms

SEARCH_PROVIDER = "local-mock"


def search_symptoms(query: str, top_k: int = 3) -> List[dict]:
    """
    Unified search entry point for the backend.

    This keeps the FastAPI app decoupled from whichever search backend we
    choose later. For now we rely on the local structured symptom database,
    which makes the project runnable without external infrastructure.
    """
    return search_mock_symptoms(query, top_k=top_k)
