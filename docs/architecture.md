# Architecture (v0.1)

Design goal: an AI coding agent should be able to open ONE capability file, infer
the pattern, and correctly build the next one without additional instructions.

## The shape of the project

This is an experiment, not a product. It builds one service twice and measures
the difference:

```
                    THE SAME POSTGRES DATABASE
                    ↑                        ↑
        agent-native layer            human storefront
        (capabilities, manifest,      (minimal browser UI —
         identity, policy, logs)       the CONTROL GROUP)
                    ↑                        ↑
        LLM tool-calling agent        LLM browser agent
                    ↓                        ↓
                    └────── benchmark ───────┘
```

The storefront is deliberately minimal and deliberately unpolished. Its only job
is to be a fair, realistic thing for a browser agent to automate against. Time
spent making it pretty is time not spent on the actual project.

## Directory structure

```
agent-native-platform/
├── CLAUDE.md
├── README.md
├── Makefile
├── docs/
│   ├── spec.md
│   └── architecture.md
├── service/
│   ├── app/
│   │   ├── main.py            # FastAPI app, mounts routers, nothing else
│   │   ├── config.py           # pydantic Settings, reads .env
│   │   ├── schemas/             # Pydantic request/response — mirrors spec.md
│   │   ├── capabilities/         # ONE FILE PER CAPABILITY — business logic
│   │   ├── routers/               # thin HTTP layer only
│   │   └── data/                   # in-memory fixtures for now (DB comes later)
│   ├── tests/                       # one test file per capability
│   ├── requirements.txt
│   └── .env.example
├── storefront/                        # human-facing UI — the control group (later)
├── agent/                              # LLM tool-calling client + browser agent (later)
└── scripts/                             # seed/dev scripts (later)
```

## The capability pattern

Every capability file:
- Takes a Pydantic input schema, returns a Pydantic output schema
- Has a docstring stating its category (READ/WRITE/FINANCIAL/DESTRUCTIVE) and
  pointing back to the relevant `docs/spec.md` section
- Contains NO FastAPI code — routers translate HTTP ↔ capability
- Contains NO auth/policy logic — that arrives with the policy engine (not built yet)

Filters are applied as a flat sequence of list comprehensions, one per optional
constraint. Adding a constraint means adding one more comprehension — not a query
builder, not a filter registry.

## Router pattern
Routers stay under ~15 lines: parse input, call the capability, return the result.

## Testing convention
`tests/test_<capability_name>.py` mirrors `capabilities/<capability_name>.py`.
Run everything with `make test` — this is the self-check loop for agent-driven changes.

## Naming conventions (keep rigid)
| Thing | Convention |
|---|---|
| Capability function | `snake_case`, matches capability name |
| Capability file | `<capability_name>.py` |
| Test file | `test_<capability_name>.py` |
| Input schema | `<CapabilityName>Input` |
| Output schema | `<CapabilityName>Output` |
| Route path | `/<capability_name>` |

## What NOT to add yet
No service-layer abstraction, no DI framework, no plugin system, no multi-tenant
capability registration. Speculative abstraction is the #1 way agent-driven
codebases rot.

## Build order (what's left, in order)
1. ~~`search_items` (READ, same pattern as `search_restaurants`)~~ ✅ done
2. Agent identity model + `X-Agent-Key` auth middleware (in-memory agents, no DB yet)
3. Policy engine (category rules + spending limit)
4. `create_order` (FINANCIAL — first capability needing persistence, add SQLAlchemy + a DB here)
5. `track_order`, `cancel_order`
6. Action logging (`action_logs` table + `GET /logs`)
7. `storefront/` — minimal human UI over the same DB (the control group)
8. `agent/run_agent.py` — LLM tool-calling client against the capability layer
9. `agent/browser_agent.py` — LLM + Playwright driving the storefront
10. `agent/benchmark.py` — run both over N trials, collect the section-8 metrics

Steps 1-6 are the agent-native service. Steps 7-10 are the experiment that proves
it was worth building.
