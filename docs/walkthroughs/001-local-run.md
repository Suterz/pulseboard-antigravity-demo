# Pulseboard Local Run Walkthrough

This walkthrough outlines how to quickly get started with the Pulseboard dashboard and API locally, verify the UI, and interact with the data operations.

![Pulseboard UI Verification Recording](./verify_pulseboard_ui_1771767768038.webp)

## Prerequisites
- Python 3.10+
- `uv` (Fast Python package and project manager)

## Exact Steps: Running the Application

1. **Clone the repository and install dependencies:**
   The project is managed via `uv`, so installing dependencies will automatically create a virtual environment for you.
   ```bash
   uv sync
   ```

2. **Start the development server:**
   ```bash
   uv run fastapi dev src/pulseboard/main.py
   ```
   *(Alternatively, you can run `uv run uvicorn pulseboard.main:app --reload --app-dir src`)*

## Exact Steps: Using the UI

1. Open your web browser and navigate to `http://127.0.0.1:8000/`.
2. Observe the Pulseboard Dashboard rendering a bar chart with initial seed data (e.g., Jan, Feb, Mar, Apr).
3. Click the **"Add Random Point"** button in the top right corner. The chart will update immediately and display a new random data point.
4. Refresh the page to verify that the newly added data point persists (data is saved to the local SQLite database).

## Expected Results
- The dashboard loads smoothly with a beautiful, modern aesthetic.
- The chart accurately reflects data from `/api/charts/data`.
- Clicking the button successfully issues a `POST /api/points` request to the backend and fetches the updated chart data.
- The `data/pulseboard.db` SQLite file holds state persistently between reloads.

## Quick Troubleshooting

- **Server fails to start?**
  Ensure you have correctly installed dependencies with `uv sync`. Check if port 8000 is already in use (`uv run fastapi dev --port 8001`).
- **Data not updating on the chart?**
  Open the browser Developer Tools (F12) -> Console. Look for any JavaScript errors. Also check the Network tab to ensure `POST /api/points` and `GET /api/charts/data` requests are returning 200/201 status codes.
- **Database errors or weird state?**
  You can safely delete the `data/pulseboard.db` file and restart the server to restore a fresh initial state. To reset entirely, run `rm data/pulseboard.db` from your terminal.

### Running Tests

To ensure the endpoints and the overall flow are functioning correctly without needing a manual UI session, you can run the test suite using `pytest`:

```bash
uv run pytest -v
```
