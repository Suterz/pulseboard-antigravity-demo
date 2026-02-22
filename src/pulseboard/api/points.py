from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from pulseboard.database import get_db_connection

router = APIRouter(tags=["points"])


class MetricPointCreate(BaseModel):
    label: str
    value: int


class MetricPointRead(MetricPointCreate):
    id: int


@router.post("/points", response_model=MetricPointRead, status_code=201)
async def create_point(item: MetricPointCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metric_points (label, value) VALUES (?, ?)",
        (item.label, item.value),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"id": new_id, "label": item.label, "value": item.value}


@router.get("/points", response_model=List[MetricPointRead])
async def list_points(limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, label, value FROM metric_points ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [{"id": r["id"], "label": r["label"], "value": r["value"]} for r in rows]


@router.delete("/points/{point_id}", status_code=204)
async def delete_point(point_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM metric_points WHERE id = ?", (point_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Point not found")

    cursor.execute("DELETE FROM metric_points WHERE id = ?", (point_id,))
    conn.commit()
    conn.close()
    return None
