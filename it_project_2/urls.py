"""it_project_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from messenger import views as m_views
from profiles import views as p_views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', m_views.messages_view, name='home'),
    url(r'^chat(?P<chat_id>[\d]+)$', m_views.chat_view, name='chat'),
    url(r'^signup$', p_views.signup_view, name='signup'),
    url(r'^login$', p_views.login_view, name='login'),
    url(r'^restore', p_views.restore_view, name='restore'),
    url(r'^logout$', p_views.logout_view, name='logout'),
]
