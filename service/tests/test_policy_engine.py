from app.policy.engine import ActionCategory, PolicyDecision, check_policy
from app.schemas.agent import Agent

FULL_ACCESS = Agent(
    agent_id="a1",
    api_key="k1",
    scopes=["search_items", "create_order", "cancel_order"],
    spending_limit=500.0,
)

READ_ONLY = Agent(
    agent_id="a2",
    api_key="k2",
    scopes=["search_items"],
    spending_limit=0.0,
)


def test_read_allowed_with_scope():
    decision = check_policy(FULL_ACCESS, "search_items", ActionCategory.READ)
    assert decision == PolicyDecision.ALLOWED


def test_read_denied_without_scope():
    decision = check_policy(READ_ONLY, "create_order", ActionCategory.READ)
    assert decision == PolicyDecision.DENIED


def test_write_allowed_with_scope():
    decision = check_policy(FULL_ACCESS, "create_order", ActionCategory.WRITE)
    assert decision == PolicyDecision.ALLOWED


def test_financial_within_limit_allowed():
    decision = check_policy(
        FULL_ACCESS, "create_order", ActionCategory.FINANCIAL, amount=300.0
    )
    assert decision == PolicyDecision.ALLOWED


def test_financial_at_exact_limit_allowed():
    decision = check_policy(
        FULL_ACCESS, "create_order", ActionCategory.FINANCIAL, amount=500.0
    )
    assert decision == PolicyDecision.ALLOWED


def test_financial_over_limit_requires_approval():
    decision = check_policy(
        FULL_ACCESS, "create_order", ActionCategory.FINANCIAL, amount=501.0
    )
    assert decision == PolicyDecision.REQUIRES_APPROVAL


def test_financial_without_scope_is_denied_not_approval():
    decision = check_policy(
        READ_ONLY, "create_order", ActionCategory.FINANCIAL, amount=10.0
    )
    assert decision == PolicyDecision.DENIED


def test_destructive_always_requires_approval():
    decision = check_policy(FULL_ACCESS, "cancel_order", ActionCategory.DESTRUCTIVE)
    assert decision == PolicyDecision.REQUIRES_APPROVAL


def test_destructive_without_scope_is_denied_not_approval():
    decision = check_policy(READ_ONLY, "cancel_order", ActionCategory.DESTRUCTIVE)
    assert decision == PolicyDecision.DENIED
