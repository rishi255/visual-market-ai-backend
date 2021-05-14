import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello user! What's up?"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
