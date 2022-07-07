from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

from logistics.models import Shipment

from .forms import ShipmentForm


class CreateShipment(View)  :
    template_name = "create-shipment.html"
    form_class = ShipmentForm
    model = Shipment

    def get(self,request,*args,**kwargs) :
        form = self.form_class()
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :
        form = self.form_class(request.POST)
        if form.is_valid() :
            shipment = form.save()
            return HttpResponseRedirect(reverse("myadmin-index"))

        else :
            return render(request,self.template_name,locals())    


