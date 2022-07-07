from django.shortcuts import render,get_object_or_404

from django.views.generic import View,DetailView
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from logistics.models import Shipment


class TrackShipment(View) :

    def get(self,request,*args,**kwargs) :
        tracking_number = request.GET.get("tracking_number")
        if not tracking_number :
            return HttpResponse("Invalid request, a tracking number is expected")
        return HttpResponseRedirect(reverse("shipment-detail",args=[tracking_number]))    



class ShipmentDetail(View) :
    model = Shipment
    context_object_name = "shipment"

    def get_template_name(self) :
        if self.request.user.is_superuser :
            return "shipment-detail-admin.html"
        return "shipment-detail.html"    

    def get(self,request,*args,**kwargs) :
        shipment = self.model.objects.filter(tracking_number = kwargs['tracking_number'])
        if shipment.exists() :
            shipment = shipment.first()
            return render(request,self.get_template_name(),locals())

        else :
            return HttpResponse("The entered tracking number is incorrect, No shipment with the tracking number was found")   
    
    def get_context_data(self,**kwargs) :
        ctx = super(ShipmentDetail,self).get_context_data(**kwargs)
        return ctx


