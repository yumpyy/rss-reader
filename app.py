import json
from flask import Flask, render_template, request

import db
from htmlCleaning import cleanHTML

app = Flask(__name__)
app.jinja_env.autoescape = False

articlesList = db.fetchDataFromSQL()
print(articlesList)


@app.route("/")
async def mainMenu():
    action = request.args.get("action")
    if action == "refresh":
        print("-------------")
        print("REFRESHING...")
        print("-------------")
        
        await db.feedFetch()

        global articlesList
        articlesList = db.fetchDataFromSQL()
        return render_template("index.html", articles=articlesList)

    else:
        return render_template("index.html", articles=articlesList)


@app.route("/articles")
def articleRead():
    articleRequestedID = request.args.get("q")
    ariceleRequestedLink = request.args.get("fullfetch")

    for feed in articlesList:
        if articleRequestedID == feed["uniqueID"]:
            db.markArticleRead(feed["uniqueID"])

            return render_template("articles.html", article=feed)

        elif ariceleRequestedLink == feed["linkOriginal"]:
            cleanContent = cleanHTML(ariceleRequestedLink)
            feed["content"] = cleanContent

            return render_template("articles.html", article=feed)
        else:
            continue

    return render_template("404.html")


# page managing feed urls
@app.route("/manage", methods=["POST", "GET"])
def addFeed():
    if request.method == "GET":
        validation = { "method" : "put" }

        return render_template("addfeed.html", urlData=db.urlsFromDatabase(), validation=validation)

    name = request.form.get("name")
    action = request.form.get("action")
    url = request.form.get("url")

    if action == "Submit":
        if db.rssValidation(url):
            db.addFeedUrlsToSql(url, name)
            validation = {
                    'msg' : "Feed is valid, Added to database.",
                    'id' : 3,
                    'class' : "success",
                    "method" : "put"
                    }

            return render_template("addfeed.html", urlData=db.urlsFromDatabase(), validation=validation )
        else:
            validation = {
                    'msg' : "Feed isn't valid, Couldn't add to database.",
                    'id' : 5,
                    'class' : "danger",
                    "method" : "put"
                    }
            return render_template("addfeed.html", urlData=db.urlsFromDatabase(), validation=validation )

    elif action == "Delete":
        if db.deleteDataSql(name):
            validation = { "method" : "put" }

            return render_template("addfeed.html", urlData=db.urlsFromDatabase(), validation=validation)
        else:
            return render_template("404.html")

    else:
        return render_template("addfeed.html", urlData=db.urlsFromDatabase())


with open("./credentials.json", "r") as f:
    credentials = json.load(f)
    port = credentials["port"]
    host = credentials["server-host"]

try:
    app.run(debug=True, port=port, host=host)
except OSError:
    print(
        "\n\033[31m SOME OTHER SERVICE IS RUNNING ON DEFAULT PORT 5000\nCONSIDER CHANGING PORT IN ./credentials.json \033[0m\n"
    )
