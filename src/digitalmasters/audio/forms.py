from django import forms

class UploadForm(forms.Form):
    label = forms.CharField(max_length=255, # fedora label maxes out at 255 characters
                help_text='Preliminary title for the object in Fedora. 255 characters max.')
    audio = forms.FileField(label="Audio file")