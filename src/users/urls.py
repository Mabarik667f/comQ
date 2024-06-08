from django.urls import path
from .views import *


urlpatterns = [
    path('profile/<int:user_id>/', UserProfileView.as_view()),
    path('userData/<int:user_id>/', UserDataView.as_view()),
    path('userOnChat/<slug:username>/', UserDataOnChatView.as_view()),

    path('login/', MyObtainTokenPairView.as_view(), name='toke_obtain_pair'),
    path('login/refresh/', MyRefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_blacklist'),
    path('register/', RegisterView.as_view(), name='register')
]