# mt5TraderJawn

MT5 + VPS + Python trading control stack for Phase 1 manual-assisted signals and Phase 2 semi-auto proposal review.

## Phases

### Phase 1 — Manual Assisted
- Python scans markets and creates setup signals
- API/dashboard shows qualified setups
- You place trades manually in MT5
- You journal whether you took the setup and how it performed

### Phase 2 — Semi-Auto
- Python converts qualified signals into trade proposals
- Human approves or rejects proposals
- Approved proposals are ready for executor consumption
- MT5 execution boundary is stubbed, not implemented

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Docker / docker-compose
- pytest

## Repo layout

```text
app/
  api/routes/         API endpoints
  core/               settings + db wiring
  db/models/          SQLAlchemy models
  schemas/            request/response schemas
  services/           scanner/proposal/heartbeat/MT5 boundary
  workers/            worker entrypoints
scripts/              seed helpers
alembic/              migrations
tests/                starter tests
```

## Local setup

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
python scripts/seed_core_data.py
uvicorn app.main:app --reload
```

## Docker setup

```bash
cp .env.example .env
docker compose up -d
docker compose exec api alembic upgrade head
docker compose exec api python scripts/seed_core_data.py
curl http://localhost:8000/health
```

## Workers

```bash
python -m app.workers.scanner_worker
python -m app.workers.heartbeat_worker
```

## Tests

```bash
pytest
```

## MT5 note
`app/services/mt5_client.py` is intentionally a placeholder interface. Real terminal connection and order execution belong on the Windows MT5 side later.
