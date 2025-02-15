from django import forms
from .models import Inbox
from django.contrib.auth.models import User

class InboxForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        model = Inbox
        fields = ['receiver', 'subject', 'message']  # Ensure receiver is included
