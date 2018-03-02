from django.conf.urls import url

from warehouse import views

urlpatterns = [
    url(r'^warehouse$', views.WarehouseListView.as_view(), name='warehouse_index'),
    url(r'^warehouse/create$', views.WarehouseCreateView.as_view(success_url='/warehouse'), name='warehouse_create'),
    url(r'^warehouse/(?P<pk>\d+)$', views.WarehouseDetailView.as_view(), name='warehouse_detail'),

    url(r'container/create$', views.BoardGameContainerCreateView.as_view(success_url='/warehouse'), name='container_create')
]
