from random import randint

from mixer.backend.django import mixer
from loans.models import Loan


class LoansFactory(object):
    @staticmethod
    def create_loan(**kwargs):
        amount = kwargs.get("amount")
        if amount is None:
            kwargs["amount"] = randint(1, 9) * 1000
        loan = mixer.blend(Loan, **kwargs)
        return loan
