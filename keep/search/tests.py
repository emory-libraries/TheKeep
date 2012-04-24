from django import forms
from django.test import TestCase

from keep.search.forms import SolrSearchField


class SolrSearchFieldTest(TestCase):

    def setUp(self):
        self.field = SolrSearchField(required=True)

    def test_to_python(self):
        self.assert_(isinstance(self.field.to_python(''), list),
                     'to python should return a list, even for an empty value')
        self.assert_(isinstance(self.field.to_python('one two three'), list),
                     'to python should return a list')

    def test_validate(self):
        # inherited validation - required field error
        self.assertRaises(forms.ValidationError,
                          self.field.validate, [])

        # when not required: empty should be valid
        not_req = SolrSearchField(required=False)
        not_req.validate([])

        # no validation error should be raised 
        self.field.validate(['one', 'two'])
        self.field.validate(['one', 'two', '"three four"'])
        self.field.validate(['one', 'two', '"three *four"'])

        # validation errors should be raised
        self.assertRaises(forms.ValidationError,
                          self.field.validate, ['*foo'])
        self.assertRaises(forms.ValidationError,
                          self.field.validate, ['foo', '*bar'])
        self.assertRaises(forms.ValidationError,
                          self.field.validate, ['"foo bar"', '*baz'])
