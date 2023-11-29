# ZapitZupit
A telegram bot that receive phone numbers via text or images and generate WhatsApp links to send messages without add a stranger contact to your phone.

## Compile in Docker
```bash
$ source config.sh
$ bot-install [API_KEY]
```

## Running
```bash
$ bot-run
```

## Access logs

```bash
$ cat ~/telebot/log/bot.log
```

## Compile in Docker
```bash
$ source config.sh
$ docker-bot-compile
```

## Running with Docker
```bash
$ docker rm zapitzupit; docker run -d -it --name zapitzupit telebot
```

## Access logs in Docker

```bash
$ source ./config.sh
$ docker-bot-attach zapitzupit

$ cat log/bot.log
```
