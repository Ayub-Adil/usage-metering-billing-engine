from fastapi import FastAPI
from app.usage import router as usage_router
from app.billing import router as billing_router
from app.billing_periods import router as billing_periods_router
from app.invoices import router as invoices_router
from app.pricing import router as pricing_router

app = FastAPI(
    title="Usage Metering & Billing Engine",
    description="FlyRank Backend Track Capstone",
    version="1.0.0"
)

app.include_router(usage_router)
app.include_router(billing_router)
app.include_router(billing_periods_router)
app.include_router(invoices_router)
app.include_router(pricing_router)

@app.get("/")
def root():
    return {
        "message": "Usage Metering & Billing Engine API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }