from django.conf.urls import url
from circulation import views
from django.conf.urls.static import static

urlpatterns = [
    # customer links
    # url(r'^Customer/$', views.CustomerListView.as_view(), name='circulation_newcustomer'),
    url(r'^customer/new/(?P<pk>None)?$', views.CustomerCreateView.as_view(), name='circulation_newcustomer'),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.CustomerUpdateView.as_view(), name='circulation_customeredit'),
    url(r'^customer/getByID/', views.get_customer_by_IDlabel, name='circulation_customergetbyid'),
    # url(r'^Customer/(?P<pk>\d+)/details/$', views.manage_Customer, name='circulation_customerdetails'),
    # url(r'^Customer/new/return_CustomerList', views.addAndReturn_CustomerList, name='return_CustomerList'),
    # url(r'^Customer/new/return_newCustomer', views.addAndAddNew_CustomerList, name='return_newCustomer'),
    url(r'^customer/new/repeat_add_customer$', views.repeat_add_customer, name='repeat_add_customer'),
    url(r'^customerid/(?P<IDpk>\d+)/activate$', views.CustomerID_activate, name='customerID_activate'),
    url(r'^customerid/(?P<IDpk>\d+)/deactivate$', views.customerID_deactivate, name='customerID_deactivate'),
    # url(r'^Customer/(?P<pk>\d+)/edit/return_CustomerList', views.updateAndReturn_CustomerList, name='return_CustomerList'),
    url(r'^customerbyidlabel-autocomp/$',views.CustomerAutocompleteViewByIDlabel.as_view(),name='customerbyidlabel-autocomplete'),
    url(r'^customerbyactiveidlabel-autocomp/$',views.CustomerAutocompleteViewByActiveIDlabel.as_view(),name='customerbyactiveidlabel-autocomplete'),
    url(r'^containerbycommodity-autocomp/$',views.BoardGameContainerInWarehouseAutocompleteViewByCommodity.as_view(),name='containerbycommodity-autocomplete'),

    url(r'^lending$', views.circulation_home, name='circulation_home'),
    url(r'^lending/new$', views.BoardGameLendingCreateView.as_view(success_url='/lending/new'),  name='circulation_lend'),
    # url(r'^lending/(?P<pk>\d+)$', views.BoardGameLendingDetailView.as_view(), name='BoardGameLending_detail'),
    url(r'^lending/(?P<pk>\d+)/return', views.register_return, name='circulation_return'),
]
