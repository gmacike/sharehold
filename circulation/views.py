from urllib.parse import urlencode

from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from dal import autocomplete
from django.forms import inlineformset_factory
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.conf import settings
from circulation.models import (Customer, CustomerID, BoardGameLending)
from warehouse.models import Warehouse, BoardGameContainer
from circulation.forms import (CustomerForm, BoardGameLendingForm, BoardGameReturnForm)
from sharehold.templatetags.anypermission import has_any_permission


@login_required
# @has_any_permission (('circulation.add_boardgamelending', 'circulation.change_boardgamelending',
#     'circulation.add_customer', 'circulation.change_customer'))
def circulation_home(request):
    if request.user.has_perm ('circulation.add_boardgamelending') or request.user.has_perm('circulation.change_boardgamelending'):
        return redirect('circulation_lend')
    if request.user.has_perm ('circulation.add_customer') or request.user.has_perm('circulation.change_customer'):
        return redirect('circulation_newcustomer')
    # if request.user.has_perm ('circulation.add_customerid'):
    #     return redirect('circulation_addcustomerid')
    # if request.user.has_perm('circulation.change_customerid'):
    #     # TODO implement view for changing idstatus only
    #     pass
    return redirect('welcome')


############################################
# customer Views
############################################
class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'circulation.add_customer'
    form_class = CustomerForm
    model = Customer


@login_required
@has_any_permission (('circulation.add_customerid', 'circulation.change_customerid',
    'circulation.add_customer', 'circulation.change_customer', 'circulation.change_boardgamelending',))
def get_customers_by_IDlabel (request):
    customers = Customer.objects.none()
    custpk = None
    if request.method == 'GET':
        if request.GET.__contains__("filter"):
            filter_criteria = request.GET.get("filter")
            # self.request.session ['catalogue_filter'] = filter_criteria
            # else:
            #     filter_criteria = self.request.session.get ('catalogue_filter', None)
            if filter_criteria != None:
                # expected one and only one Customer matching the criteria
                # TODO zrefaktoryzować, bo można jakoś inteligentniej poprzez get()
                customers = Customer.objects.filter(customerIDs__IDlabel__iexact=filter_criteria)
                if customers.count() == 1:
                    custpk = customers[0].pk
        if custpk == None:
            return redirect('circulation_newcustomer')
    return redirect('circulation_customeredit', pk = custpk)

class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.change_customer'
    raise_exception = True

    form_class = CustomerForm
    model = Customer

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance = Customer.objects.get(pk=kwargs['pk']))
        if form.is_valid():
            try:
                cust = form.save(commit=False)
                newID = form.cleaned_data['newCustomerID']
                if newID != "":
                    # create activates ID
                    custID = CustomerID.create (cust, newID)
                    custID.save()
                cust.save()
            except ValidationError as exc:
                form.add_error('newCustomerID', exc)
                return render(request, 'circulation/customer_form.html', {'form': form, 'customer': self.get_object,})
        else:
            # dupa=form.errors
            # dupa.blada
            return render(request, 'circulation/customer_form.html', {'form': form, 'customer': self.get_object,})
        return redirect(cust)


class CustomerAutocompleteViewByActiveIDlabel(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.add_boardgamelending'
    raise_exception = True

    def get_queryset(self):
        if self.q:
            qs = Customer.objects.filter(customerIDs__IDstatus=CustomerID.AKTYWNY, customerIDs__IDlabel__icontains=self.q).order_by('customerIDs__IDlabel')
        else:
            qs = Customer.objects.all().order_by('CustomerIDs__IDlabel')
        return qs



class CustomerAutocompleteViewByIDlabel(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.change_customer'
    raise_exception = True

    def get_queryset(self):
        qs = Customer.objects.all().order_by('CustomerIDs__IDlabel')
        if self.q:
            qs = qs.filter(CustomerIDs__IDlabel__icontains=self.q)
        return qs

@login_required
@permission_required ('circulation.change_customerid', raise_exception=True)
def CustomerID_activate (request, IDpk):
    try:
        custID = CustomerID.objects.get(pk=IDpk)
        custID.activate()
        # if no ValidationError raised
        custID.save()
    except CustomerID.DoesNotExist as exc:
        pass
    except ValidationError as exc:
        messages.info(request, 'Identyfikator nie może być aktywowany')
    return redirect('circulation_customeredit', pk = custID.customer.pk)

@login_required
@permission_required ('circulation.change_customerid', raise_exception=True)
def customerID_deactivate (request, IDpk):
    try:
        custID = CustomerID.objects.get(pk=IDpk)
        custID.deactivate()
        # if no ValidationError raised
        custID.save()
    except CustomerID.DoesNotExist as exc:
        pass
    except ValidationError as exc:
        messages.info(request, 'Identyfikator nie może być zablokowany')
    return redirect('circulation_customeredit', pk = custID.customer.pk)

@login_required
@permission_required('circulation.add_customer', raise_exception=True)
def repeat_add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cust = form.save()
            custID = CustomerID.objects.create (customer=cust, IDlabel=form.cleaned_data['newCustomerID'])
            custID.activate()
            # TODO: zarejestrować kto i kiedy
            # customer.save()
            custID.save()
        else:
            return render(request, 'circulation/customer_form.html', {'form': form})
    return redirect('circulation_newcustomer')

class CustomerLendingListView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, ListView):
    model = BoardGameLending
    permission_required = 'circulation.add_boardgamelending'
    raise_exception=True
    template_name = 'circulation/customerlending_list.html'
    paginate_by = settings.CIRCULATION_LENDING_PAGINATION
    paginate_orphans = settings.CIRCULATION_LENDING_PAGINATION_ORPHANS
    # ListView context object => list of warehouse containers
    # context_object_name = 'customer_lending_list'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Customer.objects.all())
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object
        return context

    def get_queryset(self):
        # qs will contain only returned lendings
        self.object = self.get_object(queryset=Customer.objects.all())
        self.queryset = BoardGameLending.objects.filter(customer=self.object).exclude(returned=None).order_by('-issued')
        return self.queryset

class BoardGameLendingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BoardGameLending
    permission_required = 'circulation.add_boardgamelending'
    raise_exception=True
    form_class = BoardGameLendingForm


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                lending = form.save(commit=False)
                lending.start()
                lending.save()
            except ValidationError as exc:
                dupa.blada
                form.add_error('newLending', exc)
                return render(request, 'circulation/boardgamelending_form.html', {'form': form,})
        else:
            # dupa = form.errors
            # dupa.blada
            return render(request, 'circulation/boardgamelending_form.html', {'form': form,})
        return redirect('circulation_lend')

class BoardGameLendingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BoardGameLending
    permission_required = 'circulation.change_boardgamelending'
    raise_exception=True
    form_class = BoardGameReturnForm
    template_name = 'circulation/boardgamereturn_form.html'

class BoardGameLendingReturnView(LoginRequiredMixin, PermissionRequiredMixin, FormMixin, ListView):
    model = BoardGameLending
    permission_required = 'circulation.change_boardgamelending'
    raise_exception=True
    form_class = BoardGameReturnForm
    template_name = 'circulation/boardgamereturn_form.html'
    # context_object_name = 'lending'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        lending = None
        if form.is_valid():
            try:
                cust = form.cleaned_data['customer']
                container = form.cleaned_data['container']
                lending = BoardGameLending.objects.get(customer=cust, container=container)
            except BoardGameLending.DoesNotExist as exc:
                form.add_error('lending', exc)
                return render(request, 'circulation/boardgamereturn_form.html', {'form': form,})
        else:
            return render(request, 'circulation/boardgamereturn_form.html', {'form': form,})
        return redirect('lending_return', pk=lending.pk)



# Old view based with form starting from customer ID
# class BoardGameLendingReturnByCustomerIDView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = BoardGameLending
#     permission_required = 'circulation.change_boardgamelending'
#     raise_exception=True
#     template_name = 'circulation/boardgamelending_return.html'
#
#     customer = None
#
#     def get_context_data(self, **kwargs):
#         if self.request.method == 'GET':
#             filter_criteria = self.request.GET.get("filter", None)
#         if filter_criteria == None:
#             self.customer = None
#         else:
#             try:
#                 self.customer = Customer.get_by_IDlabel (filter_criteria)
#             except Customer.DoesNotExist as exc:
#                 self.customer = None
#             except Customer.MultipleObjectsReturned as exc:
#                 self.customer = None
#         context = super().get_context_data(**kwargs)
#         context['customer'] = self.customer
#         qs = self.get_queryset()
#         context['object_list'] = qs
#         context['boardgamelending_list'] = qs
#         return context
#
#     def get_queryset(self):
#         if self.request.method == 'GET':
#             if self.customer == None:
#                 return BoardGameLending.objects.none()
#             else:
#                 return self.customer.get_unfinished_lendings()
#         else:
#             return BoardGameLending.objects.none()

@login_required
@permission_required ('circulation.change_boardgamelending', raise_exception=True)
def boardgamelending_finish (request, pk):
    try:
        lending = BoardGameLending.objects.get(pk=pk)
        lending.finish()
        # if no ValidationError raised
        lending.save()
    except BoardGameLending.DoesNotExist as exc:
        messages.error(request, 'Błąd odczytu wypożyczenia')
    except ValidationError as exc:
        messages.info(request, exc.messages)
    return redirect('circulation_return')

class BoardGameContainerInWarehouseAutocompleteViewByNotReturnedLending(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.change_boardgamelending'
    raise_exception=True
    # these queryset data will be available through pulib url guard w/ permissions if necessary
    # here are none as boardgame cataloge is going to be available for publicity

    def get_queryset(self):
        selected_warehouse = None
        warehouse_pk = None

        # find out which warehouse is subject to search
        if self.request.method == 'GET':
            if self.request.GET.__contains__("wrhpk"):
                warehouse_pk = self.request.GET.get("wrhpk")
            else:
                warehouse_pk = self.request.session.get('warehouse_context_pk', None)

        if warehouse_pk != None:
            try:
                selected_warehouse = Warehouse.objects.get (pk=warehouse_pk)
            except Warehouse.DoesNotExist as exc:
                messages.add_message(request, messages.ERROR, exc)
                raise Http404

            # find unfinished lending bound to forwarded customer if given
            cust = None
            try:
                cust = Customer.objects.get(pk=self.forwarded.get('customer', None))
            except Customer.DoesNotExist as exc:
                pass
            except ValueError as exc:
                pass
            if cust != None:
                unfinished_lendings = BoardGameLending.objects.filter(returned=None, container__warehouse=selected_warehouse,
                    customer=cust)
            else:
                unfinished_lendings = BoardGameLending.objects.filter(returned=None, container__warehouse=selected_warehouse)

            # find containers matching by commodity code OR catalogue entry label
            if self.q:
                containers_by_codeValue = BoardGameContainer.objects.filter(warehouse=selected_warehouse, lendings__in=unfinished_lendings,
                    commodity__codeValue__icontains=self.q).order_by('commodity__codeValue')
                containers_by_catalogueEntry_label = BoardGameContainer.objects.filter(warehouse=selected_warehouse, lendings__in=unfinished_lendings,
                    commodity__catalogueEntry__itemLabel__icontains=self.q).order_by('commodity__catalogueEntry__itemLabel')
                qs = containers_by_codeValue | containers_by_catalogueEntry_label
            else:
                qs = BoardGameContainer.objects.filter(warehouse=selected_warehouse, lendings__in=unfinished_lendings).order_by('commodity__codeValue')

        else:
            qs = BoardGameContainer.objects.none()

        return qs.distinct()

class ReturningCustomerAutocompleteViewByPseudo_ActiveID(LoginRequiredMixin, PermissionRequiredMixin, autocomplete.Select2QuerySetView):
    permission_required = 'circulation.change_boardgamelending'
    raise_exception=True
    # these queryset data will be available through pulib url guard w/ permissions if necessary
    # here are none as boardgame cataloge is going to be available for publicity

    def get_queryset(self):
        selected_warehouse = None
        warehouse_pk = None

        # find out which warehouse is subject to search
        if self.request.method == 'GET':
            if self.request.GET.__contains__("wrhpk"):
                warehouse_pk = self.request.GET.get("wrhpk")
            else:
                warehouse_pk = self.request.session.get('warehouse_context_pk', None)

        if warehouse_pk != None:
            try:
                selected_warehouse = Warehouse.objects.get (pk=warehouse_pk)
            except Warehouse.DoesNotExist as exc:
                messages.add_message(request, messages.ERROR, exc)
                raise Http404

        # find unfinished lending bound to forwarded container if given
        container = None
        try:
            container = BoardGameContainer.objects.get(pk=self.forwarded.get('container', None))
        except BoardGameContainer.DoesNotExist as exc:
            pass
        except ValueError as exc:
            pass
        # raise ArithmeticError (container)
        if container != None:
            unfinished_lendings = BoardGameLending.objects.filter(returned=None, container=container)
        else:
            unfinished_lendings = BoardGameLending.objects.filter(returned=None, container__warehouse=selected_warehouse)

        # find containers matching by commodity code OR catalogue entry label
        if self.q:
            customers_by_active_custID = Customer.get_matching_IDlabel(self.q, True)
            customers_by_nick = Customer.get_matching_nick(self.q, True)

            qs = customers_by_active_custID | customers_by_nick
            qs = qs.filter(lendings__in=unfinished_lendings).order_by("nick")
        else:
            qs = Customer.objects.filter(lendings__in=unfinished_lendings)
        return qs.distinct()
