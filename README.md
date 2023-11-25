# ZapitZupit
A bot that receive phone numbers via text or photos and generate WhatsApp links without add a stranger contact.

## Compile
```
$ source config.sh
$ bot-compile
```

## Running
```
$ docker rm zapitzupit; docker run -d -it --name zapitzupit telebot
```

## Access logs

```
$ source ./config.sh
$ bot-attach zapitzupit

# cat log/bot.log
```
