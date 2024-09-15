import json
from flask import Flask, render_template, request

import db
from sanitize import sanitize

app = Flask(__name__)
app.jinja_env.autoescape = False

articles = db.fetch_data_from_db()

@app.route("/")
async def main_menu():
    action = request.args.get("action")
    if action == "refresh":
        print("-------------")
        print("REFRESHING...")
        print("-------------")
        
        await db.feed_fetch()

        global articles
        articles = db.fetch_data_from_db()
        return render_template("index.html", articles=articles)

    else:
        return render_template("index.html", articles=articles)

@app.route("/articles")
def read_article():
    article_id = request.args.get("q")
    article_link = request.args.get("fullfetch")

    for feed in articles:
        article_index_current = articles.index(feed)

        arcticle_index_next = article_index_current + 1
        arcticle_index_prev = article_index_current - 1

        if article_index_current == 0:
            arcticle_index_prev = 0

        article_id_next = articles[arcticle_index_next]["uniq_id"]
        article_id_prev = articles[arcticle_index_prev]["uniq_id"]

        if article_id == feed["uniq_id"]: # for article card in main menu
            db.mark_article_read(feed["uniq_id"])
            
            return render_template("articles.html", article=feed, 
            article_id_next=article_id_next, article_id_prev=article_id_prev)

        elif article_link == feed["orginal_link"]: # for full fetch
            sanitized_content = sanitize(article_link)
            feed["content"] = sanitized_content

            return render_template("articles.html", article=feed, 
            article_id_next=article_id_next, article_id_prev=article_id_prev)
        else:
            continue

    return render_template("404.html")

# page managing feed urls
@app.route("/manage", methods=["POST", "GET"])
def add_feed():
    if request.method == "GET":
        validation = { "method" : "put" }

        return render_template("addfeed.html", url_data=db.fetch_urls_from_db(), validation=validation)

    name = request.form.get("name")
    action = request.form.get("action")
    url = request.form.get("url")

    if action == "Submit":
        if db.validate_rss(url):
            db.add_feed_urls_to_db(url, name)
            validation = {
                    'msg' : "Feed is valid, Added to database.",
                    'id' : 3,
                    'class' : "success",
                    "method" : "put"
                    }

            return render_template("addfeed.html", url_data=db.fetch_urls_from_db(), validation=validation )
        else:
            validation = {
                    'msg' : "Feed isn't valid, Couldn't add to database.",
                    'id' : 5,
                    'class' : "danger",
                    "method" : "put"
                    }
            return render_template("addfeed.html", url_data=db.fetch_urls_from_db(), validation=validation )

    elif action == "Delete":
        if db.delete_from_db(name):
            validation = { "method" : "put" }

            return render_template("addfeed.html", url_data=db.fetch_urls_from_db(), validation=validation)
        else:
            return render_template("404.html")

    else:
        return render_template("addfeed.html", url_data=db.fetch_urls_from_db())

with open("./credentials.json", "r") as f:
    credentials = json.load(f)
    port = credentials["port"]
    host = credentials["server-host"]

try:
    # app.run(debug=True, port=port, host=host)
    if __name__ == '__main__':
        app.run(port=port, host=host)
except OSError:
    print(
        "\n\033[31m SOME OTHER SERVICE IS RUNNING ON DEFAULT PORT 5000\nCONSIDER CHANGING PORT IN ./credentials.json \033[0m\n"
    )
