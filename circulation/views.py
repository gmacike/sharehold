from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from circulation.models import (RentalClient)
from circulation.forms import (RentalClientForm)
from django.views.generic import (ListView,DetailView,CreateView, UpdateView)

############################################
# Client Views
############################################
class RentalClientListView(ListView):
    model = RentalClient

    def get_queryset(self):
        if self.request.method == 'GET':
            self.filter_criteria = self.request.GET.get("filter")
            if self.filter_criteria:
                search_type = self.request.GET.get("search")
                if search_type == "identificationCode":
                    return RentalClient.objects.filter(identificationCode__startswith=self.filter_criteria).order_by("identificationCode")
                elif search_type == "initials":
                    return RentalClient.objects.filter(initials__icontains=self.filter_criteria).order_by("initials")
        return RentalClient.objects.none()
        
class RentalClientDetailsView(DetailView):
    model = RentalClient
     
class RentalClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'circulation.RentalClient.add_rentalclient'
    form_class = RentalClientForm
    model = RentalClient
	
class BoardGameUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'circulation.RentalClient.change_rentalclient'
    raise_exception=True

    form_class = RentalClientForm
    model = RentalClient
	
@login_required
@permission_required('circulation.RentalClient.add_rentalclient', raise_exception=True)
def return_home (request):
    if request.method == 'POST':
        form = RentalClientForm(request.POST)
        if form.is_valid():
            boardgame = form.save(commit=False)
            boardgame.save()
    return redirect('welcome')