import pytest
from fastapi import HTTPException

from app.auth.agent_auth import require_agent


def test_valid_key_returns_agent():
    agent = require_agent(x_agent_key="dev-key-shopping-001")
    assert agent.agent_id == "agent-shopping-assistant"
    assert "create_order" in agent.scopes
    assert agent.spending_limit == 500.0


def test_readonly_agent_has_no_write_scopes():
    agent = require_agent(x_agent_key="dev-key-readonly-002")
    assert agent.scopes == ["search_restaurants", "search_items"]


def test_tight_budget_agent_has_low_limit():
    agent = require_agent(x_agent_key="dev-key-tight-003")
    assert agent.spending_limit == 50.0


def test_unknown_key_raises_401():
    with pytest.raises(HTTPException) as exc_info:
        require_agent(x_agent_key="not-a-real-key")
    assert exc_info.value.status_code == 401
