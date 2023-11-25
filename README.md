# ZapitZupit
A telegram bot that receive phone numbers via text or images and generate WhatsApp links to send messages without add a stranger contact to your phone.

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
