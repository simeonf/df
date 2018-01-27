# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django import forms
from django.core.exceptions import ValidationError

from .forms import MultipleLongField, QuerySearchForm, clean_long


class TestFrm(forms.Form):
    f = MultipleLongField(required=False)

class FormTesting(TestCase):
    def testCleanLong(self):
        self.assertEquals(clean_long(1), long(1))
        with self.assertRaises(ValidationError):
            clean_long(['test'])
