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


class RedisDataForm(forms.Form):
    balance_cash = forms.IntegerField(label="Balance cash 💷",
      widget=forms.TextInput(attrs={"Balance cash 💷": "Enter an integer"}),
      required=False)

    balance_digital = forms.IntegerField(label="Balance digital 🏧",
      widget=forms.TextInput(attrs={"Balance digital 🏧": "Enter an integer"}),
      required=False)

    balance_credit = forms.IntegerField(label="Balance credit 💳",
      widget=forms.TextInput(attrs={"Balance credit 💳": "Enter an integer"}),
      required=False)

    necessity = forms.IntegerField(label="Necessity ",
      widget=forms.TextInput(attrs={"Necessity ": "Enter an integer"}),
      required=False)
