# Agent-Native Platform (FoodHub)

An agent-native capability layer: instead of a human clicking through a food
delivery website, an AI agent calls `GET /manifest` to discover what's possible,
then calls capabilities directly (`POST /search_restaurants`, etc.).

See `docs/spec.md` for the full capability contract and `docs/architecture.md`
for how the codebase is organized. If you're an AI coding agent working in this
repo, read `CLAUDE.md` first.

## Quick start

```bash
cd service
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
cp .env.example .env

cd ..
make install
make test      # should pass — 5 tests
make run       # serves on http://localhost:8000
```

Try it:
```bash
curl http://localhost:8000/manifest
curl -X POST http://localhost:8000/search_restaurants \
  -H "Content-Type: application/json" \
  -d '{"location": "ranchi"}'
```

## Status

Only `search_restaurants` is implemented. See `docs/spec.md` section 2 for what's
left and `docs/architecture.md` "Build order" for the sequence.
