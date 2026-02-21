# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-21

### Added
- Initial project scaffolding using `uv` for dependency management
- FastAPI backend integrated with SQLite database for data serving
- Unified app layout (`src/pulseboard/`) serving Jinja2 templates and static files
- Simple web UI featuring a Chart.js visualization of seeded database data
- `ruff` configured for formatting and linting alongside git `pre-commit` hooks
- `pytest` integration and test cases for API and HTML rendering
- GitHub Actions CI pipeline for automated formatting, linting, and testing
- Manual Versioning strategy and CHANGELOG initialized
