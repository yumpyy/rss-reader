import mysql.connector as m
    
db = m.connect(host="localhost", user="anupam", passwd="anupam", database="reader")
cursor = db.cursor()

def urlsFromDatabase():

    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()

    urls = []
    for url in output:
        urls.append(url[0])
        
    return urls

# print(urlsFromDatabase())
