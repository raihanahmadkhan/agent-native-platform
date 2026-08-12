from fastapi import Header, HTTPException

from app.data.seed_agents import AGENTS
from app.schemas.agent import Agent

AGENTS_BY_KEY = {a["api_key"]: a for a in AGENTS}


def require_agent(x_agent_key: str = Header(...)) -> Agent:
    """
    FastAPI dependency. Attach with Depends(require_agent) on any route whose
    capability has "Auth required? Yes" in docs/spec.md (currently create_order,
    track_order, cancel_order — none built yet). Not used by search_restaurants
    or search_items, which are public per the spec.

    Checking scope/spending_limit against the requested action is the policy
    engine's job (build order step 3), not this dependency's — this only
    answers "who is this agent," not "is this agent allowed to do this."
    """
    record = AGENTS_BY_KEY.get(x_agent_key)
    if record is None:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Agent-Key")
    return Agent(**record)
