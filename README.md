Usage Metering \& Billing Engine



A backend capstone project built for the FlyRank Backend AI Engineering track.



The system records customer usage, applies service-specific pricing rules, calculates billing amounts for selected billing periods, manages billing periods, and generates invoices.



Tech Stack



\- Python 3.13

\- FastAPI

\- PostgreSQL 16

\- Psycopg

\- Pydantic

\- Docker

\- Docker Compose

\- Pytest

\- Swagger UI



Features



\- Record customer usage events

\- Validate usage quantities

\- Configure pricing rules

\- Calculate customer bills for a billing period

\- Create and manage billing periods

\- Generate invoices

\- Prevent duplicate invoices

\- Automatically close a billing period after invoice generation

\- PostgreSQL database persistence

\- Dockerized API and database

\- Automated API tests

\- Swagger/OpenAPI documentation



Project Structure



usage-metering-billing-engine/

│

├── app/

│   ├── main.py

│   ├── database.py

│   ├── usage.py

│   ├── pricing.py

│   ├── billing.py

│   ├── billing\_periods.py

│   ├── invoices.py

│   ├── schema.sql

│   ├── pricing\_schema.sql

│   ├── billing\_period\_schema.sql

│   └── invoice\_schema.sql

│

├── test/

│   ├── conftest.py

│   └── test\_api.py

│

├── Dockerfile

├── docker-compose.yml

├── pytest.ini

├── requirements.txt

└── .gitignore



API Endpoints



Usage



Method| Endpoint| Purpose

POST| "/usage/"| Create a usage event

GET| "/usage/"| List usage events



Pricing



Method| Endpoint| Purpose

POST| "/pricing/"| Create a pricing rule

GET| "/pricing/"| List pricing rules



Billing



Method| Endpoint| Purpose

GET| "/billing/{customer\_id}"| Calculate billing for a period



Billing Periods



Method| Endpoint| Purpose

POST| "/billing-periods/"| Create a billing period

GET| "/billing-periods/{customer\_id}"| List customer billing periods



Invoices



Method| Endpoint| Purpose

POST| "/invoices/{customer\_id}/{billing\_period\_id}"| Generate an invoice

GET| "/invoices/{customer\_id}"| List customer invoices



Health



Method| Endpoint| Purpose

GET| "/"| API information

GET| "/health"| Health check



Example Pricing Rules



Service| Unit| Price

API| requests| ₹0.01

Storage| GB| ₹5.00



Example Billing Calculation



For November 2026, customer "customer-001" had:



\- 500 API requests × ₹0.01 = ₹5.00

\- 10 GB storage × ₹5.00 = ₹50.00



Total:



₹55.00



Invoice Example



The November billing period generates:



Invoice Number: INV-CUSTOMER-001-0003

Customer: customer-001

Billing Period: 2026-11-01 to 2026-11-30

Total: ₹55.00

Currency: INR

Status: issued



After invoice generation, the corresponding billing period is closed.



Running Locally



1\. Create and activate a virtual environment



Windows:



python -m venv venv

venv\\Scripts\\activate



2\. Install dependencies



pip install -r requirements.txt



3\. Start PostgreSQL



The project uses PostgreSQL for persistent billing data.



The recommended setup is Docker Compose.



4\. Start the API



python -m uvicorn app.main:app --port 8001



The API will be available at:



http://127.0.0.1:8001



Swagger Documentation



Once the API is running, open:



http://127.0.0.1:8001/docs



Swagger UI provides interactive documentation and allows the API endpoints to be tested directly.



Running with Docker



Build and start the complete stack:



docker compose up -d --build



Check the containers:



docker compose ps



The services use:



\- API: port "8001"

\- PostgreSQL: host port "5433"



The API container connects to PostgreSQL through the Docker Compose network.



Running Tests



Run the automated test suite:



pytest -v



The test suite covers:



\- Root endpoint

\- Health endpoint

\- Pricing endpoint

\- Usage validation

\- Billing calculation

\- Invoice retrieval



Billing Workflow



Usage Events

&#x20;    │

&#x20;    ▼

Pricing Rules

&#x20;    │

&#x20;    ▼

Billing Calculation

&#x20;    │

&#x20;    ▼

Billing Period

&#x20;    │

&#x20;    ▼

Invoice Generation

&#x20;    │

&#x20;    ▼

Billing Period Closed



Database



The application uses PostgreSQL with the following main tables:



\- "usage\_events"

\- "pricing\_rules"

\- "billing\_periods"

\- "invoices"



Relationships between billing periods and invoices are enforced using PostgreSQL foreign keys.



Error Handling



The API handles common invalid operations including:



\- Invalid usage quantities

\- Missing billing periods

\- No billable usage

\- Duplicate invoices



HTTP status codes are used to communicate validation and API errors.



Docker Architecture



┌───────────────────────────────┐

│        FastAPI API            │

│          Port 8001            │

└───────────────┬───────────────┘

&#x20;               │

&#x20;               │ Docker Network

&#x20;               ▼

┌───────────────────────────────┐

│       PostgreSQL 16           │

│          Port 5432            │

│       Host Port 5433          │

└───────────────────────────────┘



Project Status



Core implementation completed and tested.



The project includes:



\- Usage metering

\- Pricing

\- Billing calculation

\- Billing periods

\- Invoice generation

\- PostgreSQL persistence

\- Docker deployment

\- Automated tests

\- Swagger API documentation



Author



Ayub Adil



Backend AI Engineering — FlyRank Internship Capstone

