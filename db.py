import mysql.connector as m
import json


with open("./credentials.json", "r") as f:
    credentials = json.load(f)

    username = credentials["username"]
    password = credentials["password"]
    host = credentials["db-host"]

    # print(username, password)

    if username and password == "":
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
    cursor.execute("USE reader;")

except m.Error as e:
    print("------------------------------")
    print(f"\033[31m Error Code : {e.errno}\033[0m")
    print(f"\033[31m Error Message : {e.msg}\033[0m")
    print("------------------------------")


def urlsFromDatabase():
    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()
    urlData = output

    # print("-------------------------")
    # print(f"Fetched Data : {urlData}")
    # print("-------------------------")

    return urlData


def addDataToSql(url, name):
    insertCommand = "INSERT INTO feedUrls VALUES (%s, %s)"

    print("---------------------------------------------")
    print(f"INSERTION CMD : {insertCommand}, {url}")
    print("---------------------------------------------")

    try:
        cursor.execute(insertCommand, (url, name))
        db.commit()

        return True

    except:
        return False


def deleteDataSql(name):
    deleteCommand = "DELETE FROM feedUrls WHERE feedName=%s"

    print("---------------------------------------------")
    print(f"DELETION CMD : {deleteCommand % name}")
    print("---------------------------------------------")

    try:
        cursor.execute(deleteCommand, (name,))
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
