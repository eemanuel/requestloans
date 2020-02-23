from django.conf.urls import url

from .views import (
    LoanCreateView, 
    LoanListView,
    LoanDetailView,
    LoanUpdateView,
    LoanDeleteView,
)

urlpatterns = [
    url(r'^$', LoanCreateView.as_view(), name='loan-create'),
    url(r'^list/', LoanListView.as_view(), name='loan-list'),
    url(r'^(?P<pk>\d+)detail//', LoanDetailView.as_view(), name='loan-detail'),
    url(r'^(?P<pk>\d+)/update/', LoanUpdateView.as_view(), name='loan-update'),
    url(r'^(?P<pk>\d+)/delete/', LoanDeleteView.as_view(), name='loan-delete'),
]
