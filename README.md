# rss-reader

simple rss reader made using flask

a centralised way to get your daily news/feed.


twitter and youtube rss feeds are available by using 3rd party privacy focused frontend nitter.net(for twitter) and inv.vern.cc(for youtube)

## dependecies

flask
feedparser

## insallation

run this command in terminal

```
python -m venv env && \
source ./env/bin/activate && \
pip install -r requirements.txt && \
python app.py \
```

now head over to localhost:5000 to view the rss reader

## todo

- [ ] logs
- [ ] maybe a electron app?
- [ ] normal json file instead of some database
- [ ] a way to view articles from specific feed
- [x] gui using flask
- [x] nicer looking ui 
- [x] youtube/twitter feed support
