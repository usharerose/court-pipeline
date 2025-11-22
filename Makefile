.PHONY: setup clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  setup   - Initialize development environment"
	@echo "  test    - Run tests"
	@echo "  lint    - Run linting checks"
	@echo "  clean   - Clean up temporary files"
	@echo "  help    - Show this help message"

# Initialize development environment
setup:
	@echo "🚀 Setting up development environment..."
	poetry install
	@echo "📦 Installing pre-commit hooks..."
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg
	@echo "✅ Setup complete! Environment and hooks are ready."

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean up complete!"
