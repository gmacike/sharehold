from django.conf.urls import url
from circulation import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^customer/new/(?P<pk>None)?$', views.CustomerCreateView.as_view(), name='circulation_newcustomer'),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.CustomerUpdateView.as_view(), name='circulation_customeredit'),
    url(r'^customer/getByID/', views.get_customers_by_IDlabel, name='circulation_customergetbyid'),
    url(r'^customer/new/repeat_add_customer$', views.repeat_add_customer, name='repeat_add_customer'),
    url(r'^customerbyactiveidlabel-autocomp/$',views.CustomerAutocompleteViewByActiveIDlabel.as_view(),name='customerbyactiveidlabel-autocomplete'),
    url(r'^customer/(?P<pk>\d+)/lendings/$', views.CustomerLendingListView.as_view(), name='circulation_customerlendings'),


    url(r'^customerid/(?P<IDpk>\d+)/activate$', views.CustomerID_activate, name='customerID_activate'),
    url(r'^customerid/(?P<IDpk>\d+)/deactivate$', views.customerID_deactivate, name='customerID_deactivate'),
    url(r'^customerbyidlabel-autocomp/$',views.CustomerAutocompleteViewByIDlabel.as_view(),name='customerbyidlabel-autocomplete'),
    url(r'^returncustomerbynickorcustid-autocomp/$',views.ReturningCustomerAutocompleteViewByPseudo_ActiveID.as_view(),name='returncustomerbynickorcustid-autocomplete'),

    url(r'^circulation$', views.circulation_home, name='circulation_home'),
    url(r'^lending/new$', views.BoardGameLendingCreateView.as_view(success_url='/lending/new'),  name='circulation_lend'),
    url(r'^lending/return', views.BoardGameLendingReturnView.as_view(), name='circulation_return'),
    url(r'^lending/(?P<pk>\d+)/finish$', views.boardgamelending_finish, name='lending_finish'),
    url(r'^lending/(?P<pk>\d+)/return$', views.BoardGameLendingUpdateView.as_view(success_url='/lending/return'), name='lending_return'),
    url(r'^containertoreturn-autocomp/$',views.BoardGameContainerInWarehouseAutocompleteViewByNotReturnedLending.as_view(),name='containerbyunfinishedlendings-autocomplete'),
]
