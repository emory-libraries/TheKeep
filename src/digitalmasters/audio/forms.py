from django import forms
from django.conf import settings

from eulcore.django.forms import XmlObjectForm

from digitalmasters.audio.models import Mods

class UploadForm(forms.Form):
    label = forms.CharField(max_length=255, # fedora label maxes out at 255 characters
                help_text='Preliminary title for the object in Fedora. 255 characters max.')
    audio = forms.FileField(label="Audio file")

class SearchForm(forms.Form):
    pid = forms.CharField(required=False, help_text='Search by fedora pid.',
            initial='%s:' % settings.FEDORA_PIDSPACE)
    title = forms.CharField(required=False,
            help_text='Search for title word or phrase.  May contain wildcards * or ?.')

class EditForm(XmlObjectForm):
    class Meta:
        model = Mods
        widgets = {
            'note' : {'text': forms.Textarea },
            'origin_info' : { 'created': {'value': forms.DateInput }}
            }