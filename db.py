import mysql.connector as m
import json


with open("./credentials.json", "r") as f:
    credntials = json.load(f)

    username = credntials['username']
    password = credntials['password']

    # print(username, password)

    if username and password == "":
        print('------------------------------------------------------')
        print("\n\033[31mSET YOUR USERNAME AND PASSWORD IN ./credentials.json\033[0m\n")
        print('------------------------------------------------------')

        exit()
    

db = m.connect(host="localhost", user=username, passwd=password)
cursor = db.cursor()

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS reader")
except:
    print('------------------------------')
    print(f'\n\033[31mCOULDNT CREATE DATABASE!!!\033[0m\n')
    print('------------------------------')

try:
    cursor.execute("CREATE TABLE IF NOT EXISTS reader.feedUrls (urls VARCHAR(900), feedName VARCHAR(255))")

except:
    print('------------------------------')
    print(f'\n\033[31mCOULDNT CREATE TABLE!!!\033[0m\n')
    print('------------------------------')

cursor.execute("USE reader;")

def urlsFromDatabase():

    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()
    urlData = output
    
    print('-------------------------')
    print(f'Fetched Data : {urlData}')
    print('-------------------------')

    return urlData

def addDataToSql(url, name):

    insertCommand = "INSERT INTO feedUrls VALUES (%s, %s)"

    print('---------------------------------------------')
    print(f'INSERTION CMD : {insertCommand}, {url}')
    print('---------------------------------------------')
    
    try:
        cursor.execute(insertCommand, (url, name))
        db.commit()
        
        return True

    except:
        return False


def deleteDataSql(name):
    deleteCommand = "DELETE FROM feedUrls WHERE feedName=%s"
    
    print('---------------------------------------------')
    print(f'DELETION CMD : {deleteCommand % name}')
    print('---------------------------------------------')

    try:
        cursor.execute(deleteCommand, (name,))
        db.commit()

        print('---------------------------------------------')
        print('Data deleted successfully')
        print('---------------------------------------------')

        return True
    except:

        print('---------------------------------------------')
        print('Failed to delete data')
        print('---------------------------------------------')
        return False
