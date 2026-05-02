"""Tests for the webhook relay service."""
import json
import subprocess
import sys
import time
import urllib.request


_server_proc = None


def setup_module(module):
    """Start the uvicorn server for testing."""
    global _server_proc
    _server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "9123"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for _ in range(30):
        time.sleep(0.2)
        try:
            urllib.request.urlopen("http://127.0.0.1:9123/health", timeout=1)
            return
        except Exception:
            continue
    _server_proc.kill()
    raise RuntimeError("Server failed to start")


def teardown_module(module):
    """Stop the uvicorn server."""
    global _server_proc
    if _server_proc:
        _server_proc.kill()
        _server_proc.wait()


def _request(method, path, body=None):
    url = f"http://127.0.0.1:9123{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read())


def test_health():
    status, body = _request("GET", "/health")
    assert status == 200
    assert body == {"status": "healthy"}


def test_webhook():
    status, body = _request("POST", "/webhook", {"event": "test"})
    assert status == 200
    assert body["received"] is True
    assert "id" in body


def test_webhook_forward():
    status, body = _request("POST", "/webhook/forward", {
        "url": "https://example.com/hook",
        "payload": {"key": "value"},
    })
    assert status == 200
    assert body["forwarded"] is True
    assert body["target"] == "https://example.com/hook"
