# RSS Reader

Simple RSS Feed Reader

Twitter and Youtube RSS feed urls can obtained using:
- [nitter](https://nitter.soopy.moe/) : Twitter
- [invidious](https://inv.in.projectsegfau.lt/) : Youtube

## Insallation/Usage

Linux/MacOS :

```
python -m venv env && \
source ./env/bin/activate && \
pip install -r requirements.txt && \
python app.py
```

Windows (powershell):

```
python -m venv env && \
./env/bin/Activate.ps1 && \
pip install -r requirements.txt && \
python app.py
```

Head over to `localhost:5000` to view the RSS Reader.

## Misc.

A simple service file.

```
[Unit]
Description="Local RSS Reader"

[Service]
WorkingDirectory=<project-folder-location>
ExecStart=/bin/bash -c 'cd <project-folder-location> && source ./env/bin/activate && python app.py'
```
