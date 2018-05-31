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

    url(r'^rental$',
        views.BoardGameLendingList.as_view(),
        name='BoardGameLending_list'),
    url(r'^rental/new$',
        views.BoardGameLendingCreateView.as_view(success_url='/rental'),
        name='BoardGameLending_create'),
    url(r'^rental/(?P<pk>\d+)$',
        views.BoardGameLendingDetailView.as_view(),
        name='BoardGameLending_detail'),
    url(r'^rental/(?P<pk>\d+)/return',
        views.register_return,
        name='BoardGameLending_return'),
]
