# Temporary in-memory data source. Replace with a real DB query once
# service/app/models/ + a DB connection are introduced (see docs/architecture.md
# "Build order" step 4 — that's when create_order needs real persistence).

AGENTS = [
    {
        "agent_id": "agent-shopping-assistant",
        "api_key": "dev-key-shopping-001",
        "scopes": [
            "search_restaurants",
            "search_items",
            "create_order",
            "track_order",
            "cancel_order",
        ],
        "spending_limit": 500.0,
    },
    {
        "agent_id": "agent-readonly-explorer",
        "api_key": "dev-key-readonly-002",
        "scopes": ["search_restaurants", "search_items"],
        "spending_limit": 0.0,
    },
    {
        "agent_id": "agent-tight-budget",
        "api_key": "dev-key-tight-003",
        "scopes": [
            "search_restaurants",
            "search_items",
            "create_order",
            "track_order",
            "cancel_order",
        ],
        "spending_limit": 50.0,
    },
]
