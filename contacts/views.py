from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import F, Case, When, BooleanField, Q

from .models import Contact

from contacts.models import Contact



# Create your views here.
class ContactListView(generic.ListView):
    model = Contact
    paginate_by = 5
    
    def get_queryset(self):
        qs = Contact.objects.annotate(
            is_favorite=Case(
                When(favorito=True, then=1),
                When(favorito=False, then=0),
                output_field=BooleanField()
            )
        ).order_by('-favorito', 'name')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        return context

class ContactCreateView(generic.CreateView):
    model = Contact
    fields = ('avatar','name','email','birth','phone',)
    success_url = reverse_lazy('contact_list')

class ContactUpdateView(generic.UpdateView):
    model = Contact
    fields = ('avatar','name','email','birth','phone',)
    success_url = reverse_lazy('contact_list')

class ContactDeleteView(generic.DeleteView):
    model = Contact
    success_url = reverse_lazy('contact_list')

class ContactDetailView(generic.DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
class ContactToggleFavoriteView(View):
    def get(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.favorito = not contact.favorito
        contact.save()
        return redirect('contact_list')