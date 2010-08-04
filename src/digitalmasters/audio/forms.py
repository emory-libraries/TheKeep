from django import forms
from django.conf import settings

from eulcore.django.forms import XmlObjectForm

from digitalmasters.audio.models import Mods, CollectionMods, ModsDate, CollectionObject

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
        fields = [
            'title', 'resource_type', 'note',
            # NOTE: disabled because created is now a list field - not yet supported
            #'origin_info.created.date', 'origin_info.created.key_date',
            ]

        widgets = {
            'note' : {'text': forms.Textarea },
            #'origin_info' : { 'created' : { 'date': forms.DateInput }}
            }

class CollectionForm(XmlObjectForm):
    # NOTE: this only sets choices on load time
    # TODO: would be nice to have an ObjectChoiceField analogous to django's ModelChoiceField
    collection = forms.ChoiceField(label="Collection",
                    choices=[(o.pid, o.label) for o in CollectionObject.top_level()] )
    date_created = forms.CharField(help_text="Date created, or start date for a date range.")
    date_end = forms.CharField(help_text="End date for a date range. Leave blank if not a range.",
                                required=False)
    class Meta:
        model = CollectionMods
        fields = [
            'source_id', 'title', 'resource_type',
            # TODO: name
            'restrictions_on_access.text', 'use_and_reproduction.text',
            ]
        widgets = {
            'restrictions_on_access' : {'text': forms.Textarea },
            'use_and_reproduction' : {'text': forms.Textarea }
            }


    def update_instance(self):
        # override default update for additional logic
        super(CollectionForm, self).update_instance()

        # set date created - could be a single date or a date range
        if len(self.instance.origin_info.created) == 0:
            self.instance.origin_info.created.insert(0, ModsDate())
        self.instance.origin_info.created[0].date = self.cleaned_data['date_created']
        self.instance.origin_info.created[0].key_date = True
        if 'date_end' in self.cleaned_data and self.cleaned_data['date_end']:
            if len(self.instance.origin_info.created) == 1:
                self.instance.origin_info.created.insert(1, ModsDate())            
            self.instance.origin_info.created[1].date = self.cleaned_data['date_end']
            self.instance.origin_info.created[1].point = 'end'
            self.instance.origin_info.created[0].point = 'start'

        # NOTE: parent collection - not part of the MODS
        # will have to be set in the view?

        return self.instance