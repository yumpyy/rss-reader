import mysql.connector as m
    
db = m.connect(host="localhost", user="anupam", passwd="anupam", database="reader")
cursor = db.cursor()

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
