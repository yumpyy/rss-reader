import mysql.connector as m
import json
import feedparser
import uuid

with open("./credentials.json", "r") as f:
    credentials = json.load(f)

    username = credentials["username"]
    password = credentials["password"]
    host = credentials["db-host"]

    if username == "":
        print("------------------------------------------------------")
        print("\n\033[31mSET YOUR USERNAME AND PASSWORD IN ./credentials.json\033[0m\n")
        print("------------------------------------------------------")

        exit()

db = m.connect(host=host, user=username, passwd=password)
cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS reader")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS reader.feedUrls (urls VARCHAR(900), feedName VARCHAR(255))"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS reader.articles (name VARCHAR(255) NOT NULL, uniqueID VARCHAR(32) NOT NULL, title VARCHAR(255) NOT NULL, published VARCHAR(255) NOT NULL, linkOriginal VARCHAR(255) NOT NULL, content MEDIUMTEXT CHARACTER SET utf8mb4, viewed ENUM('y', 'n'), UNIQUE(title))"
    )
    cursor.execute("USE reader")

except m.Error as e:
    print("---------------------------------------------")
    print(f"\033[31m Error Code : {e.errno}\033[0m")
    print(f"\033[31m Error Message : {e.msg}\033[0m")
    print("---------------------------------------------")

    exit()

def urlsFromDatabase():
    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()
    urlData = output

    return urlData


def rssValidation(url):
    validation = feedparser.parse(url).version

    if validation != "":
        return True

    elif validation == "":
        return False

def addFeedUrlsToSql(url, name):
    insertCommand = "INSERT INTO feedUrls VALUES (%s, %s)"

    print("---------------------------------------------")
    print(f"INSERTION CMD : {insertCommand}, {url}")
    print("---------------------------------------------")

    cursor.execute(insertCommand, (url, name))
    db.commit()

def deleteDataSql(name):
    deleteFeedUrls = "DELETE FROM feedUrls WHERE feedName=%s"
    deleteRelatedArticles = "DELETE FROM articles WHERE name=%s"

    print("---------------------------------------------")
    print(f"DELETION CMD : {deleteFeedUrls % name}")
    print("---------------------------------------------")

    try:
        cursor.execute(deleteFeedUrls, (name,))
        cursor.execute(deleteRelatedArticles, (name,))
        db.commit()

        print("---------------------------------------------")
        print("Data deleted successfully")
        print("---------------------------------------------")

        return True
    except:
        print("---------------------------------------------")
        print("Failed to delete data")
        print("---------------------------------------------")

        return False


async def feedFetch():
    urlData = urlsFromDatabase()

    print("-------------------------")
    print(f"Full Url Data: ")
    print(f"{urlData}")
    print("-------------------------")

    for url in urlData:
        print("-------------------------")
        print(f"Parsing : {url}")
        print("-------------------------")

        parser = feedparser.parse(url[0])

        for x in range(len(parser["entries"])):
            name = url[1]
            uniqueID = uuid.uuid4().hex
            title = parser["entries"][x]["title"]

            cursor.execute("SELECT * FROM articles WHERE title=%s", (title,))
            existingArticle = cursor.fetchone()

            if existingArticle is None:
                if "published_parsed" in parser["entries"][x]:
                    published = parser["entries"][x]["published_parsed"]
                else:
                    published = parser["entries"][x]["updated_parsed"]

                published = list(published)
                published = f"{published[0]}/{published[1]}/{published[2]} {published[3]}:{published[4]}"

                linkOriginal = parser["entries"][x]["links"][0]["href"]

                if "content" in parser["entries"][x]:
                    content = parser["entries"][x]["content"][0]["value"]
                else:
                    content = parser["entries"][x]["summary"]

                viewed = "n"
                insertCommand = "INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    insertCommand,
                    (name, uniqueID, title, published, linkOriginal, content, viewed),
                )
                db.commit()
            
            else:
                continue

def fetchDataFromSQL():
    cursor.execute(
        "SELECT * FROM articles ORDER BY STR_TO_DATE(published, '%Y/%m/%d') DESC"
    )
    fetchedData = cursor.fetchall()

    articles = []
    for article in fetchedData:
        feed = {
            "name": article[0],
            "uniqueID": article[1],
            "title": article[2],
            "published": article[3],
            "linkOriginal": article[4],
            "content": article[5],
            "viewed": article[6],
        }
        articles.append(feed)

    return articles


def markArticleRead(uniqueID):
    updateCommand = "UPDATE articles SET viewed = 'y' WHERE uniqueID=%s"
    cursor.execute(updateCommand, (uniqueID,))
    db.commit()
