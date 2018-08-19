"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
#from acc.forms import LoginForm
from Account.forms import PasswordChangeForm
from django.contrib.auth import views as auth_views
from mysite.views import UserCreateView, UserCreateDoneTV ,LoginDoneView
from Project.views import ProjectCreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('About.urls', namespace='About')),
    #Project
    url(r'^Project/', include('Project.urls', namespace="Project")),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    #url(r'^accounts/login/$', django.contrib.auth.views.login, {'authentication_form': LoginForm},name = 'login_url'),
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', auth_views.login,name = 'login_url'),
    url(r'^accounts/login/done/$',ProjectCreateView.as_view(),name = 'login_done'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page' :'/accounts/login/'},name = 'logout_url'),
    url(r'^accounts/password_change/$', auth_views.password_change,
        {'template_name': 'registration/password_change_form.html','post_change_redirect': '/accounts/password_change/done/'},
        name='password_change'),
    url(r'^accounts/password_change/done/$', auth_views.password_change_done,name = 'password_change_done'),
    url(r'^accounts/register/$', UserCreateView.as_view(), name='register'),
    url(r'^accounts/register/done/$', UserCreateDoneTV.as_view(), name='register_done'),
    

    #password lost   
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')), 
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
