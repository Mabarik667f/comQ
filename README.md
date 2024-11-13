# ComQ
Мессенджер, аналог телеграмма.
Есть возможность создания личных и групповых чатов, для работы с websockets используется `django-channels`

Messenger, analog of telegram.
There is a possibility to create personal and group chats, `django-channels` is used to work with websockets

# What can be improved 
- move orm ops from models to crud.py
- UTC timezone
- stability of websocket connections

# dev commands
```
gunicorn --reload config.wsgi:application
hypercorn --debug --reload config.asgi:application
```
# dev frontend (frontend dir)
```
npm run serve
```

# deploy
create certbot 
https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal
```
docker compose up -d
```

```
docker compose exec wsgi python manage.py migrate 
```
