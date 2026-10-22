ENGINE ?= podman
PROJECT ?= priority-sale-order

ifeq ($(ENGINE),podman)
COMPOSE ?= podman compose
else ifeq ($(ENGINE),docker)
COMPOSE ?= docker compose
else
$(error ENGINE must be either podman or docker)
endif

.DEFAULT_GOAL := help
.PHONY: help up down restart logs ps shell store-html package-store

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z_-]+:.*## / {printf "%-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start Odoo and PostgreSQL in the background (ENGINE=podman|docker)
	$(COMPOSE) -p $(PROJECT) up -d

down: ## Stop the containers and preserve database data
	$(COMPOSE) -p $(PROJECT) down

restart: ## Restart Odoo and PostgreSQL
	$(COMPOSE) -p $(PROJECT) restart

logs: ## Follow container logs
	$(COMPOSE) -p $(PROJECT) logs -f

ps: ## Show container status
	$(COMPOSE) -p $(PROJECT) ps

shell: ## Open a shell in the Odoo container
	$(COMPOSE) -p $(PROJECT) exec odoo bash

store-html: ## Build localized Odoo Apps description pages
	python3 docs/store/build_html.py --store-listing --output-dir static/description

package-store: store-html ## Build clean ZIP packages for Odoo 17, 18, 19, and 20
	python3 tools/package_store.py
