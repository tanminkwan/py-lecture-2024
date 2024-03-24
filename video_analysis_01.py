from flask import Flask

app = Flask(import_name=__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)