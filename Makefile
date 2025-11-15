SHELL := /bin/zsh

PYTHON ?= python3
PIP ?= pip3
NPM ?= npm

.PHONY: preflight node_env venv install-backend install-frontend node_modules backend frontend worker dev migrate lint format seed test

preflight:
	@echo "Preflight checks..."
	@command -v node >/dev/null || (echo "Node is missing. Run scripts/setup_node_intel.sh" && exit 1)
	@node -v | grep -E "v20\." >/dev/null || (echo "Node 20 required. Current: $$(node -v)" && exit 1)
	@[ -d .venv ] || $(MAKE) venv
	@. .venv/bin/activate && python backend/tms/scripts/preflight.py

node_env:
	@./scripts/setup_node_intel.sh

venv:
	[ -d .venv ] || $(PYTHON) -m venv .venv

install-backend: venv
	. .venv/bin/activate && pip install -e backend/.[dev]

install-frontend:
	@if [ -f frontend/package.json ]; then cd frontend && $(NPM) install; \
	elif [ -f package.json ]; then $(NPM) install; else echo "No package.json found"; fi

node_modules: preflight install-frontend

backend: install-backend
	. .venv/bin/activate && uvicorn tms.main:app --app-dir backend --host 0.0.0.0 --port 8000

frontend: install-frontend
	@if [ -f frontend/package.json ]; then cd frontend && $(NPM) run dev; else echo "No frontend detected"; fi

worker: install-backend
	. .venv/bin/activate && rq worker ssg_sync

dev: install-backend install-frontend
	@echo "Backend: . .venv/bin/activate && uvicorn tms.main:app --app-dir backend --host 0.0.0.0 --port 8000"
	@if [ -f frontend/package.json ]; then echo "Frontend: cd frontend && $(NPM) run dev"; else echo "No frontend detected"; fi

migrate: install-backend
	. .venv/bin/activate && cd backend && alembic upgrade head

lint: install-backend
	. .venv/bin/activate && ruff check backend/tms
	@if [ -f frontend/package.json ]; then cd frontend && $(NPM) run lint; fi

format: install-backend
	. .venv/bin/activate && ruff check backend/tms --fix
	. .venv/bin/activate && black backend/tms
	@if [ -f frontend/package.json ]; then cd frontend && $(NPM) run lint -- --fix; fi

seed: install-backend
	. .venv/bin/activate && python backend/tms/scripts/seed.py

test: install-backend
	. .venv/bin/activate && pytest backend/tests
	@if [ -f frontend/package.json ]; then cd frontend && $(NPM) test || true; fi
