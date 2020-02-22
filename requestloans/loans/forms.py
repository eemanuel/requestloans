from django.forms import BooleanField, CharField, Form, ModelForm

from .models import Loan


class LoanForm(ModelForm):
    dni = CharField(min_length=7, max_length=8)

    class Meta:
        model = Loan
        fields = [
            'dni',
            'firstname',
            'lastname',
            'gender',
            'email',
            'amount'
        ]


class LoanRequesterForm(Form):
    approved = BooleanField()
