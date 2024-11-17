import json
import uuid
import os.path
import sys

import mysql.connector as m
import feedparser

if not os.path.isfile('./credentials.json'):
    print("'credentials.json' doesn't exist.")
    sys.exit()

with open("./credentials.json", "r") as f:
    credentials = json.load(f)

    username = credentials["username"]
    password = credentials["password"]
    host = credentials["db-host"]

    if username == "" or password == "":
        print("Credentials for database are not set. Do you want to set it? [y/N]")
        choice = input("> ")
        if choice.lower() in ['y', 'yes']:
            username = input("Username for database: ")
            password = input("Password for database: ")

            credentials['username'] = username
            credentials['password'] = password
            json.dump(credentials, open('./credentials.json', 'w'), indent=4)

        sys.exit()

db = m.connect(host=host, user=username, passwd=password)
cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS reader")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS reader.feedUrls (urls VARCHAR(900), feedName VARCHAR(255))"
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS reader.articles (name VARCHAR(255) NOT NULL,
        uniq_id VARCHAR(32) NOT NULL,
        title VARCHAR(255) NOT NULL,
        published VARCHAR(255) NOT NULL,
        orginal_link VARCHAR(255) NOT NULL,
        content MEDIUMTEXT,
        viewed ENUM('y', 'n'), UNIQUE(title))"""
    )
    cursor.execute("USE reader")

except m.Error as e:
    print("---------------------------------------------")
    print(f"\033[31m Error Code : {e.errno}\033[0m")
    print(f"\033[31m Error Message : {e.msg}\033[0m")
    print("---------------------------------------------")

    sys.exit()

def fetch_urls_from_db():
    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()
    url_data = output

    return url_data

def validate_rss(url):
    validation = feedparser.parse(url).version

    if validation != "":
        return True

    elif validation == "":
        return False

def add_feed_urls_to_db(url, name):
    insert_command = "INSERT INTO feedUrls VALUES (%s, %s)"

    print("---------------------------------------------")
    print(f"INSERTION CMD : {insert_command}, {url}")
    print("---------------------------------------------")

    cursor.execute(insert_command, (url, name))
    db.commit()

def delete_from_db(name):
    delete_feed_urls_command = "DELETE FROM feedUrls WHERE feedName=%s"
    delete_articles_command = "DELETE FROM articles WHERE name=%s"

    print("---------------------------------------------")
    print(f"DELETION CMD : {delete_feed_urls_command % name}")
    print("---------------------------------------------")

    try:
        cursor.execute(delete_feed_urls_command, (name,))
        cursor.execute(delete_articles_command, (name,))
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

async def feed_fetch():
    url_data = fetch_urls_from_db()

    print("-------------------------")
    print(f"Full Url Data: ")
    print(f"{url_data}")
    print("-------------------------")

    for url in url_data:
        print("-------------------------")
        print(f"Parsing : {url}")
        print("-------------------------")

        parser = feedparser.parse(url[0])

        for x in range(len(parser["entries"])):
            name = url[1]
            uniq_id = uuid.uuid4().hex
            title = parser["entries"][x]["title"]

            cursor.execute("SELECT * FROM articles WHERE title=%s", (title,))
            existing_article = cursor.fetchone()

            if existing_article is None:
                if "published_parsed" in parser["entries"][x]:
                    published = parser["entries"][x]["published_parsed"]
                else:
                    published = parser["entries"][x]["updated_parsed"]

                published = list(published)
                published = f"{published[0]}/{published[1]}/{published[2]} {published[3]}:{published[4]}"

                orginal_link = parser["entries"][x]["links"][0]["href"]

                if "content" in parser["entries"][x]:
                    content = parser["entries"][x]["content"][0]["value"]
                else:
                    content = parser["entries"][x]["summary"]

                viewed = "n"
                insert_command = "INSERT INTO articles VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    insert_command,
                    (name, uniq_id, title, published, orginal_link, content, viewed),
                )
                db.commit()
            
            else:
                continue

def fetch_data_from_db():
    cursor.execute(
        "SELECT * FROM articles ORDER BY STR_TO_DATE(published, '%Y/%m/%d') DESC"
    )
    fetched_data = cursor.fetchall()

    articles = []
    for article in fetched_data:
        feed = {
            "name": article[0],
            "uniq_id": article[1],
            "title": article[2],
            "published": article[3],
            "orginal_link": article[4],
            "content": article[5],
            "viewed": article[6],
        }
        articles.append(feed)

    return articles

def mark_article_read(uniq_id):
    update_command = "UPDATE articles SET viewed = 'y' WHERE uniq_id=%s"
    cursor.execute(update_command, (uniq_id,))
    db.commit()
