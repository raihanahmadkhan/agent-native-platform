from enum import Enum

from app.schemas.agent import Agent


class ActionCategory(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    FINANCIAL = "FINANCIAL"
    DESTRUCTIVE = "DESTRUCTIVE"


class PolicyDecision(str, Enum):
    ALLOWED = "ALLOWED"
    REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
    DENIED = "DENIED"


def check_policy(
    agent: Agent,
    action: str,
    category: ActionCategory,
    amount: float | None = None,
) -> PolicyDecision:
    """
    See docs/spec.md section 6 for the rule table this implements.

    `amount` only matters for FINANCIAL actions (e.g. create_order's total).
    A DESTRUCTIVE decision here is unconditional ("always requires_approval on
    first call") — this engine has no notion of a previously-granted approval;
    handling that (letting a second, pre-approved call through) is the
    capability's job once cancel_order exists (build order step 5), not this
    engine's.
    """
    if action not in agent.scopes:
        return PolicyDecision.DENIED

    if category in (ActionCategory.READ, ActionCategory.WRITE):
        return PolicyDecision.ALLOWED

    if category == ActionCategory.FINANCIAL:
        if amount is not None and amount <= agent.spending_limit:
            return PolicyDecision.ALLOWED
        return PolicyDecision.REQUIRES_APPROVAL

    return PolicyDecision.REQUIRES_APPROVAL  # DESTRUCTIVE
