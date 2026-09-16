CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id VARCHAR(100) NOT NULL,
    billing_period_id INTEGER NOT NULL REFERENCES billing_periods(id),
    subtotal NUMERIC(12, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    status VARCHAR(20) NOT NULL DEFAULT 'issued',
    issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);