from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter(prefix="/billing-periods", tags=["Billing Periods"])


class BillingPeriod(BaseModel):
    customer_id: str
    period_start: str
    period_end: str


@router.post("/")
def create_billing_period(period: BillingPeriod):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO billing_periods
                (customer_id, period_start, period_end)
                VALUES (%s, %s, %s)
                RETURNING id, customer_id, period_start,
                          period_end, status, created_at
                """,
                (
                    period.customer_id,
                    period.period_start,
                    period.period_end,
                ),
            )

            row = cursor.fetchone()
            conn.commit()

            return {
                "id": row[0],
                "customer_id": row[1],
                "period_start": row[2],
                "period_end": row[3],
                "status": row[4],
                "created_at": row[5],
            }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        conn.close()


@router.get("/{customer_id}")
def get_billing_periods(customer_id: str):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, customer_id, period_start,
                       period_end, status, created_at
                FROM billing_periods
                WHERE customer_id = %s
                ORDER BY period_start DESC
                """,
                (customer_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "customer_id": row[1],
                    "period_start": row[2],
                    "period_end": row[3],
                    "status": row[4],
                    "created_at": row[5],
                }
                for row in rows
            ]

    finally:
        conn.close()