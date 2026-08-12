# FoodHub — Agent-Native Service Spec (v0.1)

## 1. What this is

A fictional food-delivery service ("FoodHub") exposed as a set of machine-readable
capabilities that an AI agent can discover and call, instead of clicking through a
website. This is the first vertical slice — one service, a handful of capabilities,
identity + policy + logging wired end to end.

## 2. Capabilities (v0.1 — exactly 5, no more)

| Capability            | Category    | Auth required? | Status        |
|------------------------|-------------|-----------------|----------------|
| `search_restaurants`    | READ        | No              | ✅ implemented |
| `search_items`            | READ        | No              | ⬜ not built    |
| `create_order`              | FINANCIAL   | Yes             | ⬜ not built    |
| `track_order`                 | READ        | Yes             | ⬜ not built    |
| `cancel_order`                  | DESTRUCTIVE | Yes             | ⬜ not built    |

Action categories:
- **READ** — always allowed, no side effects
- **WRITE** — changes state, low risk
- **FINANCIAL** — moves money, needs a spending-limit check
- **DESTRUCTIVE** — needs explicit confirmation regardless of limit

## 3. Schemas

### 3.1 `search_restaurants` — ✅ implemented
**Input**
```json
{
  "location": "string, required",
  "cuisine": "string, optional",
  "max_delivery_time_minutes": "integer, optional",
  "min_rating": "number, optional"
}
```
**Output**
```json
{
  "restaurants": [
    { "id": "string", "name": "string", "cuisine": "string", "rating": "number", "eta_minutes": "integer" }
  ]
}
```

### 3.2 `search_items` — not built yet
**Input**
```json
{ "restaurant_id": "string, required", "query": "string, optional" }
```
**Output**
```json
{ "items": [ { "id": "string", "name": "string", "price": "number", "veg": "boolean" } ] }
```

### 3.3 `create_order` — not built yet
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

### 3.4 `track_order` — not built yet
**Input** `{ "order_id": "string, required" }`
**Output** `{ "order_id": "string", "status": "string", "eta_minutes": "integer" }`

### 3.5 `cancel_order` — not built yet
**Input** `{ "order_id": "string, required", "reason": "string, optional" }`
**Output** `{ "order_id": "string", "status": "string" }`
Policy note: always return `requires_approval` on the first call (DESTRUCTIVE rule).

## 4. Agent identity (not built yet — needed before `create_order`)

```json
{
  "agent_id": "string",
  "api_key": "string",
  "scopes": ["search_restaurants", "search_items", "create_order", "track_order", "cancel_order"],
  "spending_limit": 500
}
```
Auth = `X-Agent-Key` header, checked by middleware, no OAuth in v0.1.

## 5. Policy engine rules (not built yet — needed before `create_order`)

```
READ        → always allowed if scope present
WRITE       → allowed if scope present
FINANCIAL   → allowed if scope present AND amount <= spending_limit, else requires_approval
DESTRUCTIVE → always requires_approval on first call
```

## 6. Explicitly out of scope for v0.1
Multi-service onboarding, full OAuth, real payments, dashboard UI, caching,
rate limiting, horizontal scaling, GEO/discovery ranking.

## 7. Success criteria for v0.1
1. `GET /manifest` returns implemented capabilities with schemas
2. All 5 capabilities work via curl/Postman with a valid agent key
3. Policy engine correctly blocks/approves based on category + limit
4. Every call is logged (agent_id, action, args, result, latency)
5. A script drives an LLM (tool calling) through a natural-language request end to end
6. One benchmark: agent-native step count vs. simulated browser steps
