import feedparser

url = "test.xml"
feedType = url.split(".")[1]

def atomReader(url):
    parser = feedparser.parse(url)
    # print(parser)
    #print(parser[''][0])
    feed = {
            'title' : parser['entries'][0]['title'],
            'published' : parser['entries'][0]['published'],
            'linkOriginal' : parser['entries'][0]['id'],
            'content' : parser['entries'][0]['content'][0]['value']
    }

    return feed


if feedType == "rss":
    print("Feed in RSS 2.0 format")
    rssReader(url)

elif feedType in ["atom","xml"]:
    print("Feed in atom format")
    atomReader(url)

from flask import Flask, render_template

app = Flask(__name__)

app.jinja_env.autoescape = False


@app.route("/")
def renderHtml():
    return render_template("index.html", feed=atomReader("test.xml") )

app.run(debug=True)
