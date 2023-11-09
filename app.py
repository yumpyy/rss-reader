from flask import Flask, render_template, request
from main import feedFetch
from db import addDataToSql, urlsFromDatabase, deleteDataSql

app = Flask(__name__)

app.jinja_env.autoescape = False

articlesList = feedFetch()

@app.route("/")
def mainMenu():
    return render_template("index.html", articles=articlesList)
    

@app.route("/articles")
def articleRead():
    articleRequested = request.args.get("q")
    
    for feed in articlesList:
        print('----', feed["linkOriginal"])
        if articleRequested == feed["linkOriginal"]:
            return render_template("articles.html", article=feed)
        else:
            continue

    return render_template("404.html")

@app.route("/manage", methods=['POST', 'GET'])
def addFeed():

    if request.method == "GET":
        return render_template("addfeed.html", urlData=urlsFromDatabase())

    name = request.form.get("name")
    action = request.form.get("action")
    url = request.form.get("url")

    if action == "Submit":

        if addDataToSql(url, name):
            return render_template("addfeed.html", urlData=urlsFromDatabase())
        else:
            return render_template("404.html")

    elif action == "Delete":

        if deleteDataSql(name):
            return render_template("addfeed.html", urlData=urlsFromDatabase())
        else:
            return render_template("404.html")

    else:
        return render_template("addfeed.html", urlData=urlsFromDatabase())

app.run(debug=True)
