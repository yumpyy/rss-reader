import mysql.connector as m
import json


with open("./credentials.json", "r") as f:
    credntials = json.load(f)

    username = credntials['username']
    password = credntials['password']

    # print(username, password)

    if username and password == "":
        print('------------------------------------------------------')
        print("\nSET YOUR USERNAME AND PASSWORD IN ./credentials.json \n")
        print('------------------------------------------------------')

        exit()
    

db = m.connect(host="localhost", user=username, passwd=password)
cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS reader")
except:
    print('------------------------------')
    print(f'\nCOULDNT CREATE DATABASE!!!\n')
    print('------------------------------')

try:
    cursor.execute("CREATE TABLE IF NOT EXISTS reader.feedUrls (urls VARCHAR(900), feeName VARCHAR(255))")
except:
    print('------------------------------')
    print(f'\nCOULDNT CREATE TABLE!!!\n')
    print('------------------------------')

cursor.execute("USE reader;")

def urlsFromDatabase():

    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()
    urlData = output
    
    print(urlData)
    return urlData

def addDataToSql(url, name):

    insertCommand = "INSERT INTO feedUrls VALUES (%s, %s)"
    
    try:
        cursor.execute(insertCommand, (url, name))
        db.commit()
        return True

    except:
        return False
