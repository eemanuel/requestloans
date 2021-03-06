from django.contrib.auth.models import User
from django.utils.timezone import datetime

from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .constants import ANOTHER, MALE
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
        self.client = Client()

    def _create_data(self, data):
        return self.client.post(reverse("loan-create"), data, format="json")

    def test_create_success(self):
        """
        Testing if loan is successfully created.
        """

        Loan.objects.count() == 0
        response = self._create_data(self.request_create_data)
        assert Loan.objects.count() == 1
        loan = Loan.objects.last()
        assert loan.dni == "33777666"
        assert loan.firstname == "Cosme"
        assert loan.lastname == "Fulanito"
        assert loan.gender == MALE
        assert loan.email == "pepe@localhost"
        assert loan.amount == 7000
        assert isinstance(loan.approved, bool)
        assert isinstance(loan.created, datetime)
        assert isinstance(loan.updated, datetime)
        assert response.status_code == 302

    def test_create_bad_request(self):
        """
        Testing if loan is not created with bad request.
        """

        Loan.objects.count() == 0
        bad_request_create_data = {
            "dni": 50555000,
            "gender": "X",
            "email": "email",
            "amount": 10777666555,
        }
        response = self._create_data(bad_request_create_data)
        Loan.objects.count() == 0
        response_str = response.content.decode()
        assert "This field is required." in response_str
        assert "Select a valid choice. X is not one of the available choices." in response_str
        assert "Enter a valid email address." in response_str
        assert "Ensure that there are no more than 6 digits in total." in response_str
        assert response.status_code == 200


class LoanListViewTestCase(TestCase):
    def setUp(self):
        create_user_data = {
            "username": "super",
            "email": "super@localhost",
            "password": "69pwd69",
        }
        self.superuser = self.create_superuser(create_user_data)
        for _ in range(5):
            LoansFactory.create_loan()
        self.client = Client()

    def _list_data(self):
        return self.client.get(reverse("loan-list"), format="json")

    def create_superuser(self, data):
        return User.objects.create_superuser(
            data.get("username"), data.get("email"), data.get("password")
        )

    def authenticate_superuser(self):
        self.client.login(username='super', password='69pwd69')

    def test_list_success(self):
        """
        Testing if loans are successfully listed.
        """

        assert Loan.objects.count() == 5
        assert User.objects.count() == 1
        self.authenticate_superuser()
        super_user = User.objects.first()
        assert super_user.is_staff
        response = self._list_data()
        response_str = response.content.decode()
        loan_qs = Loan.objects.all()
        for loan in loan_qs:
            assert loan.dni in response_str
            assert loan.firstname in response_str
            assert loan.lastname in response_str
            assert str(loan.amount) in response_str
            assert str(loan.approved) in response_str
        assert response.status_code == 200

    def test_list_not_auth_redirect(self):
        """
        Testing if redirect to login when user is not auth user.
        """

        response = self._list_data()
        assert response.url == "/admin/login/?next=/list/"
        assert response.status_code == 302


class LoanDetailViewTestCase(TestCase):
    def setUp(self):
        create_user_data = {
            "username": "super",
            "email": "super@localhost",
            "password": "69pwd69",
        }
        self.superuser = self.create_superuser(create_user_data)
        self.loan = LoansFactory.create_loan()
        self.client = Client()

    def _detail_data(self, pk):
        return self.client.get(
            reverse("loan-detail", args=[pk]),
            format="json"
        )

    def create_superuser(self, data):
        return User.objects.create_superuser(
            data.get("username"), data.get("email"), data.get("password")
        )

    def authenticate_superuser(self):
        self.client.login(username='super', password='69pwd69')

    def test_detail_success(self):
        """
        Testing if loan is successfully detailed.
        """

        self.authenticate_superuser()
        loan = self.loan
        response = self._detail_data(loan.id)
        response_str = response.content.decode()
        assert loan.dni in response_str
        assert loan.firstname in response_str
        assert loan.dni in response_str
        assert loan.lastname in response_str
        assert loan.gender in response_str
        assert loan.email in response_str
        assert str(loan.amount) in response_str
        assert str(loan.approved) in response_str
        assert response.status_code == 200

    def test_detail_invalid_id_error(self):
        """
        Testing if view returns error if pk is invalid.
        """

        self.authenticate_superuser()
        response = self._detail_data(pk=666)
        assert response.status_code == 404

    def test_detail_not_auth_redirect(self):
        """
        Testing if redirect when user is not staff user.
        """

        response = self._detail_data(self.loan.id)
        assert response.url[:27] == "/admin/login/?next=/detail/"
        assert response.status_code == 302


class LoanUpdateViewTestCase(TestCase):
    def setUp(self):
        self.request_update_data = {
            "dni": "44555777",
            "firstname": "Another",
            "lastname": "Person",
            "gender": ANOTHER,
            "email": "someone@localhost",
            "amount": 9777,
        }
        create_user_data = {
            "username": "super",
            "email": "super@localhost",
            "password": "69pwd69",
        }
        self.superuser = self.create_superuser(create_user_data)
        self.loan = LoansFactory.create_loan()
        self.client = Client()

    def _update_data(self, data, pk):
        return self.client.post(
            reverse("loan-update", args=[pk]),
            data=data,
            format="json"
        )

    def create_superuser(self, data):
        return User.objects.create_superuser(
            data.get("username"), data.get("email"), data.get("password")
        )

    def authenticate_superuser(self):
        self.client.login(username='super', password='69pwd69')

    def test_update_success(self):
        """
        Testing if loan is successfully updated.
        """

        self.authenticate_superuser()
        data = self.request_update_data
        response = self._update_data(data=data, pk=self.loan.id)
        self.loan.refresh_from_db()
        loan = self.loan
        assert data.get("dni") == loan.dni
        assert data.get("firstname") == loan.firstname
        assert data.get("lastname") == loan.lastname
        assert data.get("gender") == loan.gender
        assert data.get("email") == loan.email
        assert data.get("amount") == loan.amount
        assert response.status_code == 302

    def test_update_invalid_id_error(self):
        """
        Testing if returns error if pk is invalid.
        """

        self.authenticate_superuser()
        response = self._update_data(self.request_update_data, pk=666)
        assert response.status_code == 404

    def test_update_not_auth_redirect(self):
        """
        Testing if redirect when user is not staff user.
        """

        response = self._update_data(self.request_update_data, pk=self.loan.id)
        assert response.url[:27] == "/admin/login/?next=/update/"
        assert response.status_code == 302


class LoanDeleteViewTestCase(TestCase):
    def setUp(self):
        create_user_data = {
            "username": "super",
            "email": "super@localhost",
            "password": "69pwd69",
        }
        self.superuser = self.create_superuser(create_user_data)
        self.loan = LoansFactory.create_loan()
        self.client = Client()

    def _delete_data(self, pk):
        return self.client.delete(
            reverse("loan-delete", args=[pk]),
            format="json"
        )

    def create_superuser(self, data):
        return User.objects.create_superuser(
            data.get("username"), data.get("email"), data.get("password")
        )

    def authenticate_superuser(self):
        self.client.login(username='super', password='69pwd69')

    def test_delete_success(self):
        """
        Testing if loan is successfully deleted.
        """

        self.authenticate_superuser()
        assert Loan.objects.count() == 1
        response = self._delete_data(self.loan.id)
        assert Loan.objects.count() == 0
        assert response.url == "/list/"
        assert response.status_code == 302


    def test_delete_not_auth_redirect(self):
        """
        Testing if redirect when user is not staff user.
        """

        assert Loan.objects.count() == 1
        response = self._delete_data(self.loan.id)
        assert Loan.objects.count() == 1
        assert response.url[:27] == "/admin/login/?next=/delete/"
        assert response.status_code == 302
