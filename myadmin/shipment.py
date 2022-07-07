from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

from logistics.models import Shipment

from .forms import ShipmentForm


class CreateShipment(LoginRequiredMixin,UserPassesTestMixin,View)  :
    template_name = "create-shipment.html"
    form_class = ShipmentForm
    model = Shipment

    def test_func(self) :
        return self.request.user.is_superuser

    def get(self,request,*args,**kwargs) :
        form = self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            shipment = form.save()
            return HttpResponseRedirect(reverse("shipment-detail",args=[shipment.tracking_number]))

        else :
            return render(request,self.template_name,locals())    



class  Shipments(LoginRequiredMixin,UserPassesTestMixin,ListView) :

    def test_func(self) :
        return self.request.user.is_superuser

    model  = Shipment
    template_name = "shipment-list.html"
    context_object_name = "shipments"



class AddStatusLog() : pass


class AddTransitLog() : pass
