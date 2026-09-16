CREATE TABLE IF NOT EXISTS pricing_rules (
    id SERIAL PRIMARY KEY,
    service VARCHAR(100) NOT NULL UNIQUE,
    unit VARCHAR(50) NOT NULL,
    price_per_unit NUMERIC(12, 4) NOT NULL
);