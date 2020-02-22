from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import LoanForm, LoanRequesterForm
from .models import Loan
from .requester import LoanRequester


class LoanCreateView(CreateView):
    form_class = LoanForm
    template_name = ''
    success_url = reverse_lazy('loan-create')

    def form_valid(self, form):
        data = {
            'document_number': form.cleaned_data['dni'],
            'gender': form.cleaned_data['gender'],
            'email': form.cleaned_data['email']
        }
        loan_requester = LoanRequester()
        loan_response = loan_requester.request(data)
        loan_form = LoanRequesterForm(data=loan_response.json())
        import ipdb; ipdb.set_trace()
        if not loan_form.is_valid():
            self.success_message = "Loan Reject"
            return HttpResponseRedirect(self.get_success_url())
        self.success_message = "Loan Accepted"
        form.instance.approved = True
        return super().form_valid(form)

