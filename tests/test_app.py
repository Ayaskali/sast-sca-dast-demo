import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vulnerable_flask_app"))
from app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index():
    assert client().get("/").status_code == 200


def test_hello_escapes_xss():
    r = client().get("/hello?name=<script>alert(1)</script>")
    assert b"<script>" not in r.data
    assert b"&lt;script&gt;" in r.data


def test_security_headers():
    r = client().get("/")
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert "Content-Security-Policy" in r.headers


def test_dangerous_routes_removed():
    c = client()
    assert c.get("/execute?cmd=id").status_code == 404
    assert c.get("/admin").status_code == 404
