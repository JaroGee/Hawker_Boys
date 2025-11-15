	PYTHON ?= python3
	PIP ?= pip3
	POETRY ?= poetry
	NPM ?= npm

.PHONY: dev backend frontend worker test lint format migrate preflight seed

venv:
	[ -d .venv ] || $(PYTHON) -m venv .venv

install-backend: venv
	. .venv/bin/activate && pip install -e backend/.[dev]

install-frontend:
	cd frontend && $(NPM) install

backend:
	. .venv/bin/activate && uvicorn tms.main:app --app-dir backend --host 0.0.0.0 --port 8000

frontend:
	cd frontend && $(NPM) run dev

worker:
	. .venv/bin/activate && rq worker ssg_sync

dev: install-backend install-frontend
	$(MAKE) -j3 backend frontend worker

migrate: install-backend
	. .venv/bin/activate && cd backend && alembic upgrade head

lint: install-backend install-frontend
	. .venv/bin/activate && ruff check backend/tms
	cd frontend && $(NPM) run lint

format: install-backend install-frontend
	. .venv/bin/activate && ruff check backend/tms --fix
	. .venv/bin/activate && black backend/tms
	cd frontend && $(NPM) run lint -- --fix

seed: install-backend
	. .venv/bin/activate && python backend/tms/scripts/seed.py

test: install-backend install-frontend
	. .venv/bin/activate && pytest backend/tests
	cd frontend && $(NPM) run lint

preflight: install-backend
	. .venv/bin/activate && python backend/tms/scripts/preflight.py
