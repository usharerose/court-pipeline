.PHONY: setup clean test help

# Default target
help:
	@echo "Available commands:"
	@echo "  setup   - Initialize development environment"
	@echo "  test    - Run tests"
	@echo "  lint    - Run linting checks"
	@echo "  clean   - Clean up temporary files"
	@echo "  help    - Show this help message"

# Run tests
test:
	@echo "🧪 Running tests..."
	source .venv/bin/activate || true; \
	python -m pytest -sv --cov-report term-missing --cov-report html:coverage_report --cov-report xml:coverage_report/cov.xml --junitxml=coverage_report/pytest.xml --cov=court_pipeline/ --disable-warnings -p no:cacheprovider tests/*

# Initialize development environment
setup:
	@echo "🚀 Setting up development environment..."
	poetry install
	@echo "📦 Installing pre-commit hooks..."
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg
	@echo "✅ Setup complete! Environment and hooks are ready."

build: clean
	docker compose build court-pipeline-build

run: build clean-container
	docker compose up -d court-pipeline-run

ssh:
	docker compose exec court-pipeline-run /bin/sh

clean-container:
	# stop and remove useless containers
	docker compose down --remove-orphans

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean up complete!"
