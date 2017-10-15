# video-crowd-control
A simple docker based webserver to crowd review videos and assess their quality

## tldr
```
docker run --name video-crowd-db -d mongo
docker run --name video-crowd-control --restart=always -p 1081:80 --link video-crowd-db:mongo -v ~/Projects/video-crowd-control/:/app -v videoFolder/:/app/static/videos -d jazzdd/alpine-flask
```
