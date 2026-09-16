from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter(prefix="/pricing", tags=["Pricing"])


class PricingRule(BaseModel):
    service: str
    unit: str
    price_per_unit: float


@router.post("/")
def create_pricing_rule(rule: PricingRule):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pricing_rules
                (service, unit, price_per_unit)
                VALUES (%s, %s, %s)
                RETURNING id, service, unit, price_per_unit
                """,
                (
                    rule.service,
                    rule.unit,
                    rule.price_per_unit,
                ),
            )

            row = cursor.fetchone()
            conn.commit()

            return {
                "id": row[0],
                "service": row[1],
                "unit": row[2],
                "price_per_unit": float(row[3]),
            }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        conn.close()


@router.get("/")
def get_pricing_rules():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, service, unit, price_per_unit
                FROM pricing_rules
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "service": row[1],
                    "unit": row[2],
                    "price_per_unit": float(row[3]),
                }
                for row in rows
            ]

    finally:
        conn.close()