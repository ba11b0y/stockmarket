from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login/$', views.loginview, name='login'),
    url(r'logout/$', views.logoutview, name='logout'),
    url(r'signup/$', views.signup, name='signup'),
    url(r'^stocks/(?P<pk>[0-9])/$', views.successful_login, name='successful_login'),
    url(r'^buystocks/(?P<pk>[0-9]+)/(?P<sn>[A-Z]+)/buy/$', views.buy, name='buy'),
    url(r'^sellstocks/(?P<pk>[0-9]+)/(?P<sn>[A-Z]+)/buy/$', views.buy, name='sell'),
]
