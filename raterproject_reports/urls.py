from django.urls import path
from .views import game_rating_list

urlpatterns = [
    path('reports/gameReport', game_rating_list),
]