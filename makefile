# Makefile for FastAPI project with Docker & uv

# Default Docker Compose file path
DOCKER_COMPOSE_FILE=docker/docker-compose.yml
DOCKER_CONTAINER_NAME=fast-clean-api

# Default source folder for uv
SRC_DIR=src

# --- Targets ---

.PHONY: lock
# Generate or update uv.lock from pyproject.toml in the source folder
lock:
	@echo "Generating uv.lock in $(SRC_DIR)/..."
	uv lock --directory $(SRC_DIR)

.PHONY: up
# Run Docker Compose (start services in foreground)
up:
	@echo "Starting Docker Compose..."
	docker compose -f $(DOCKER_COMPOSE_FILE) up

.PHONY: upd
# Run Docker Compose in detached mode
upd:
	@echo "Starting Docker Compose in detached mode..."
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

.PHONY: build
# Build Docker images using Docker Compose
build:
	@echo "Building Docker Compose images..."
	docker compose -f $(DOCKER_COMPOSE_FILE) build

.PHONY: down
# Stop Docker Compose services
down:
	@echo "Stopping Docker Compose..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: restart
# Rebuild and restart services
restart: build down up-d
	@echo "Services rebuilt and restarted."

.PHONY: bash
# Moving inside the container
bash:
	@echo "Moving inside the container"
	docker exec -it $(DOCKER_CONTAINER_NAME) bash

.PHONY: ruff
# Run flake
ruff:
	docker exec $(DOCKER_CONTAINER_NAME) bash -c "ruff check . --fix && ruff format"
	@echo "Ruff executed."

.PHONY: ruff
# Run mypy
mypy:
	docker exec $(DOCKER_CONTAINER_NAME) mypy . --explicit-package-bases
	@echo "MyPY executed."

.PHONY: isort
# Run isort
isort:
	docker exec $(DOCKER_CONTAINER_NAME) isort .

.PHONY: isort
# Run isort
format:
	make isort
	make ruff

.PHONY: pre-commit
# Run pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: alembic-db-upgrade
# Run pre-commit
alembic-db-upgrade:
	docker exec $(DOCKER_CONTAINER_NAME) alembic upgrade head

.PHONY: alembic-revision
# Run pre-commit
alembic-revision:
	docker exec $(DOCKER_CONTAINER_NAME) alembic revision --autogenerate -m "New tables"

.PHONY: claude
# Run claude
claude:
	docker exec -it $(DOCKER_CONTAINER_NAME) /home/web-user/.local/bin/claude
