# Trading Stack
Production-minded systematic trading control stack for retail automation.
## Overview
This is a high-discipline trading operations backend that separates scanning, proposals, approval, execution, and risk controls. Built for a two-phase workflow:
**Phase 1 — Manual Assisted**
- Python scans markets and creates setup signals
- Dashboard shows qualified setups
- Human manually executes trades in MT5
- Human journals whether they took the setup
- System logs signal quality and manual outcomes
**Phase 2 — Semi-Automated**
- Python converts qualified signals into trade proposals
- Human approves or rejects proposals in the dashboard
- Approved proposals are sent to executor service
- Full audit trail maintained
- Execution architecture ready for integration
## Stack
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Runtime**: Uvicorn
- **Containerization**: Docker + docker-compose
- **Testing**: pytest
## Architecture
trading-stack/ ├── app/ │ ├── api/ # FastAPI routes │ ├── core/ #
Config, DB, logging, security │ ├── db/ # Models and session management
│ ├── schemas/ # Pydantic request/response schemas │ ├── services/ #
Business logic layer │ ├── workers/ # Background task workers │ └──
main.py # FastAPI application ├── alembic/ # Database migrations ├──
scripts/ # Utility scripts ├── tests/ # Test suite └──
docker-compose.yml # Local development environment
## Local Setup
### Prerequisites
- Python 3.11+
- PostgreSQL 16+ (or use Docker)
### Quick Start with Docker
```bash
# Clone and navigate
cd trading-stack
# Copy environment file
cp .env.example .env
# Start services
docker-compose up -d
# Run migrations
docker-compose exec api alembic upgrade head
# Seed core data
docker-compose exec api python scripts/seed_core_data.py
# Check health
curl http://localhost:8000/health
Local Development Setup
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
# Install dependencies
pip install -e ".[dev]"
# Configure database
createdb trading_stack
cp .env.example .env
# Edit .env with your database URL
# Run migrations
alembic upgrade head
# Seed data
python scripts/seed_core_data.py
# Start API server
uvicorn app.main:app --reload
# Run tests
pytest
Database Management
Create Migration
alembic revision --autogenerate -m "description"
Apply Migrations
alembic upgrade head
Rollback
alembic downgrade -1
Running Workers
Workers are standalone Python scripts that can be run as background
processes or cron jobs.
Scanner Worker
python -m app.workers.scanner_worker
Scans markets and creates signals based on configured strategies.
Heartbeat Worker
python -m app.workers.heartbeat_worker
Sends service health heartbeats.
API Endpoints
Health

-   GET /health - API health check
    Heartbeats

-   GET /heartbeats - List service heartbeats

-   POST /heartbeats - Create heartbeat
    Signals

-   POST /signals - Create new signal

-   GET /signals - List signals

-   GET /signals/{signal_id} - Get signal detail
    Journal

-   POST /journal - Create manual trade journal entry
    Proposals

-   POST /proposals - Create trade proposal

-   GET /proposals - List proposals

-   POST /proposals/{proposal_id}/review - Approve/reject proposal
    System Workflow
    Phase 1: Manual Trading

1.  Scanner worker runs and generates signals

2.  Signals appear in dashboard (frontend, not included)

3.  Human reviews and manually executes in MT5

4.  Human logs outcome via journal endpoint

5.  System tracks signal→outcome correlation
    Phase 2: Semi-Automated

1.  Scanner generates signals

2.  Proposal engine converts signals to proposals

3.  Proposals appear in dashboard for review

4.  Human approves/rejects

5.  Approved proposals queued for executor service

6.  Full audit trail maintained
    MT5 Integration
    Current Status: Intentionally stubbed
    The mt5_client.py service contains placeholder methods for future
    integration:

-   connect() - Establish MT5 connection

-   fetch_bars() - Get historical price data

-   send_order() - Execute trade order

-   get_positions() - Query open positions
    Integration Path:

1.  MT5 execution will run on a separate Windows VPS

2.  Communication via REST API or RPC mechanism

3.  This backend will send execution commands

4.  MT5 service will report back order status
    Next Implementation Steps

1.  Frontend Dashboard: Build React/Next.js dashboard to consume API

2.  MT5 Bridge Service: Create Windows service to wrap MT5 terminal

3.  Risk Engine: Implement pre-trade risk checks (position sizing,
    exposure limits)

4.  Execution Service: Build automated executor for approved proposals

5.  Real-time Data: Integrate price feed for signal generation

## Running an On-Demand SPY Scan

`scan_spy()` in `app/services/scanner.py` is a real opening-range-breakout
scanner (not a stub): it pulls M5 bars for SPY from an MT5 bridge over
HTTP and looks for a breakout of the first 30 minutes' range.

It needs a bridge process reachable over the network — `MT5Client` never
talks to MetaTrader directly, it only calls a small HTTP service that
wraps the MT5 terminal. That bridge process is **not included in this
repo**; it has to run wherever the MT5 terminal lives (e.g. your Mac/VPS)
and implement this contract:

```
POST /connect                    {login, password, server} -> {"connected": bool}
POST /disconnect                 {}                         -> {"disconnected": bool}
GET  /bars?symbol&timeframe&start&count
                                                              -> [{"time","open","high","low","close","volume"}, ...]
POST /orders                     {symbol, order_type, volume, price,
                                   stop_loss, take_profit, comment}
                                                              -> {"ticket": int, "status": str, ...}
GET  /positions?symbol                                       -> [{"ticket", "symbol", ...}, ...]
GET  /account                                                -> {"balance", "equity", "margin", ...}
POST /positions/{ticket}/modify  {stop_loss, take_profit}    -> {"success": bool}
POST /positions/{ticket}/close   {}                          -> {"success": bool}
```

Once that bridge is running and reachable, point this app at it and seed
SPY's symbol/strategy rows:

```bash
# .env
MT5_HOST=<bridge host, e.g. localhost or your Mac's LAN IP>
MT5_PORT=<bridge port>

python scripts/seed_core_data.py     # creates the SPY symbol + SPY_ORB strategy once
python -m app.workers.scanner_worker --symbol SPY
```

If the bridge is unreachable, the scan logs the error and skips instead
of crashing the whole worker run. If no breakout is found, no signal is
created.

    Production Deployment
    Environment Variables
    Ensure these are set in production:

-   DATABASE_URL - PostgreSQL connection string

-   SECRET_KEY - Secure random string for session/JWT

-   ENVIRONMENT=production
    Database Backups
    Set up automated PostgreSQL backups via pg_dump or managed backup
    service.
    Monitoring
    Add:

-   Sentry or similar for error tracking

-   Prometheus + Grafana for metrics

-   Database query performance monitoring
    Testing
    # Run all tests
    pytest
    # Run with coverage
    pytest --cov=app tests/
    # Run specific test file
    pytest tests/test_signals.py
    Contributing
    This is an internal trading operations system. Maintain:

-   Clean commit messages

-   Test coverage for new features

-   Migration files for schema changes

-   Documentation for new endpoints
    License
    Internal use only.
    ---
    ##
