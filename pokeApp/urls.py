from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('pokemon/<int:id>', views.pokemon, name="pokemon"),
    path('team/', views.team_view, name="team"),
    path('team/add/<int:id>/', views.add_to_team, name="add_to_team"),
    path('team/remove/<int:id>/', views.remove_from_team, name="remove_from_team"),
    path('battle/', views.battle, name="battle"),

]