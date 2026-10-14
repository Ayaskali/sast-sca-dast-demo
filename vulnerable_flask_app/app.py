import os
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
# Correction 1 : secret lu depuis une variable d'environnement
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", os.urandom(32))

# Correction 2 : en-tetes de securite HTTP
@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    return resp

@app.route('/')
def index():
    return '<h1>Welcome</h1><ul><li><a href="/hello?name=World">Hello Page</a></li></ul>'

# Correction 3 : echappement de l'entree utilisateur (XSS)
@app.route('/hello')
def hello():
    name = escape(request.args.get('name', 'Guest'))
    return f"<h1>Hello Page</h1><p>Hello, {name}!</p><p><a href='/'>Back</a></p>"

# Correction 4 : routes /execute et /admin supprimees

if __name__ == '__main__':
    # Correction 5 : debug desactive, ecoute locale par defaut (0.0.0.0 fourni par Docker)
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1",
            host=os.environ.get("APP_HOST", "127.0.0.1"))
