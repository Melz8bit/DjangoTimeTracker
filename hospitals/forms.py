from django import forms
from .models import Hospital

class HospitalModelForm(forms.ModelForm):
    class Meta:
        email = forms.EmailField(required=False)

        model = Hospital
        fields = [
            'name',
            'address',
            'city',
            'state',
            'zip_code',
            'email',
            'telephone',
        ]