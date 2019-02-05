from django.urls import path

from . import views

app_name = 'assure'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:site_id>/comment/', views.comment, name='comment'),
]
