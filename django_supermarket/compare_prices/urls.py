from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search$', views.search, name='search'),
    url(r'^addtobasket$', views.addtobasket, name='addtobasket'),
    url(r'^getbasket$', views.getbasket, name='getbasket'),
    url(r'^getsummary$', views.getsummary, name='getsummary'),
    url(r'^clearbasket$', views.clearbasket, name='clearbasket'),
    #    url(r'^(?P<search_term>.+)/$', views.search, name='search'),
]

