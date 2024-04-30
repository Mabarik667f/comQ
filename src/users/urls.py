from django.urls import path
from .views import *


urlpatterns = [
    path('short-data/<int:user_id>', UserShortDataView.as_view()),
    path('profile/<int:user_id>', UserProfileView.as_view()),

    path('login/', MyObtainTokenPairView.as_view(), name='toke_obtain_pair'),
    path('login/refresh/', MyRefreshTokenView.as_view(), name='token_refresh'),
    path('login/verify/', MyVerifyTokenView.as_view(), name='token_verify'),
    path('logout/', MyTokenBlackListView.as_view(), name='token_blacklist'),
    path('register/', RegisterView.as_view(), name='register')
]