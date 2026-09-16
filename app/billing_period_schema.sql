CREATE TABLE IF NOT EXISTS billing_periods (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (customer_id, period_start, period_end)
);