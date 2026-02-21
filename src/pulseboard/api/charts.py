from fastapi import APIRouter
from pulseboard.database import get_db_connection

router = APIRouter(tags=["charts"])


@router.get("/charts/data")
async def get_chart_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT label, value FROM chart_data ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    return {
        "labels": [row["label"] for row in rows],
        "values": [row["value"] for row in rows],
    }
