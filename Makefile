.PHONY: dev backend frontend worker migrate test lint format seed preflight

PYTHON ?= python3
PIP ?= pip

venv:
[ -d .venv ] || $(PYTHON) -m venv .venv
. .venv/bin/activate && $(PIP) install --upgrade pip
. .venv/bin/activate && pip install -e backend/[dev]

node_modules:
cd frontend && [ -f package-lock.json ] && npm ci || npm install

preflight:
. .venv/bin/activate && python backend/scripts/preflight.py

backend:
. .venv/bin/activate && uvicorn tms.api:app --reload --app-dir backend

frontend:
cd frontend && npm run dev

worker:
. .venv/bin/activate && rq worker ssg-sync

dev: venv node_modules
tmux new-session \;
send-keys 'make backend' C-m \;
split-window -h \;
send-keys 'make frontend' C-m \;
split-window -v \;
send-keys 'make worker' C-m

migrate:
. .venv/bin/activate && alembic -c backend/alembic.ini upgrade head

test:
. .venv/bin/activate && pytest

lint:
. .venv/bin/activate && ruff check backend

format:
. .venv/bin/activate && black backend

seed:
. .venv/bin/activate && python backend/scripts/seed_data.py
