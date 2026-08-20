from typing_extensions import final
from django import forms


@final
class DateFilterForm(forms.Form):
    start_date = forms.DateField(
        label="Start date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    end_date = forms.DateField(
        label="End date", widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

