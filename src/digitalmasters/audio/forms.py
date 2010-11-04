import mods
from django import forms
from django.conf import settings

from eulcore.django.forms import XmlObjectForm, SubformField, xmlobjectform_factory
from eulcore.django.forms.fields import W3CDateField

from digitalmasters import mods
from digitalmasters.audio.models import AudioMods
from digitalmasters.collection.models import CollectionObject

class UploadForm(forms.Form):
    label = forms.CharField(max_length=255, # fedora label maxes out at 255 characters
                help_text='Preliminary title for the object in Fedora. 255 characters max.')
    audio = forms.FileField(label="Audio file")
    
class UploadFormSingle(forms.Form):
    fileManualUpload = forms.FileField(label="Audio file")
    
def HTML5Upload():
    output = '<link rel="stylesheet" type="text/css" href="/static/HTML5/_styles.css" media="screen" />'
    output += '<div id="output" class="clearfix">'
    output += '<ul id="output-listing01"></ul>'
    output += '</div>'
    output += '<script type="text/javascript" src="/static/HTML5/prototype.js"></script>'
    output += '<script type="text/javascript" src="/static/HTML5/md5.js"></script>'
    output += '<script type="text/javascript" src="/static/HTML5/HTML5Upload.js"></script>'
    #Need to fix the hardcoding of "html5dropbox".
    output += '<br /><br /><input type="button" value="Ingest the above file(s)" id="btn_ingest" name="btn_ingest" onClick="html5dropbox.ingestWhenReady();"/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="button" value="Clear the above files" id="btn_clear" name="btn_clear" onClick="html5dropbox.clearAllDisplayed(); return false;" />'
    output += "<script>var html5dropbox = new HTML5DropBox('uploadForm','/audio/HTML5FileUpload','output');</script>"
    output += "<script>html5dropbox.setActionPage('/audio/HTML5FileUpload');</script>"
    output += '<script>html5dropbox.setAcceptedFileType("audio/*");</script>'
    output += '<script>html5dropbox.setAcceptedFileType("image/*");</script>'    
    
    return output
  

class SearchForm(forms.Form):
    pid = forms.CharField(required=False, help_text='Search by fedora pid.',
            initial='%s:' % settings.FEDORA_PIDSPACE)
    title = forms.CharField(required=False,
            help_text='Search for title word or phrase.  May contain wildcards * or ?.')


class SimpleNoteForm(XmlObjectForm):
    """Custom XmlObjectForm to simplify editing a MODS note.  Displays text content
    input only, as a textarea with no label; no other note attributes are displayed.
    """
    text = forms.CharField(label='', widget=forms.Textarea, required=False)
    class Meta:
        model = mods.Note
        fields = ['text']


class SimpleDateForm(XmlObjectForm):
    """Custom XmlObjectForm to edit a MODS date.  Currently only allows
    editing the date value itself, using a W3CDateField.
    """
    date = W3CDateField(label='', required=False)
    class Meta:
        model = mods.Date
        fields = ['date']


class OriginInfoForm(XmlObjectForm):
    """Custom XmlObjectForm to edit MODS originInfo.  Currently only consists
    of bare-minimum date entry for date created and issued.
    """
    # FIXME: need a way to limit these to one each! subformfield seems to want to repeat them!
    created = SubformField(formclass=xmlobjectform_factory(mods.DateCreated, form=SimpleDateForm))
    issued = SubformField(formclass=xmlobjectform_factory(mods.DateIssued, form=SimpleDateForm))
    class Meta:
        model = mods.OriginInfo


class EditForm(XmlObjectForm):
    # PLACEHOLDER: needs non-top-level collections here
    collection = forms.ChoiceField(label="Collection",
                    choices=[(o.uri, o.label) for o in CollectionObject.top_level()],
                    help_text="Collection this item belongs to.")
                    # using URI because it will be used to set a relation in RELS-EXT
                    
    # TODO: ARK will need to be set on form init from instance
    # read-only text input to display ARK (not editable)
    identifier = forms.CharField(label="Identifier", required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'long'}))
    origin_info = SubformField(formclass=OriginInfoForm)
    general_note = SubformField(formclass=SimpleNoteForm)
    part_note = SubformField(formclass=SimpleNoteForm)
    
    class Meta:
        model = AudioMods
        fields = (
            'collection', 'identifier', 'title', 
            'origin_info', 'general_note', 'part_note',
            )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'long'}),
            }