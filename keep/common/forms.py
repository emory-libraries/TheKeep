from django import forms

class ReadonlyTextInput(forms.TextInput):
    'Read-only variation on :class:`django.forms.TextInput`'
    readonly_attrs = {
        'readonly': 'readonly',
        'class': 'readonly long',
        'tabindex': '-1',
    }
    def __init__(self, attrs=None):
        if attrs is not None:
            self.readonly_attrs.update(attrs)
        super(ReadonlyTextInput, self).__init__(attrs=self.readonly_attrs)
