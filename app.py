from flask import Flask, render_template
from main import feedFetch

app = Flask(__name__)

app.jinja_env.autoescape = False

@app.route("/")
def mainMenu():
    return render_template("index.html", articles=feedFetch())
    

@app.route("/articles")
def articleRead():
    return render_template("articles.html", articles=feedFetch())

app.run(debug=True)
