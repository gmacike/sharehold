from django.conf.urls import url
from circulation import views

urlpatterns = [
    # client links
    url(r'^rClient/$', views.RentalClientListView.as_view(), name='circulation_entries'),
    url(r'^rClient/new/$', views.RentalClientCreateView.as_view(), name='rentalClient_new'),
    url(r'^rClient/(?P<pk>\d+)/edit/$', views.ClientUpdateView.as_view(), name='rentalclient_edit'),
    url(r'^rClient/new/return_rentalClientList', views.addAndReturn_rentalClientList, name='return_rentalClientList'),
    url(r'^rClient/new/return_newRentalClient', views.addAndReturn_rentalClientList, name='return_newRentalClient'),
    url(r'^rClient/(?P<pk>\d+)/edit/return_rentalClientList', views.updateAndReturn_rentalClientList, name='return_rentalClientList'),

    url(r'^rental$',
        views.ClientHasBoardGameList.as_view(),
        name='clienthasboardgame_list'),
    url(r'^rental/new$',
        views.ClientHasBoardGameCreateView.as_view(success_url='/rental'),
        name='clienthasboardgame_create'),
]
