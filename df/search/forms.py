from itertools import tee
from django import forms
from django.core.validators import RegexValidator

empty_choice = [('', '')] 
overall_choices = empty_choice + zip(*tee('ABCDF'))
modifier_choices = [('>=', 'Or Better'), ('=', 'Exactly'), ('<=', 'Or worse')]
modifier_choices_wider = [('>=', 'Or Wider'), ('=', 'Exactly'), ('<=', 'Or narrower')]

def stars(num):
  if num == 0:
    return "No stars"
  num = list("{:02}".format(num))
  return "*" * int(num[0]) + ("" if num[1] == '0' else "1/2")
  
star_choices = empty_choice + [("{:02}".format(num), stars(num)) for num in range(40, -1, -5)]
moral_choices = range(4, -5, -1)

def add_plus(n):
  return "+%s" % n if n > 0 else str(n)
  
moral_choices = empty_choice + [(n, add_plus(n)) for n in moral_choices]
age_choices = empty_choice + [('K', 'Kids & up'), ('T', 'Teens & up'), ('A', 'Adults'), ('Z', 'No one')]
mpaa_choices = empty_choice + zip(*tee(['G', 'PG', 'PG-13', 'R', 'NR']))
usccb_choices = empty_choice + zip(*tee(['A-I', 'A-II', 'A-III', 'O', 'NR']))

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'expand'}), required=False)
    keywords = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'expand'}), required=False)
    cast = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'expand'}), required=False)
    year_from = forms.CharField(max_length=4,
                                validators=[RegexValidator(r'\d{4}', "Enter a 4 digit year")],
                                widget=forms.TextInput(attrs={'size': '4'}),
                                required=False)
    year_to = forms.CharField(max_length=4,
                              validators=[RegexValidator(r'\d{4}', "Enter a 4 digit year")],
                              widget=forms.TextInput(attrs={'size': '4'}),
                              required=False)
    genre = forms.MultipleChoiceField(choices=[], widget=forms.SelectMultiple(attrs={'size': '8'}), required=False)
    label = forms.MultipleChoiceField(choices=[], widget=forms.SelectMultiple(attrs={'size': '8'}), required=False)
    overall = forms.ChoiceField(choices=overall_choices, required=False)
    overall_modifier = forms.ChoiceField(choices=modifier_choices, required=False)
    artistic = forms.ChoiceField(choices=star_choices, required=False)
    artistic_modifier = forms.ChoiceField(choices=modifier_choices, required=False)
    moral = forms.ChoiceField(choices=moral_choices, required=False)
    moral_modifier = forms.ChoiceField(choices=modifier_choices, required=False)
    age = forms.ChoiceField(choices=age_choices, required=False)
    age_modifier = forms.ChoiceField(choices=modifier_choices_wider, required=False, initial="=")
    mpaa = forms.ChoiceField(choices=mpaa_choices, required=False)
    mpaa_modifier = forms.ChoiceField(choices=modifier_choices_wider, required=False, initial="=")
    usccb = forms.ChoiceField(choices=usccb_choices, required=False)
    usccb_modifier = forms.ChoiceField(choices=modifier_choices_wider, required=False, initial="=")
    
