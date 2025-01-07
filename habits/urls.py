from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .apps import HabitsConfig
from .views import HabitViewSet, PublicHabitListView

app_name = HabitsConfig.name
router = DefaultRouter()
router.register(r"habits", HabitViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("public-habits/", PublicHabitListView.as_view(), name="public_habits"),
]

