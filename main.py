import feedparser
from datetime import datetime
from dateutil.parser import parse
from db import urlsFromDatabase

def feedFetch():
    urlData = urlsFromDatabase()
    # print(urls)
    # global articles
    articles = []
    feed = {}

    for url in urlData:
        # print(url)
        parser = feedparser.parse(url[0])
        # print(parser)
        for x in range(len(parser['entries'])):
            try:
                feed = {
                        'feed-name' : url[1],
                        'title' : parser['entries'][x]['title'],
                        'published' : parser['entries'][x]['published_parsed'],
                        'linkOriginal' : parser['entries'][x]['links'][0]['href']
                        }

                if 'summary' in feed:
                    feed['summary'] = parser['entries'][x]['summary']
                else:
                    feed['summary'] = ''

                if 'content' in feed:
                    feed['content'] = parser['entries'][x]['content'][0]['value']
                else:
                    feed['content'] = parser['entries'][x]['summary']

                articles.append(feed)
            except KeyError as e:
                errorKey = e.args[0]

                if errorKey in feed:
                    feed[errorKey] = feed['summary']
                else:
                    feed[errorKey] = ''
        
    return articles

def dateSort(articles):
    dates = []
    for article in articles:
        date = article['published']
        date = list(date)
        date = f'{date[0]}/{date[1]}/{date[2]} {date[3]}:{date[4]}'
        dates.append(date)

        # date.sort(key=lambda date: datetime.strptime(date, '%Y/%m/%d %H:%M'))
    dates.sort(key=lambda date: datetime.strptime(date, '%Y/%m/%d %H:%M'), reverse=True)
    print(dates)
    # Append the sorted dates to the original list
    articles.sort(key=lambda article: dates[article['published']])
    
# feedFetch()
dateSort(feedFetch())
