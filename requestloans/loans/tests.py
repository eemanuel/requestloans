from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .constants import ANOTHER, FEMALE, MALE
from .models import Loan

from core_utils.utils import LoansFactory


class LoanCreateViewTestCase(TestCase):
    def setUp(self):
        self.request_create_data = {
            "dni": "33777666",
            "firstname": "Cosme",
            "lastname": "Fulanito",
            "gender": MALE,
            "email": "pepe@localhost",
            "amount": 7000,
        }
        for _ in range(5):
            LoansFactory.create_loan()
        self.client = Client()

    def _create_data(self, data):
        return self.client.post(reverse("loan-create"), data, format="json")

    def test_create_success(self):
        """
        Testing if loan is successfully created.
        """

        Loan.objects.count() == 5
        response = self._create_data(self.request_create_data)
        assert Loan.objects.count() == 6
        loan = Loan.objects.last()
        assert loan.dni == "33777666"
        assert loan.firstname == "Cosme"
        assert loan.lastname == "Fulanito"
        assert loan.gender == MALE
        assert loan.email == "pepe@localhost"
        assert loan.amount == 7000
        assert isinstance(loan.approved, bool)
        assert loan.created is not None
        assert loan.updated is not None
        assert response.status_code == 302
