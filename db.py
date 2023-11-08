import mysql.connector as m
    
db = m.connect(host="localhost", user="anupam", passwd="anupam", database="reader")
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
