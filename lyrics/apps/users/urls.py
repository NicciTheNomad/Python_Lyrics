from django.conf.urls import url
from . import views

# urlpatterns = [
#     url(r'^users/$', views.index),
#     url(r'^users/success$', views.success),
#     url(r'^users/logout$', views.logout),
#     url(r'^users/register$', views.register),
#     url(r'^users/log_in$', views.log_in),
# ]
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^log_in$', views.log_in),
]