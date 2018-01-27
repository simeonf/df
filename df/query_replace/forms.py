import json

from django import forms
from django.core.exceptions import ValidationError

from .models import SearchDetail


def clean_long(x):
    try:
        return long(x)
    except (ValueError, TypeError) as e:
        raise ValidationError("Cannot convert to long: {}".format(repr(x)))



class MultipleLongField(forms.Field):
    """A Field that accepts a list of ints and serializes/deserializes to json."""
    widget = forms.TextInput

    def prepare_value(self, value):
        if not value:
            value = json.dumps({'value': []})
        return value

    def clean(self, value):
        if value:
            value = json.loads(value)['value']
        else:
            value = []
        return map(clean_long, value)


class QuerySearchForm(forms.Form):
    "Show search/replace UI and keep state with moving through records."""

    # Visible fields users enter
    search = forms.CharField(max_length=100)
    replace = forms.CharField(max_length=100)

    # Submit button taking the next action (start, skip, replace)
    next = forms.CharField(max_length=50)

    # Hidden fields used for book-keeping
    skip = MultipleLongField(required=False)
    current_pk = forms.CharField(max_length=50, required=False)

    def update(self, pk):
        """Edit form data.

        Since two of the fields are just used to persist a list of records through a cycle of POSTs
        and aren't actually edited on the page we need to mutate self.data
        """

        data = self.data.copy()
        data['current_pk'] = pk
        if data.get('skip'):
          skip = json.loads(data['skip'])
          skip['value'].append(pk)
        else:
          skip = {'value': [pk]}
        data['skip'] = json.dumps(skip)
        self.data = data


class ChooseFieldForm(forms.Form):
    "Show configured searches and choose one."""
    sd = forms.ModelChoiceField(queryset=SearchDetail.objects.all(), required=True)
