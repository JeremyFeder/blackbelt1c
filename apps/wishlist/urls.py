from django.conf.urls import url
from views import users, users_w_id, new, destroy, add, remove


urlpatterns = [
    url(r'^$', users, name='index'),
    url(r'^new$', new, name='new'),
    url(r'^add(?P<item_id>\d+)$', add, name='add'),
    url(r'^remove(?P<item_id>\d+)$', remove, name='remove'),
    url(r'^(?P<id>\d+)/$', users_w_id),
    # url(r'^delete/(?P<item_id>\d+)$', destroy, name='destroy'),
    url(r'^(?P<id>\d+)/destroy/$', destroy, name='destroy'),
]
