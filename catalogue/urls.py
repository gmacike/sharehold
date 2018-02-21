from django.conf.urls import url
from catalogue import views

urlpatterns = [
    url(r'^$', views.CatalogueItemListView.as_view(), name='catalogue_entries'),
    url(r'^brdgm/(?P<pk>\d+)$', views.BoardGameDetailsView.as_view(), name='boardgame_detail'),
    url(r'^brdgm/new/$', views.BoardGameCreateView.as_view(), name='boardgame_new'),
    url(r'^brdgm/(?P<pk>\d+)/edit/$', views.BoardGameUpdateView.as_view(), name='boardgame_edit'),

    url(r'^warehouse$', views.WarehouseListView.as_view(), name='warehouse_index'),
    url(r'^warehouse/create$', views.WarehouseCreateView.as_view(success_url='/warehouse'), name='warehouse_create'),
    url(r'^warehouse/(?P<pk>\d+)$', views.WarehouseDetailView.as_view(), name='warehouse_detail'),

    url(r'container/create$', views.ContainerCreateView.as_view(success_url='/warehouse'), name='container_create')
]
