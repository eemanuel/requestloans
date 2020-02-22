from django.db import models
from django.db.models import (
    CharField, EmailField, DecimalField, BooleanField, DateTimeField
)

from .constants import GENDER_CHOICES
from core_utils.models import TimeStampModel


class Loan(TimeStampModel):
    amount = DecimalField(max_digits=6, decimal_places=2)
    dni = CharField(max_length=8)
    firstname = CharField(max_length=150)
    lastname = CharField(max_length=100)
    gender = CharField(max_length=1, choices=GENDER_CHOICES)
    email = EmailField(max_length=250, help_text=("Example: pepe@localhost"))
    approved = BooleanField(default=False)

    class Meta:
        db_table = "loans"
        ordering = ("id",)

    def __str__(self):
        return f"id={self.id}, dni={self.dni}, amount={self.amount}"
