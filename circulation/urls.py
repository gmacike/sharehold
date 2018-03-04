from django.conf.urls import url
from circulation import views

urlpatterns = [
    # client links
    url(r'^rClient/$', views.RentalClientListView.as_view(), name='circulation_entries'),
    url(r'^rClient/new/$', views.RentalClientCreateView.as_view(), name='rentalClient_new'),
    url(r'^rClient/(?P<pk>\d+)/edit/$', views.BoardGameUpdateView.as_view(), name='rentalclient_edit'),
    url(r'^rClient/new/return_rentalClientList', views.rentalClientList_return, name='return_rentalClientList'),
]
