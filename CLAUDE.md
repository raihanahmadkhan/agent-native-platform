# Project context for AI coding agents

Read this before making changes. Also read `docs/spec.md` (capability contracts,
including build status per capability) and `docs/architecture.md` (why the repo
is shaped this way).

## What this project is

An agent-native capability layer for a fictional food-delivery service
("FoodHub"). AI agents discover capabilities via `GET /manifest` and call them
via `POST /<capability_name>`. Currently only `search_restaurants` is built —
see `docs/spec.md` section 2 for what's left and `docs/architecture.md` section
"Build order" for the sequence to build it in.

## Commands

```bash
make install   # install dependencies into the venv
make run        # start the FastAPI dev server on :8000
make test        # run the full test suite — run this after every change
```

Do not invent other commands. If something needs a new one, add it to the
Makefile.

## Ground rules

1. **Run `make test` after every change.** Fix failing tests before considering
   a task done.
2. **One capability = one file**, in `service/app/capabilities/`. Copy the shape
   of `search_restaurants.py` — same structure, same docstring convention.
3. **Capabilities never import FastAPI, HTTPException, or Request.** Raise a
   plain Python exception; the router translates it to an HTTP response.
4. **Capabilities never check auth or policy.** That logic doesn't exist yet
   (see build order step 2-3) — when you add it, put it in `auth/` and `policy/`,
   never inline inside a capability.
5. **Schemas in `service/app/schemas/` must match `docs/spec.md` field-for-field.**
   Update both in the same change.
6. **Don't add new abstractions** (service layers, generic handler base classes,
   plugin systems) without being asked.
7. **Keep routers under ~15 lines.**
8. **New capability checklist** — do these in order:
   - Update the status table + schema in `docs/spec.md` (flip ⬜ → ✅ when done)
   - Add `schemas/<name>.py` (Input/Output)
   - Add `capabilities/<name>.py`
   - Add the route in the relevant `routers/*.py`
   - Add `tests/test_<name>.py`
   - Run `make test`

## Follow the build order

Build in the sequence listed in `docs/architecture.md` under "Build order."
Don't jump to `create_order` before identity + policy exist — `create_order` is
FINANCIAL and needs the policy engine to enforce spending limits correctly.

## Things deliberately NOT implemented yet (don't build silently)
Real payments, full OAuth, multi-tenant capability registration, an observability
dashboard UI, caching, rate limiting, horizontal scaling. If a task seems to need
one of these, flag it instead of building it.

## Scope decisions already settled (don't relitigate)

1. **This is ONE service, not a platform other developers plug into.** The
   manifest format happens to be service-agnostic, and that's a fine thing to
   claim in the README — but multi-tenant registration is explicitly out of
   scope. Do not build a generic capability-registration SDK.
2. **The `storefront/` IS in scope** (build order step 7). It is a human-facing
   browser UI and the control group for the benchmark — it is NOT the
   "dashboard UI" ruled out above (that means an agent-metrics dashboard).
   Keep it minimal and ugly on purpose.
3. **Added complexity goes into capability parameters, not new capabilities.**
   The 5-capability limit in `docs/spec.md` is firm. A new filter is a new
   optional field on an existing input schema.

## When unsure
Prefer a `# TODO:` comment or a direct question over guessing at scope.
