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
    url(r'^detail/(?P<pk>\d+)/', LoanDetailView.as_view(), name='loan-detail'),
    url(r'^update/(?P<pk>\d+)/', LoanUpdateView.as_view(), name='loan-update'),
    url(r'^delete/(?P<pk>\d+)/', LoanDeleteView.as_view(), name='loan-delete'),
]
