import feedparser
import uuid

from db import urlsFromDatabase


def feedFetch():
    urlData = urlsFromDatabase()
    print("-------------------------")
    print(f"Full Url Data: ")
    print(f"{urlData}")
    print("-------------------------")

    articles = []
    feed = {}

    for url in urlData:
        print("-------------------------")
        print(f"Parsing : {url}")
        print("-------------------------")

        parser = feedparser.parse(url[0])
        # print(parser)
        for x in range(len(parser["entries"])):
            try:
                feed = {
                    "name": url[1],
                    "id": uuid.uuid4().hex,
                    "title": parser["entries"][x]["title"],
                    "published": parser["entries"][x]["published_parsed"],
                    "linkOriginal": parser["entries"][x]["links"][0]["href"],
                }

                if "content" in parser["entries"][x]:
                    feed["content"] = parser["entries"][x]["content"][0]["value"]
                else:
                    feed["content"] = parser["entries"][x]["summary"]
                
                # print(feed)
                articles.append(feed)

            except KeyError as e:
                errorKey = e.args[0]
                print(f"Couldn't get {errorKey} from {parser['entries'][x]}")

    print(articles)
    articles = dateSort(articles)
    return articles


# for sorting all articles date wise
def dateSort(articles):
    for article in articles:
        date = article["published"]
        date = list(date)

    articles.sort(
        key=lambda article: (
            article["published"][0],
            article["published"][1],
            article["published"][2],
            article["published"][3],
            article["published"][4],
        ),
        reverse=True,
    )

    for article in articles:
        date = article["published"]
        date = list(date)
        date = f"{date[0]}/{date[1]}/{date[2]} {date[3]}:{date[4]}"
        article["published"] = date

    print(articles)
    return articles
