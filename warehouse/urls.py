from django.conf.urls import url

from warehouse import views

urlpatterns = [
    url(r'^warehouse$',
        views.WarehouseListView.as_view(),
        name='warehouse_index'),

    url(r'^warehouse/create$',
        views.WarehouseCreateView.as_view(success_url='/warehouse'),
        name='warehouse_create'),

    url(r'^warehouse/inv/(?P<pk>\d+)*$',
        views.WarehouseDetailView.as_view(),
        name='warehouse_inventory'),

    url(r'warehouse/(?P<pk>\d+)/add_boardgame$',
        views.BoardGameContainerCreateView.as_view(),
        name='container_create'),


]
