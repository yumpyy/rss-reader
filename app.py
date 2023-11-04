
from flask import Flask, render_template
from main import atomReader

app = Flask(__name__)

app.jinja_env.autoescape = False


@app.route("/")
def articleRead():
    return render_template("index.html", feed=atomReader("test2.rss") )

app.run(debug=True)
