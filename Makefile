.PHONY: help install dev test lint format clean docker-up docker-down migrate seed
help:
    @echo "Trading Stack - Available Commands"
    @echo ""
    @echo "  install      Install dependencies"
    @echo "  dev          Run development server"
    @echo "  test         Run tests"
    @echo "  lint         Run linter"
    @echo "  format       Format code"
    @echo "  clean        Clean cache files"
    @echo "  docker-up    Start Docker services"
    @echo "  docker-down  Stop Docker services"
    @echo "  migrate      Run database migrations"
    @echo "  seed         Seed core data"
install:
    pip install -e ".[dev]"
dev:
    uvicorn app.main:app --reload
test:
    pytest
lint:
    ruff check app/ tests/
format:
    black app/ tests/
    ruff check --fix app/ tests/
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +
docker-up:
    docker-compose up -d
docker-down:
    docker-compose down
migrate:
    alembic upgrade head
seed:
    python scripts/seed_core_data.py
