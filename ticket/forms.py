from django import forms
from .models import Ticket


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'text', 'attachment']

    def save(self, client):
        instance = super(TicketCreateForm, self).save(commit=False)
        instance.sender = client
        return instance.save()

