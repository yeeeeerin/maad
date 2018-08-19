from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [	

	url(r'^add/$', views.ProjectCreateView.as_view(), name='create_pro'),
	url(r'^search/$', views.SearchFormView.as_view(), name='search'),
	url(r'^search/autocomplete/$', views.AutoCompleteView.as_view(), name='auto'),
	url(r'^(?P<pk>\d+)/(?P<slug>[\w\-]+)/type_create/$', views.FolderCreate.as_view(), name='type_create'),
	url(r'^(?P<pk>\d+)/(?P<slug>[\w\-]+)/(?P<ti>\w+)/moodboard/$', views.PictureCreateView.as_view(), name='create_pic'),
	url(r'^(?P<slug>\w+)/(?P<ti>[\w\-]+)/(?P<pk>\w+)/delete/$',views.Delete.as_view(), name='delete'),
	url(r'^(?P<slug>\w+)/(?P<ti>[\w\-]+)/(?P<pk>\w+)/urldelete/$',views.URLDelete.as_view(), name='url_delete'),
	url(r'^(?P<slug>[\w\-]+)/(?P<ti>\w+)/text/$', views.index, name='create_text'),
	url(r'^(?P<pk>\d+)/(?P<slug>[\w\-]+)/(?P<ti>\w+)/url/$', views.URLCreateView.as_view(), name='create_url'),
	url(r'^$', views.ProjectIndex.as_view(), name='index'),
] 
