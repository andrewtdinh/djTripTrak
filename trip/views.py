from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.urls import reverse_lazy

from .models import Trip, Note

# Create your views here.
class HomeView(TemplateView):
    template_name = 'trip/index.html'


def trips_list(request):
    trips = Trip.objects.filter(owner=request.user)
    context = {
        'trips': trips,
    }
    return render(request, 'trip/trips_list.html', context)

class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trips-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # It automatically looks for template named mode_form.html
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class TripDetailView(DetailView):
    model = Trip

    # right now we only details on the Trip and not the Notes, so we need the Notes data
    # get_context_data is already defined, but, it won't have the Notes data
    def get_context_data(self, **kwargs):
        # Get context about the trip
        context = super().get_context_data(**kwargs)
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes
        return context
    
class NoteDetailView(DetailView):
    model = Note

class NoteListView(ListView):
    model = Note
    # override get_queryset from ListView
    def get_queryset(self):
        queryset = Note.objects.filter(trip__owner=self.request.user)
        return queryset




