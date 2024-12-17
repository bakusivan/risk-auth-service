# Risk-Based Authentication Service

## Project Overview

This project implements a Risk-Based Authentication Service as a microservice using Python 3.12+ and FastAPI. The service evaluates authentication risks based on various factors such as user history, device, and network location.

## Problem Statement

The service provides a flexible risk assessment mechanism that allows dynamic authentication strategies based on:
- User identity
- Device familiarity
- Network origin (internal/external)
- Login history

## Features

- Log ingestion from multiple sources
- Real-time risk calculation
- Risk-based authentication support
- In-memory risk tracking

## Technical Stack

- Python 3.12+
- FastAPI
- Pytest (for testing)

## Project Structure

```
risk-auth-service/
│
├── src/
│   ├── main.py           # FastAPI application entry point
│   ├── risk_service.py   # Core risk calculation logic
│   ├── log_handler.py    # Log processing module
│   └── models.py         # Data models and type definitions
│
├── tests/
│   ├── test_risk_service.py
│   └── test_log_handler.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup and Installation

1. Clone the repository
```bash
git clone <repository-url>
cd risk-auth-service
```

2. Create a virtual environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Service

```bash
uvicorn src.main:app --reload
```

## Endpoints

- `POST /log`: Ingest log entries
- `GET /risk/isuserknown`: Check if a user is known
- `GET /risk/isipknown`: Verify IP address history
- `GET /risk/failedlogincountlastweek`: Retrieve failed login attempts

## Risk Assessment Logic

The service categorizes risk into three levels:
1. **Low Risk**: Known user, known device, internal network
2. **Medium Risk**: Known user, new device, internal network
3. **High Risk**: Known user, new device, external network

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Design Considerations

- In-memory storage for risk tracking
- Lightweight, extensible risk calculation
- Focus on PoC implementation
- Minimal external dependencies

## Future Improvements

- Persistent storage integration
- More granular risk scoring
- Enhanced logging and monitoring

## Limitations

- No permanent data storage
- Simplified risk calculation
- No authentication for the service itself