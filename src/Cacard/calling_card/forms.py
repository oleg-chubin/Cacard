from django import forms
from models import ConsumerFeedback
from models import Translation
from django.core.exceptions import ValidationError


class ConsumerFeedback(forms.ModelForm):

    class Meta:
        model = ConsumerFeedback
        fields = ["title", "message", "name", "e_mail"]


class Translation(forms.ModelForm):

    class Meta:
        model = Translation

    def clean_short_description(self):
        data = self.cleaned_data['short_description']
        if len(data.split(' ')) > 5:
            raise forms.ValidationError('Too long')
        return data
