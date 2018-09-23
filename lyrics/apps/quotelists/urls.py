from django.conf.urls import url
from . import views

#quotes - quotelists

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'add$', views.add),
    url(r'^(?P<quote_id>\d+)/add_to_logged_user_list$', views.add_to_logged_user_list),
    url(r'^(?P<quote_id>\d+)/remove_from_logged_user_list', views.remove_from_logged_user_list),
    url(r'^(?P<name>\w+)', views.display),
]