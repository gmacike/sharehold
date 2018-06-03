from django.conf.urls import url
from circulation import views
from django.conf.urls.static import static

urlpatterns = [
    # client links
    url(r'^rClient/$', views.RentalClientListView.as_view(), name='circulation_entries'),
    url(r'^rClient/new/$', views.RentalClientCreateView.as_view(), name='rentalClient_new'),
    url(r'^rClient/(?P<pk>\d+)/edit/$', views.ClientUpdateView.as_view(), name='rentalclient_edit'),
    url(r'^rClient/(?P<pk>\d+)/details/$', views.manage_rentalclient, name='rentalclient_details'),
    url(r'^rClient/new/return_rentalClientList', views.addAndReturn_rentalClientList, name='return_rentalClientList'),
    url(r'^rClient/new/return_newRentalClient', views.addAndAddNew_rentalClientList, name='return_newRentalClient'),
    url(r'^rClient/new/return_editRentalClient', views.addAndEditRentalClient, name='return_editRentalClient'),
    url(r'^rClient/(?P<pk>\d+)/edit/return_rentalClientList', views.updateAndReturn_rentalClientList, name='return_rentalClientList'),
    url(r'^clientbyidlabel-autocomp/$',views.ClientAutocompleteViewByIDlabel.as_view(),name='clientbyidlabel-autocomplete'),
    url(r'^containerbycommodity-autocomp/$',views.BoardGameContainerInWarehouseAutocompleteViewByCommodity.as_view(),name='containerbycommodity-autocomplete'),

    url(r'^lending$',
        views.BoardGameLendingList.as_view(),
        name='BoardGameLending_list'),
    url(r'^lending/new$',
        views.BoardGameLendingCreateView.as_view(success_url='/lending/new'),
        name='BoardGameLending_create'),
    url(r'^lending/(?P<pk>\d+)$',
        views.BoardGameLendingDetailView.as_view(),
        name='BoardGameLending_detail'),
    url(r'^lending/(?P<pk>\d+)/return',
        views.register_return,
        name='BoardGameLending_return'),
]
