
from flask import Flask, render_template
from main import atomReader

app = Flask(__name__)

app.jinja_env.autoescape = False

@app.route("/")
def mainMenu():
    return render_template("index.html", articles=atomReader("test.xml") )
    

@app.route("/articles")
def articleRead():
    return render_template("articles.html", articles=atomReader("test.xml") )

app.run(debug=True)
