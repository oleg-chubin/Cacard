from django import forms
from models import Feed_back


class Feed_back(forms.ModelForm):

    class Meta:
        model = Feed_back
        fields = ["title", "message", "name", "e_mail"]
