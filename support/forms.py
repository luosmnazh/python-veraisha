from django import forms

from support.models import Ticket, TicketMessage


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title']


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your message...'}),
        }