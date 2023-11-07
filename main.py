import feedparser
import dateutil.parser
import datetime
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
                        'published' : parser['entries'][x]['published'],
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
    for x in range(len(articles)):
        try:
            dates = sorted(map(dateutil.parser.parse, articles[x]['published']))
        except dateutil.parser._parser.ParserError:
            dates = []
        sortedDates = [d.strftime('%Y-%m-%d') for d in dates]
        print(sortedDates)

# feedFetch()
dateSort(feedFetch())
