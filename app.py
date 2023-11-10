import json
from flask import Flask, render_template, request
from main import feedFetch
from db import addDataToSql, urlsFromDatabase, deleteDataSql

app = Flask(__name__)
app.jinja_env.autoescape = False

articlesList = feedFetch()


@app.route("/")
def mainMenu():
    action = request.args.get("action")
    if action == "refresh":
        print("-------------")
        print("REFRESHING...")
        print("-------------")

        global articlesList
        articlesList = feedFetch()
        return render_template("index.html", articles=articlesList)

    else:
        return render_template("index.html", articles=articlesList)


@app.route("/articles")
def articleRead():
    articleRequested = request.args.get("q")

    for feed in articlesList:
        if articleRequested == feed["linkOriginal"]:
            return render_template("articles.html", article=feed)
        else:
            continue

    return render_template("404.html")


# page managing feed urls
@app.route("/manage", methods=["POST", "GET"])
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


with open("./credentials.json", "r") as f:
    credntials = json.load(f)
    port = credntials["port"]
    print(port)

try:
    app.run(debug=True, port=port)
except OSError:
    print(
        "\n\033[31m SOME OTHER SERVICE IS RUNNING ON DEFAULT PORT 5000\nCONSIDER CHANGING PORT IN ./credentials.json \033[0m\n"
    )
