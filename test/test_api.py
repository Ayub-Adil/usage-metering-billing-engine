from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Usage Metering & Billing Engine API"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_pricing_rules():
    response = client.get("/pricing/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_invalid_usage_quantity():
    response = client.post(
        "/usage/",
        json={
            "customer_id": "customer-001",
            "service": "api",
            "quantity": -100,
            "unit": "requests",
            "event_timestamp": "2026-11-20 12:00:00"
        }
    )

    assert response.status_code == 422

def test_billing_calculation():
    response = client.get(
        "/billing/customer-001",
        params={
            "period_start": "2026-11-01",
            "period_end": "2026-11-30"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_id"] == "customer-001"
    assert data["total_amount"] == 55
    assert data["currency"] == "INR"

def test_get_invoices():
    response = client.get("/invoices/customer-001")

    assert response.status_code == 200

    invoices = response.json()

    assert len(invoices) >= 3

    november_invoice = next(
        invoice
        for invoice in invoices
        if invoice["billing_period_id"] == 3
    )

    assert november_invoice["invoice_number"] == "INV-CUSTOMER-001-0003"
    assert november_invoice["total_amount"] == 55
    assert november_invoice["currency"] == "INR"