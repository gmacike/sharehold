from django.conf.urls import url

from warehouse import views

urlpatterns = [
    url(r'^warehouse$',
        views.WarehouseListView.as_view(),
        name='warehouse_index'),

    url(r'^warehouse-autocomp/$',
        views.WarehouseAutocompleteView.as_view(),
        name='warehouse-autocomplete'),


    url(r'^warehouse/select/(?P<wrhpk>\d+)$',
        views.warehouse_select,
        name='warehouse_select'),

    url(r'^warehouse/create$',
        views.WarehouseCreateView.as_view(success_url='/warehouse'),
        name='warehouse_create'),

    url(r'^warehouse/inv/(?P<pk>\d+)*$',
        views.WarehouseDetailView.as_view(),
        name='warehouse_inventory'),

    url(r'warehouse/(?P<pk>\d+)/add_boardgame$',
        views.BoardGameContainerCreateView.as_view(),
        name='container_create'),

    url(r'warehouse/bgcnt/(?P<cntpk>\d+)/inc$',
        views.bgcontainer_inc,
        name='bgcontainer_inc'),

    url(r'warehouse/bgcnt/(?P<cntpk>\d+)/dec$',
        views.bgcontainer_dec,
        name='bgcontainer_dec'),
]
