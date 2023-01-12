# offtop_bot

Guide for .env
```dotenv
#this token for bot
BOT_TOKEN=

#this id and url group where will we redirect
OFF_TOP_CHAT_ID=
OFF_TOP_CHAT_URL=

# 0 - false
# 1 - true
WEBHOOK=1
STATISTICS=1

#webhook settings
WEBHOOK_PATH=""
WEBHOOK_URL="https://b3f5-46-211-234-79.eu.ngrok.io"
WEBAPP_HOST='127.0.0.1'
WEBAPP_PORT=5051

#path for bd
DATABASE_STATISTICS=database.bd
#if db was found but it doesn't have a table script to add it automatically with the /start command
DATABASE_STATISTICS_AUTO=1
```

To create database.bd use this command
```
CREATE TABLE "statistic" (
	"username"	TEXT NOT NULL,
	"id"	INTEGER NOT NULL UNIQUE,
	"count"	INTEGER NOT NULL DEFAULT 0
);
```
