from django.urls import path

from NEMO_billing.prepayments.views import prepayments

urlpatterns = [
	path("prepaid_project_status/", prepayments.prepaid_project_status, name="prepaid_project_status"),
]