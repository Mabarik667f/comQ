from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

USER = get_user_model()


class JWTAuthBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return USER.objects.get(pk=user_id)
        except USER.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = USER.objects.get(
                Q(username=username) | Q(email=username)
            )
        except USER.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None
