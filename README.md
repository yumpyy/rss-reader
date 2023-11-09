# rss-reader

simple rss reader made using flask  
a centralised way to get your daily news/feed.

twitter and youtube rss feed urls can obtained by using alternate privacy focused frontends like [nitter](https://nitter.soopy.moe/) (for twitter) and [invidious](https://inv.in.projectsegfau.lt/)  (for youtube)

## insallation/usage

run this command in terminal

linux/macos :

```
python -m venv env && \
source ./env/bin/activate && \
pip install -r requirements.txt && \
python app.py \
```

windows (powershell):

```
python -m venv env && \
./env/bin/Activate.ps1 && \
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
