from fastapi import APIRouter, HTTPException, Query
from app.database import get_connection

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/{customer_id}")
def calculate_bill(
    customer_id: str,
    period_start: str = Query(...),
    period_end: str = Query(...),
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    u.service,
                    u.unit,
                    SUM(u.quantity) AS total_quantity,
                    p.price_per_unit
                FROM usage_events u
                JOIN pricing_rules p
                    ON u.service = p.service
                   AND u.unit = p.unit
                WHERE u.customer_id = %s
                  AND u.event_timestamp >= %s
                  AND u.event_timestamp < (%s::date + INTERVAL '1 day')
                GROUP BY u.service, u.unit, p.price_per_unit
                """,
                (
                    customer_id,
                    period_start,
                    period_end,
                ),
            )

            rows = cursor.fetchall()

            if not rows:
                raise HTTPException(
                    status_code=404,
                    detail="No billable usage found for this billing period",
                )

            items = []
            total_amount = 0

            for row in rows:
                service = row[0]
                unit = row[1]
                quantity = float(row[2])
                price_per_unit = float(row[3])
                amount = quantity * price_per_unit

                items.append(
                    {
                        "service": service,
                        "unit": unit,
                        "quantity": quantity,
                        "price_per_unit": price_per_unit,
                        "amount": round(amount, 2),
                    }
                )

                total_amount += amount

            return {
                "customer_id": customer_id,
                "period_start": period_start,
                "period_end": period_end,
                "items": items,
                "total_amount": round(total_amount, 2),
                "currency": "INR",
            }

    finally:
        conn.close()