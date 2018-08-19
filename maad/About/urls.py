from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Landing.as_view(), name='new'),
]
