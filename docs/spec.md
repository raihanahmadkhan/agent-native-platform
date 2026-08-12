# FoodHub — Agent-Native Service Spec (v0.1)

## 1. What this is

A fictional food-delivery service ("FoodHub") exposed as a set of machine-readable
capabilities that an AI agent can discover and call, instead of clicking through a
website. This is the first vertical slice — one service, a handful of capabilities,
identity + policy + logging wired end to end.

The project deliberately builds the SAME service twice:
1. **Agent-native layer** — capabilities, discovery, identity, policy (this spec)
2. **Human storefront** — a minimal browser UI over the same database

The storefront exists as the *control group* for the benchmark in section 8. It is
not a product. See `docs/architecture.md` for why.

## 2. The canonical task

Every demo, test, and benchmark run targets this one natural-language request:

> "Get me a large veg pizza under ₹400 from a 4+ rated place that delivers to
> Ranchi in under 40 minutes — pick the most ordered one."

It decomposes into seven constraints: item type, size, dietary flag, price cap,
restaurant rating, location + delivery time, and a popularity ranking.

Why this task: a browser agent must set a location, apply filters one at a time,
open each qualifying restaurant separately, find pizza items, check size variants
and prices, and then compare "most ordered" across restaurants — a signal most
real sites do not expose as a filter at all. The agent-native path answers it in
one `search_items` call because search is **cross-restaurant** by design.

## 3. Capabilities (v0.1 — exactly 5, no more)

| Capability            | Category    | Auth required? | Status        |
|------------------------|-------------|-----------------|----------------|
| `search_restaurants`    | READ        | No              | ✅ implemented |
| `search_items`            | READ        | No              | ✅ implemented |
| `create_order`              | FINANCIAL   | Yes             | ⬜ not built    |
| `track_order`                 | READ        | Yes             | ⬜ not built    |
| `cancel_order`                  | DESTRUCTIVE | Yes             | ⬜ not built    |

Action categories:
- **READ** — always allowed, no side effects
- **WRITE** — changes state, low risk
- **FINANCIAL** — moves money, needs a spending-limit check
- **DESTRUCTIVE** — needs explicit confirmation regardless of limit

Constraint richness lives in capability *parameters*, not in extra capabilities.
Do not add a sixth capability to support a new filter.

## 4. Schemas

### 4.1 `search_restaurants` — ✅ implemented
**Input**
```json
{
  "location": "string, required",
  "cuisine": "string, optional",
  "max_delivery_time_minutes": "integer, optional",
  "min_rating": "number, optional",
  "veg_only": "boolean, optional",
  "max_cost_for_two": "integer, optional",
  "max_distance_km": "number, optional",
  "open_now": "boolean, optional",
  "has_offers": "boolean, optional",
  "sort_by": "string, optional — rating | delivery_time | cost | popularity"
}
```
**Output**
```json
{
  "restaurants": [
    {
      "id": "string", "name": "string", "cuisine": "string",
      "rating": "number", "eta_minutes": "integer",
      "cost_for_two": "integer", "distance_km": "number",
      "is_open": "boolean", "offer_text": "string|null",
      "total_orders": "integer", "veg_only": "boolean"
    }
  ]
}
```

### 4.2 `search_items` — ✅ implemented
`restaurant_id` is **optional**. When omitted, the search runs across every
restaurant matching the location/rating/delivery constraints. This is the single
biggest structural advantage over the browser path — do not remove it.

Each size variant is its own item row (no nested variant objects).

**Input**
```json
{
  "restaurant_id": "string, optional — omit to search across restaurants",
  "location": "string, optional — scopes a cross-restaurant search",
  "query": "string, optional — substring match on item name",
  "category": "string, optional — pizza | curry | noodles | dessert | drink | starter",
  "veg_only": "boolean, optional",
  "size": "string, optional — regular | medium | large",
  "max_price": "number, optional",
  "max_spice_level": "integer, optional — 0..3",
  "dietary_tags": "list of string, optional — jain | egg_free | gluten_free",
  "available_now": "boolean, optional",
  "min_restaurant_rating": "number, optional",
  "max_delivery_time_minutes": "integer, optional",
  "sort_by": "string, optional — popularity | price_asc | price_desc | rating",
  "limit": "integer, optional"
}
```
**Output**
```json
{
  "items": [
    {
      "id": "string", "name": "string", "price": "number", "veg": "boolean",
      "size": "string", "category": "string", "spice_level": "integer",
      "dietary_tags": ["string"], "total_orders": "integer", "in_stock": "boolean",
      "restaurant_id": "string", "restaurant_name": "string",
      "restaurant_rating": "number", "eta_minutes": "integer"
    }
  ]
}
```

### 4.3 `create_order` — not built yet
**Input**
```json
{
  "restaurant_id": "string, required",
  "items": [ { "item_id": "string", "quantity": "integer" } ],
  "delivery_address": "string, required"
}
```
**Output**
```json
{ "order_id": "string", "status": "string", "total_amount": "number", "eta_minutes": "integer" }
```
Policy note: if `total_amount` exceeds the agent's spending limit, return
`requires_approval` instead of executing.

### 4.4 `track_order` — not built yet
**Input** `{ "order_id": "string, required" }`
**Output** `{ "order_id": "string", "status": "string", "eta_minutes": "integer" }`

### 4.5 `cancel_order` — not built yet
**Input** `{ "order_id": "string, required", "reason": "string, optional" }`
**Output** `{ "order_id": "string", "status": "string" }`
Policy note: always return `requires_approval` on the first call (DESTRUCTIVE rule).

## 5. Agent identity (not built yet — needed before `create_order`)

```json
{
  "agent_id": "string",
  "api_key": "string",
  "scopes": ["search_restaurants", "search_items", "create_order", "track_order", "cancel_order"],
  "spending_limit": 500
}
```
Auth = `X-Agent-Key` header, checked by middleware, no OAuth in v0.1.

## 6. Policy engine rules (not built yet — needed before `create_order`)

```
READ        → always allowed if scope present
WRITE       → allowed if scope present
FINANCIAL   → allowed if scope present AND amount <= spending_limit, else requires_approval
DESTRUCTIVE → always requires_approval on first call
```

## 7. Explicitly out of scope for v0.1
Multi-service onboarding, full OAuth, real payments, an observability dashboard UI,
caching, rate limiting, horizontal scaling, GEO/discovery ranking.

The manifest format is service-agnostic by design — onboarding a second service
would mean writing capability files, not changing the platform. That claim is a
design property, not a feature to build here.

## 8. The benchmark (the project's headline result)

Both paths execute the section-2 task against the **same database**.

| Path | How it runs |
|---|---|
| Agent-native | LLM tool-calling against `/manifest` + capabilities |
| Human/browser (control) | LLM browser agent driving the storefront via Playwright |

Metrics collected per trial, over N trials:
- steps / tool calls to completion
- wall-clock latency
- tokens consumed and cost
- **success rate** — did it return the correct item?
- recovery events (retries, wrong turns, ambiguity)

Correctness is checkable because the task has exactly one right answer in the
seed data (see `service/app/data/seed_items.py`). The seed data is deliberately
built so that naive shortcuts fail: the cheapest matching pizza, the
highest-rated restaurant's pizza, and the globally most-ordered pizza are all
DIFFERENT items, and the globally most-ordered one is disqualified by the
delivery-time constraint.

## 9. Success criteria for v0.1
1. `GET /manifest` returns implemented capabilities with schemas
2. All 5 capabilities work via curl/Postman with a valid agent key
3. Policy engine correctly blocks/approves based on category + limit
4. Every call is logged (agent_id, action, args, result, latency)
5. An LLM completes the section-2 task end to end through tool calling
6. A measured benchmark: agent-native vs. real browser agent on the same task
