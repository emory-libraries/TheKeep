from django import forms
from django.conf import settings

from eulcore.django.forms import XmlObjectForm

from digitalmasters import mods

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


class EditForm(XmlObjectForm):
    class Meta:
        model = mods.MODS
        fields = [
            'title', 'resource_type', 'note',
            'origin_info.created.date', 'origin_info.created.key_date',
            ]

        widgets = {
            'note' : {'text': forms.Textarea },
            'origin_info' : { 'created' : { 'date': forms.DateInput }}
            }