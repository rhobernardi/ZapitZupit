import os
from flask import Flask

app = Flask(__name__)

# file = open("/logs/bot.log", "rw")

@app.route("/")
def log():
    return "<html><body>HELLO BOT</body></html>"