
from django.conf.urls import url
from . import views

app_name="elections"
urlpatterns = [
    url(r'^$', views.index, name= "home"),
    url(r'^areas/(?P<area>.+)/$', views.areas),
    url(r'^areas/(?P<area>.+)/results$', views.results),
    url(r'^polls/(?P<poll_id>.+)/$', views.polls),
    url(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates),
]
