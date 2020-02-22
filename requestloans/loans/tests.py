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

    def test_create_bad_request_error(self):
        """
        Testing if loan is not created with bad request.
        """

        Loan.objects.count() == 5
        bad_request_create_data = {
            "dni": 50555000,
            "gender": "X",
            "email": "email",
            "amount": 10777666555,
        }
        response = self._create_data(bad_request_create_data)
        response_str = response.content.decode()
        assert "This field is required." in response_str
        assert "Select a valid choice. X is not one of the available choices." in response_str
        assert "Enter a valid email address." in response_str
        assert "Ensure that there are no more than 6 digits in total." in response_str
        assert response.status_code == 200
