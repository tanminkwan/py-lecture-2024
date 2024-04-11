from flask import Flask, render_template

app = Flask(import_name=__name__)

@app.route("/home/<username>")
def home(username):
    return render_template('index.html',title=f'{username}님 환영합니다.')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)