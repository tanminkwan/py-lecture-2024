from flask import Flask, render_template

app = Flask(import_name=__name__)

@app.route("/")
def home():
    return render_template('index.html',title="동영상을 분석해드립니다.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)