from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

from logistics.models import Shipment

from .forms import ShipmentForm


class Index(LoginRequiredMixin,UserPassesTestMixin,TemplateView) :
    template_name = "admin-index.html"

    def test_func(self) :
        return self.request.user.is_superuser

