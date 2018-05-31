from django.conf.urls import url
from catalogue import views

urlpatterns = [
    url(r'^brdgm/$', views.CatalogueItemListView.as_view(), name='catalogue_entries'),
    url(r'^brdgm-autocomp/$', views.BoardGameAutocompleteView.as_view(), name='boardgame-autocomplete'),
    url(r'^brdgm/(?P<pk>\d+)$', views.BoardGameItemDetailsView.as_view(), name='boardgame_detail'),
    url(r'^brdgm/new/$', views.BoardGameItemCreateView.as_view(), name='boardgame_new'),
    url(r'^brdgm/new/repeat_add_boardgame', views.repeat_add_boardgame, name='boardgame_repeat_new'),
    url(r'^brdgm/new/boardgamelist_return', views.boardgamelist_return, name='boardgamelist_return'),
    url(r'^brdgm/new/return_home', views.return_home, name='return_home'),
    url(r'^brdgm/(?P<pk>\d+)/edit/$', views.BoardGameItemUpdateView.as_view(), name='boardgame_edit'),
    url(r'^brdgmed/new/$', views.BoardGameCommodityCreateView.as_view(), name='boardgame_new_edition'),
    url(r'^brdgmed/new/(?P<bgpk>\d+)$', views.BoardGameCommodityCreateView.as_view(), name='boardgame_new_edition'),
    url(r'^brdgmed/(?P<pk>\d+)/edit/$', views.BoardGameCommodityUpdateView.as_view(), name='boardgame_edition_edit'),
    url(r'^brdgm-commnotinwrhs-autocomp/$', views.BoardGameCommodityNotInWarehouseAutocompleteViewByCode.as_view(), name='commodity-notinwarehouse-autocomplete'),
    url(r'^brdgmed/new/return_home', views.return_home, name='return_home'),
]
