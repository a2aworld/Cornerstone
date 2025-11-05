# A2A-World Makefile
# Simple commands for managing the development environment

.PHONY: help build up down logs restart test clean ps status

help: ## Show this help message
	@echo "A2A-World Development Commands"
	@echo "=============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build all Docker containers
	@echo "🔨 Building A2A-World containers..."
	docker-compose build

up: ## Start all services
	@echo "🚀 Starting A2A-World ecosystem..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "   A2A Server: http://localhost:8000"
	@echo "   Visual Cortex: http://localhost:8001"
	@echo "   A2A Server Docs: http://localhost:8000/docs"
	@echo "   Visual Cortex Docs: http://localhost:8001/docs"

down: ## Stop all services
	@echo "🛑 Stopping A2A-World ecosystem..."
	docker-compose down
	@echo "✅ Services stopped"

logs: ## View logs from all services
	docker-compose logs -f

logs-server: ## View A2A Server logs
	docker-compose logs -f a2a-server

logs-cortex: ## View Visual Cortex logs
	docker-compose logs -f visual-cortex-api

restart: ## Restart all services
	@echo "🔄 Restarting A2A-World..."
	docker-compose restart
	@echo "✅ Services restarted"

ps: ## Show running containers
	docker-compose ps

status: ## Show service status with health checks
	@echo "A2A-World Service Status:"
	@echo "========================"
	@docker-compose ps
	@echo ""
	@echo "Health Checks:"
	@curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "❌ A2A Server not responding"
	@curl -s http://localhost:8001/health | python -m json.tool 2>/dev/null || echo "❌ Visual Cortex not responding"

test: ## Run tests (placeholder for actual test suite)
	@echo "🧪 Running tests..."
	@echo "Note: Full test suite will be implemented in Sprint 1"
	docker-compose exec a2a-server pytest tests/ || echo "Test framework not yet set up"

clean: ## Remove all containers, volumes, and networks
	@echo "🧹 Cleaning up A2A-World environment..."
	docker-compose down -v
	@echo "✅ Cleanup complete"

init: build up ## Initialize the entire environment (build + start)
	@echo "🌍 A2A-World initialized!"
	@echo "Tagline: 'Yesterday's myths. Tomorrow's AI. Verified by Earth.'"

shell-server: ## Open shell in A2A Server container
	docker-compose exec a2a-server /bin/bash

shell-cortex: ## Open shell in Visual Cortex container
	docker-compose exec visual-cortex-api /bin/bash

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U a2a -d a2a_world

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "⚠️  This will destroy all data. Are you sure? [y/N]"
	@read confirm && [ "$$confirm" = "y" ] && docker-compose down -v && docker-compose up -d postgres || echo "Cancelled"

# Development helpers
dev-setup: ## Set up development environment
	@echo "Setting up development environment..."
	cp .env.example .env || echo ".env.example not found"
	@echo "✅ Run 'make init' to start the services"

watch-logs: logs ## Alias for logs (watch in real-time)

check-health: status ## Alias for status
