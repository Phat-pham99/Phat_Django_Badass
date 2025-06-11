from django import forms

class DateFilterForm(forms.Form):
    start_date = forms.DateField(label="Start date",
                    help_text="Select a start date for the filter",
                    widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="End date",
                    help_text="Select an end date for the filter",
                    widget=forms.DateInput(attrs={'type': 'date'}))