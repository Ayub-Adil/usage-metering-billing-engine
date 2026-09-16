from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field ,field_validator
from app.database import get_connection

router = APIRouter(prefix="/usage", tags=["Usage"])


class UsageEvent(BaseModel):
    customer_id: str = Field(min_length=1)
    service: str = Field(min_length=1)
    quantity: float
    unit: str = Field(min_length=1)
    event_timestamp: str | None = None

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value


@router.post("/")
def create_usage(event: UsageEvent):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usage_events
                (customer_id, service, quantity, unit, event_timestamp)
                VALUES (%s, %s, %s, %s, COALESCE(%s::timestamp, CURRENT_TIMESTAMP))
                RETURNING id, customer_id, service, quantity, unit,
                          event_timestamp, created_at
                """,
                (
                    event.customer_id,
                    event.service,
                    event.quantity,
                    event.unit,
                    event.event_timestamp,
                ),
            )

            row = cursor.fetchone()
            conn.commit()

            return {
                "id": row[0],
                "customer_id": row[1],
                "service": row[2],
                "quantity": float(row[3]),
                "unit": row[4],
                "event_timestamp": row[5],
                "created_at": row[6],
            }

    finally:
        conn.close()


@router.get("/")
def get_usage():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, customer_id, service, quantity, unit,
                       event_timestamp, created_at
                FROM usage_events
                ORDER BY event_timestamp DESC
                """
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "customer_id": row[1],
                    "service": row[2],
                    "quantity": float(row[3]),
                    "unit": row[4],
                    "event_timestamp": row[5],
                    "created_at": row[6],
                }
                for row in rows
            ]

    finally:
        conn.close()