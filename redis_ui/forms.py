from django import forms


class SetForm(forms.Form):
    key = forms.CharField(max_length=200, required=True)
    value = forms.CharField(max_length=10_000, required=True, widget=forms.Textarea)
    ttl_seconds = forms.IntegerField(
        min_value=1,
        max_value=31_536_000,  # 1 year
        required=False,
        label="TTL (seconds) — optional",
    )


class QueryForm(forms.Form):
    key = forms.CharField(max_length=200, required=True)
    pattern = forms.CharField(
        max_length=200,
        required=False,
        initial="*",
        label="Key pattern (for browse)",
    )


class DeleteForm(forms.Form):
    key = forms.CharField(max_length=200, required=True)
    confirm = forms.BooleanField(required=True, label="Confirm deletion")