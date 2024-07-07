import datetime

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db import close_old_connections
from django.utils import timezone
from users.models import CustomUser


@database_sync_to_async
def get_user(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        print(payload)
    except:
        return AnonymousUser()

    token_exp = datetime.fromtimestamp(payload['exp'])
    if token_exp < datetime.utcnow():
        return AnonymousUser()

    try:
        user = CustomUser.objects.get(id=payload['user_id'])
    except CustomUser.DoesNotExist:
        return AnonymousUser()

    return user


@database_sync_to_async
def update_last_login(scope):
    CustomUser.objects.filter(pk=scope['user'].pk).update(last_login=timezone.now())


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token_key = dict((x.split('=') for x in scope['query_string'].decode().split("&"))).get('token', None)
        except ValueError:
            token_key = None

        scope['user'] = await get_user(token_key)
        cache_key = f"last-seen-{scope['user'].pk}"
        last_login = cache.get(cache_key)

        if not last_login:
            await update_last_login(scope)
            cache.set(cache_key, timezone.now(), 300)

        return await super().__call__(scope, receive, send)


def JWTAuthMiddleWareStack(inner):
    return TokenAuthMiddleware(inner)