from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from .forms import TicketCreateForm, TicketMessageForm
from .models import Ticket


# Create your views here.

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketCreateForm
    template_name = 'support/ticket_form.html'
    success_url = reverse_lazy('support:user_ticket_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your ticket has been created.')
        return super().form_valid(form)


class UserTicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'support/user_ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'support/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msgs'] = self.object.messages.all().order_by('created_at')
        context['form'] = TicketMessageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TicketMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.ticket = self.object
            message.save()
            messages.success(request, 'Your message has been sent.')
            return self.get(self, request, *args, **kwargs)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class ManageTicketListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ticket
    template_name = 'support/manage_ticket_list.html'
    context_object_name = 'tickets'

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Car manager', 'Admin']).exists()

    def get_queryset(self):
        return Ticket.objects.filter(status='open')


class TicketCloseView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Car manager', 'Admin']).exists()

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.status = 'closed'
        ticket.save()
        messages.success(request, "The ticket has been closed.")
        return redirect('support:ticket_detail', pk=pk)
