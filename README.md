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
