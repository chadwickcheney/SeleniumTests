from django.urls import path

from . import views

app_name='assure'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:site_id>/', views.detail, name='detail'),
    path('<int:site_id>/results/', views.results, name='results'),
    path('<int:site_id>/comment/', views.comment, name='comment'),
]
