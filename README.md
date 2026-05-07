# ZI Webhook Relay

A lightweight webhook relay service built with FastAPI.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8443
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /webhook | Receive and log webhook data |
| POST | /webhook/forward | Simulate forwarding webhook to target URL |

## Docker

```bash
docker build -t zi-webhook-relay .
docker run -p 8443:8443 zi-webhook-relay
```
