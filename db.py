import mysql.connector as m
    
db = m.connect(host="localhost", user="anupam", passwd="anupam", database="reader")
cursor = db.cursor()

def urlsFromDatabase():

    cursor.execute("SELECT * FROM feedUrls")
    output = cursor.fetchall()

    urlData = output
    # for url in output:
    #     urls.append(url[0])
        
    return urlData

print(urlsFromDatabase())
