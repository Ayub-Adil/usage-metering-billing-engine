import os
import psycopg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://billing_user:billing_password@localhost:5433/usage_billing"
)


def get_connection():
    return psycopg.connect(DATABASE_URL)