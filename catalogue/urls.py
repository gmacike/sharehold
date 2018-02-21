from django.conf.urls import url
from catalogue import views

urlpatterns = [
    url(r'^$', views.CatalogueItemListView.as_view(), name='catalogue_entries'),
    url(r'^brdgm/(?P<pk>\d+)$', views.BoardGameDetailsView.as_view(), name='boardgame_detail'),
    url(r'^brdgm/new/$', views.BoardGameCreateView.as_view(), name='boardgame_new'),
    url(r'^brdgm/new/repeat_add_boardgame', views.repeat_add_boardgame, name='boardgame_repeat_new'),
    url(r'^brdgm/new/boardgamelist_return', views.boardgamelist_return, name='boardgamelist_return'),
    url(r'^brdgm/(?P<pk>\d+)/edit/$', views.BoardGameUpdateView.as_view(), name='boardgame_edit'),
    # client links
    url(r'^rClient/new/$', views.RentalClientCreateView.as_view(), name='rentalClient_new'),
]
