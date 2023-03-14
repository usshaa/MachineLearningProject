from django.urls import path
from . import views

urlpatterns = [
    path('visual', views.visual, name='visual'),
    path('plot',views.plot,name='plot'),
]
