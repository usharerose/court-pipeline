# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project called `court-pipeline` for historical basketball statistics data pipeline. It uses Poetry for dependency management and is licensed under Apache License 2.0.

## Environment Setup

- Python version: ^3.14
- This project uses Poetry for dependency management
- Virtual environment is configured in-project (`in-project = true` in poetry.toml)
- The project currently only has IPython as a dev dependency

## Project Initialization

### Prerequisites

- Poetry (for dependency management)

### Setup

For new developers who have just cloned the repository:

```bash
# One-command setup (installs dependencies and hooks)
make setup
```

The command will:
1. 📦 **Installs Python dependencies** via `poetry install`
2. 🔗 **Sets up pre-commit hooks** for code quality checks
3. ✅ **Configures commit message validation** via commit-msg hooks
4. 🚀 **Prepares development environment** for immediate use

## Architecture

This is a minimal project structure:
- Basic README.md with project description is now present
- Apache License 2.0 is included
- No source code files exist yet
- No tests, src directory, or other standard Python project structure
- Project appears to be in early setup phase

## Commit Message Convention

Follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification:

### Format
```
<type>(<scope>): <subject>

[body]

[footer]
```

### Required Rules

**Types (must be lowercase):**
- `build` - Build system or dependency changes
- `chore` - Maintenance tasks, no production code changes
- `ci` - CI/CD configuration changes
- `docs` - Documentation changes
- `feat` - New feature (introduces new API or functionality)
- `fix` - Bug fix
- `perf` - Performance improvements
- `refactor` - Code refactoring without changing functionality
- `revert` - Reverts a previous commit
- `style` - Code formatting changes (white-space, formatting, missing semi-colons)
- `test` - Adding missing tests or correcting existing tests

**Scope (optional but recommended):**
- Noun describing the section of codebase affected

**Subject:**
- Cannot be empty
- Must start with lowercase letter
- Cannot end with period
- Maximum 100 characters
- Use imperative mood: "add" not "added" or "adds"
- Concise description of the change

### Optional Rules

**Body:**
- Must have blank line after header
- Each line maximum 100 characters (or 72 for better readability)
- Explain the motivation for the change and contrast with previous behavior
- Provide context about the problem being solved

**Footer:**
- Must have blank line after body
- Each line maximum 100 characters
- **Breaking Changes**: Must start with `BREAKING CHANGE: ` followed by space
- **Issue References**: `Closes #123`, `Fixes #456`, `Resolves #789`

### Examples

```bash
# Simple commits
✅ fix: resolve authentication issue
✅ feat: add user profile module
✅ docs: update installation guide
✅ chore: update dependencies

# Commits with scope
✅ feat(auth): add two-factor authentication
✅ fix(api): handle timeout errors gracefully
✅ test(utils): add unit tests for validation
✅ build: upgrade webpack to v5.0

# Commits with body
✅ fix: resolve memory leak in data processing

The application was experiencing memory leaks when processing large datasets.
This commit fixes the issue by properly disposing of resources and implementing
efficient memory management patterns.

✅ refactor(parser): improve error handling

Simplified the error handling logic by creating dedicated validator classes.
This improves maintainability and makes the code more testable.

# Commits with breaking changes
✅ feat(api): new authentication system

BREAKING CHANGE: Authentication endpoints now require JWT tokens.
Previous session-based authentication has been removed.

✅ feat(database): migrate to new connection pool

BREAKING CHANGE: Database connection configuration has changed.
Update your environment variables accordingly.

# Commits with issue references
✅ fix: handle null values in user data

Closes #42

✅ feat: add email notification system

Fixes #156, Addresses #160

# Invalid examples
❌ Feat: add new feature  # type must be lowercase
❌ fix: Add new feature   # subject must start with lowercase
❌ fix: add new feature. # subject should not end with period
❌ feat:                 # subject cannot be empty
❌ feat:: add feature    # only one colon allowed
❌ feat add feature      # missing colon after type
```

### Key Principles

1. **Be Consistent** - Follow the same pattern across all commits
2. **Be Descriptive but Concise** - Provide enough context in the subject
3. **Use Imperative Mood** - Describe what the commit does, not what you did
4. **Separate Concerns** - One logical change per commit
5. **Document Breaking Changes** - Always use BREAKING CHANGE footer for API changes
```

## Notes for Development

- Since there's no source code yet, any development will likely involve creating the initial project structure
- Consider creating src/, tests/, and other standard directories as needed
- The project description indicates it's for "historical basketball statistics" data pipeline work
- Currently only IPython is available as a dev tool for interactive development

