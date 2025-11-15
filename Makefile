SHELL := /bin/zsh

.PHONY: preflight node_env node_modules dev test migrate

preflight:
	@echo "Preflight checks..."
	@command -v node >/dev/null || (echo "Node is missing. Run scripts/setup_node_intel.sh" && exit 1)
	@node -v | grep -E "v20\." >/dev/null || (echo "Node 20 required. Current: $$(node -v)" && exit 1)

node_env:
	@./scripts/setup_node_intel.sh

node_modules: preflight
	@if [ -f frontend/package.json ]; then cd frontend && npm install; \
	else if [ -f package.json ]; then npm install; else echo "No package.json found"; fi; fi

dev: preflight
	@if [ -f frontend/package.json ]; then echo "Start your frontend dev server here, for example: cd frontend && npm run dev"; else echo "No frontend detected"; fi

test:
	@echo "Add frontend and backend test runners here"
	@echo "For example: cd frontend && npm test"

migrate:
	@. .venv/bin/activate && alembic -c backend/alembic.ini upgrade head
