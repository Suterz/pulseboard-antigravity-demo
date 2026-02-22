# Pulseboard Local Run Walkthrough

This walkthrough outlines how to quickly get started with the Pulseboard dashboard and API locally.

## Prerequisites
- Python 3.10+
- `uv` (Fast Python package and project manager)

## Installation

1. **Clone the repository and install dependencies:**
   The project is managed via `uv`, so installing dependencies will automatically create a virtual environment for you.
   ```bash
   uv sync
   ```

## Running the Application

This application serves both a frontend dashboard (via Jinja2 templates) and a RESTful JSON API using FastAPI.

**Start the development server:**
```bash
uv run fastapi dev src/pulseboard/main.py
```
*(Alternatively, you can run `uv run uvicorn pulseboard.main:app --reload --app-dir src`)*

## Usage & Endpoints

- **Dashboard UI:** Navigate to `http://127.0.0.1:8000/`. You'll see the dashboard rendering dynamic charts using Chart.js.
- **Interactive API Docs:** Navigate to `http://127.0.0.1:8000/docs` to test endpoints directly from the browser via Swagger UI.

### Chart Data API

The API supports full CRUD operations on chart data. By default, upon first startup, the application creates a SQLite database located at `data/pulseboard.db` and seeds it with default dummy metrics.

- `GET    /api/charts/data`: Retrieves all chart data formats (labels and values).
- `POST   /api/charts/data`: Create a new chart data entry. Accepts JSON: `{"label": "May", "value": 50}`.
- `PUT    /api/charts/data/{id}`: Update an existing chart entry by ID.
- `DELETE /api/charts/data/{id}`: Delete an entry by ID.

### Running Tests

To ensure the endpoints and the overall flow are functioning correctly, you can run the test suite using `pytest`:

```bash
uv run pytest
```
