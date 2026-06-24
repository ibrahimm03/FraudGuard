# FraudGuard 🛡️

A full-stack credit card fraud detection system built with Python, Flask, and SQLite. Transactions are analysed in real time against a rules-based fraud engine, with suspicious activity flagged and surfaced through a live dashboard.

## Features

- Real-time transaction simulation through an interactive dashboard
- Rules-based fraud detection engine — flags large amounts, high-frequency transactions, and unusual transaction hours
- Live stats: total transactions, fraud alerts, and flagged transactions
- Relational database schema with three linked tables (cards, transactions, alerts)
- REST API built with Flask, fully separated from the frontend
- Dedicated data access layer separating database logic from business logic
- Environment variables for sensitive configuration
- Card number masking for data minimisation
- Unit tests covering core fraud detection logic, including edge cases
- Git version control with descriptive commits at every milestone

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Testing:** pytest
- **Other:** python-dotenv for environment variable management

## Project Structure

```
fraudguard/
├── backend/
│   ├── app.py              # Flask REST API and server entry point
│   ├── database.py         # Data access layer — all SQL lives here
│   ├── fraud_engine.py      # Fraud detection logic (OOP)
│   └── models.py
├── frontend/
│   ├── index.html          # Dashboard structure
│   ├── style.css           # Dashboard styling
│   └── app.js               # Dashboard behaviour, talks to the API
├── tests/
│   └── test_fraud_engine.py # Unit tests for fraud detection rules
├── .env                     # Secret key (not uploaded)
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

1. A transaction is submitted through the dashboard (or directly to the API)
2. Flask receives the request and saves the transaction via the data access layer
3. The fraud engine analyses the transaction against a set of rules:
   - Is the amount unusually large?
   - Have there been too many transactions in a short window?
   - Did this happen at an unusual hour?
4. If any rule is triggered, the transaction is flagged and an alert is created
5. The dashboard updates instantly, showing the transaction and any fraud alerts — no page reload required

## Database Schema

Three tables, linked through foreign keys:

- **cards** — the credit cards being monitored
- **transactions** — every transaction made, linked to a card
- **alerts** — every fraud flag raised, linked to a transaction

## Fraud Detection Rules

| Rule | Logic | Severity |
|---|---|---|
| Large amount | Transaction over £3,000 | Medium/High |
| High frequency | 3+ transactions within 1 minute | High |
| Suspicious hour | Transaction between 1am–4am | Low |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ibrahimm03/FraudGuard.git
cd FraudGuard
```

### 2. Install dependencies

```bash
pip3 install flask python-dotenv pytest
```

### 3. Add environment variables

Create a `.env` file in the root folder:

```
SECRET_KEY=your-secret-key-here
```

### 4. Run the app

```bash
cd backend
python3 app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

### Running Tests

```bash
pytest tests/ -v
```

## What I Learned

- How to design a relational database schema from scratch, including foreign key relationships between tables
- How to build a data access layer to separate database logic from the rest of the application
- How to build and consume a REST API using Flask, including different HTTP methods and status codes
- How to apply object oriented programming principles — encapsulation and abstraction — to build a fraud detection engine
- How to connect a JavaScript frontend to a Python backend using asynchronous fetch requests
- How to write unit tests with pytest, including testing edge cases like exact threshold boundaries
- How to secure sensitive configuration using environment variables, and why this matters for production systems
- The importance of separation of concerns across an entire codebase — frontend, backend, data access layer, and fraud logic each have a single responsibility
- How version control supports iterative development, with commits marking meaningful milestones throughout the build

## Future Improvements

- Migrate from SQLite to PostgreSQL for concurrent access at scale
- Add user authentication for the dashboard
- Containerise the application with Docker
- Set up a CI/CD pipeline to run tests automatically on every push
- Expand the fraud engine with machine learning–based anomaly detection
