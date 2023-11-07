from flask import Flask, render_template, request
from main import feedFetch

app = Flask(__name__)

app.jinja_env.autoescape = False

@app.route("/")
def mainMenu():
    articlesList = feedFetch()
    return render_template("index.html", articles=articlesList)
    

@app.route("/articles")
def articleRead():
    articlesList = feedFetch()

    articleRequested = request.args.get("q")

    for feed in articlesList:
        if articleRequested == feed["title"]:
            return render_template("articles.html", article=feed)
        else:
            continue

    return render_template("404.html")

app.run(debug=True)
