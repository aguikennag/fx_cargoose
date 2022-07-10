from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse

from logistics.models import Shipment, StatusLog,TransitLog

from .forms import ShipmentForm,StatusLogForm,TransitLogForm


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



class AddStatusLog(LoginRequiredMixin,UserPassesTestMixin,CreateView) : 
    def test_func(self) :
        return self.request.user.is_superuser

    model = StatusLog
    form_class = StatusLogForm

    def get_success_url(self) :
        return reverse("shipment-detail",args=[self.kwargs['tracking_number']])

    def form_valid(self,form) :
        shipment = Shipment.objects.filter(tracking_number = self.kwargs['tracking_number'])
        if not shipment.exists() : return HttpResponse("This shipment no longer exists")
        form.save(commit = False)
        form.instance.shipment = shipment.first()
        form.save()
        return form





class UpdateTransitLog(LoginRequiredMixin,UserPassesTestMixin,View) : 
    
    def test_func(self) :
        return self.request.user.is_superuser

    model = TransitLog
    form_class = TransitLogForm

    def get_success_url(self) :
        return reverse("shipment-detail",args=[self.kwargs['tracking_number']])

    def post(self,request,*args,**kwargs) :
        shipment = Shipment.objects.filter(tracking_number = self.kwargs['tracking_number'])
        if not shipment.exists() : return HttpResponse("This shipment no longer exists")
        if kwargs['action'] == "update" :
            form = self.form_class(request.POST)
            if form.is_valid() :
                form.save(commit = False)
                form.instance.shipment = shipment.first()
                form.save()
            else :
                print(form.errors.as_text())     
          

        elif kwargs['action'] == "roll_back" :
            error = shipment.roll_back_transit_log()
            if error :
                return HttpResponse(error)


        else :
            return HttpResponse("invalid request")  

        return HttpResponseRedirect(self.get_success_url())      


class UpdateStatusLog(LoginRequiredMixin,UserPassesTestMixin,View) : 
    def test_func(self) :
        return self.request.user.is_superuser

    model = StatusLog

 
    def post(self,request,*args,**kwargs) :
        shipment = Shipment.objects.filter(tracking_number = self.kwargs['tracking_number'])
        if not shipment.exists() : return HttpResponse("This shipment no longer exists")
        shipment = shipment.first()
        
        #just for testing, remove later
        date = request.POST.get("date")

        if kwargs['action'] == "update" :
            error = shipment.update_status_log(date = date)
            if error : return HttpResponse(error)

        elif kwargs['action'] == "roll_back"  :
            error = shipment.roll_back_status_log()  
            if error : return HttpResponse(error)

        url = reverse("shipment-detail",args=[self.kwargs['tracking_number']])
        return HttpResponseRedirect(url)


