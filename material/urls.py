from django.urls import path
from . import views

urlpatterns = [
    path('material-detail/<int:material_id>/', views.material_detail, name='material-detail'),
]