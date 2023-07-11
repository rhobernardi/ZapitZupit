import os
from flask import Flask

app = Flask(__name__)

# file = open("/logs/bot.log", "rw")

@app.route("/")
def log():
    return "<html><body>HELLO BOT</body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)