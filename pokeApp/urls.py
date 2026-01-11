from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = "index"),
    path('pokemon/<int:id>', views.pokemon, name="pokemon"),
    
    path('team/create/', views.create_team, name='create_team'),
    path('team/', views.team_view, name='team'),
    path('team/add/<int:pokemon_id>/', views.add_to_team, name='add_to_team'),
]