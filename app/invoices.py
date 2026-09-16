from fastapi import APIRouter, HTTPException
from app.database import get_connection

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/{customer_id}/{billing_period_id}")
def generate_invoice(customer_id: str, billing_period_id: int):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # Check billing period
            cursor.execute(
                """
                SELECT id, customer_id, period_start, period_end
                FROM billing_periods
                WHERE id = %s
                  AND customer_id = %s
                """,
                (billing_period_id, customer_id),
            )

            period = cursor.fetchone()

            if not period:
                raise HTTPException(
                    status_code=404,
                    detail="Billing period not found"
                )

            # Calculate bill for the billing period
            cursor.execute(
                """
                SELECT
                    SUM(u.quantity * p.price_per_unit) AS total_amount
                FROM usage_events u
                JOIN pricing_rules p
                    ON u.service = p.service
                   AND u.unit = p.unit
                WHERE u.customer_id = %s
                  AND u.event_timestamp >= %s
                  AND u.event_timestamp < (%s::date + INTERVAL '1 day')
                """,
                (
                    customer_id,
                    period[2],
                    period[3],
                ),
            )

            result = cursor.fetchone()
            total_amount = result[0]

            if total_amount is None:
                raise HTTPException(
                    status_code=404,
                    detail="No billable usage found for this billing period"
                )

            # Check if invoice already exists
            cursor.execute(
                """
                SELECT id, invoice_number
                FROM invoices
                WHERE billing_period_id = %s
                """,
                (billing_period_id,),
            )

            existing_invoice = cursor.fetchone()

            if existing_invoice:
                raise HTTPException(
                    status_code=409,
                    detail=f"Invoice already exists: {existing_invoice[1]}"
                )

            # Generate invoice number
            invoice_number = (
                f"INV-{customer_id.upper()}-{billing_period_id:04d}"
            )

            cursor.execute(
                """
                INSERT INTO invoices
                (
                    invoice_number,
                    customer_id,
                    billing_period_id,
                    subtotal,
                    total_amount,
                    currency,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, 'INR', 'issued')
                RETURNING
                    id,
                    invoice_number,
                    customer_id,
                    billing_period_id,
                    subtotal,
                    total_amount,
                    currency,
                    status,
                    issued_at
                """,
                (
                    invoice_number,
                    customer_id,
                    billing_period_id,
                    total_amount,
                    total_amount,
                ),
            )

            invoice = cursor.fetchone()

            # Close the billing period
            cursor.execute(
                """
                UPDATE billing_periods
                SET status = 'closed'
                WHERE id = %s
                """,
                (billing_period_id,),
            )

            conn.commit()

            return {
                "id": invoice[0],
                "invoice_number": invoice[1],
                "customer_id": invoice[2],
                "billing_period_id": invoice[3],
                "subtotal": float(invoice[4]),
                "total_amount": float(invoice[5]),
                "currency": invoice[6],
                "status": invoice[7],
                "issued_at": invoice[8],
            }

    finally:
        conn.close()


@router.get("/{customer_id}")
def get_invoices(customer_id: str):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    invoice_number,
                    customer_id,
                    billing_period_id,
                    subtotal,
                    total_amount,
                    currency,
                    status,
                    issued_at
                FROM invoices
                WHERE customer_id = %s
                ORDER BY issued_at DESC
                """,
                (customer_id,),
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row[0],
                    "invoice_number": row[1],
                    "customer_id": row[2],
                    "billing_period_id": row[3],
                    "subtotal": float(row[4]),
                    "total_amount": float(row[5]),
                    "currency": row[6],
                    "status": row[7],
                    "issued_at": row[8],
                }
                for row in rows
            ]

    finally:
        conn.close()