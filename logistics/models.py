from django.db import models
import uuid
import re

from core.models import Country

class Station(models.Model) :
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name = 'stations',on_delete = models.CASCADE)




class Shipment(models.Model) :


    def get_tracking_number() :
        tracking_number =  ''.join(filter(str.isdigit,str(uuid.uuid4())))
        return tracking_number[:8]
    
    #package info
    package_name = models.CharField(max_length=20)
    weight = models.PositiveIntegerField()   #in kg
    tracking_number = models.CharField(default= get_tracking_number, max_length=8,blank = True)
    is_fragile = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False,blank = True)
    shipment_fee = models.DecimalField(decimal_places=2,max_digits=100,blank = True)
    
    #shipment info
    source_country = models.ForeignKey(Country,on_delete = models.CASCADE,related_name="shipment_source")
    source_address = models.CharField(max_length = 200) 
    destination_country = models.ForeignKey(Country,on_delete = models.CASCADE,related_name = "shipment_destination")
    destination_adresss = models.CharField(max_length = 200)
    
    #sender info
    sender_name = models.CharField(max_length = 40)
    sender_address = models.CharField(max_length = 200)
    sender_phone_number = models.CharField(max_length = 20)
    sender_email = models.EmailField()

    def save(self,*args,**kwargs) :
        if not self.pk :
            #send email that the shipment has been registered
            #create first status 
            self.status_logs.objects.create(status = "registered")
            #StatusLog.objects.create(shipment = self,status = "registered")

        super(Shipment,self).save(*args,**kwargs)

    @property
    def last_status_log(self) :
        return self.status_logs.all()[0]

    @property
    def last_transit_log(self) :
        return self.transit_logs.all()[0]

    @property
    def shipment_status_log(self)  :
        if self.last_status_log.status != "in transit" :
            log = {
            "location" : "packaging station",
            "status" : self.last_status_log.status,
            "date_since" : self.last_status_log.date,
            "status_verbose" : self.last_status_log.status,
        }

        else :
            #then get transit data
            log = {
            "location" : "{} station".format(self.last_transit_log.station.name),
            "status" : self.last_transit_log.status,
            "date_since" : self.last_transit_log.date,
            "status_verbose" : self.last_transit_log.status_verbose,
        }

        return log


    
     

class StatusLog(models.Model) :
    
    StatusChoices = (
        ("registered","registred"),
        ("received","received"),
        ("processing","processing"),
        ("in transit","in transit")

    )

    shipment = models.ForeignKey(Shipment,related_name = "status_logs",on_delete = models.CASCADE)
    status  = models.CharField(max_length = 10,choices = StatusChoices)
    date = models.DateTimeField(auto_now_add=True)

    class Meta() :
        ordering = ['-date']

    def save(self,*args,**kwargs) :
        if self.status == "in transit" :
            #make sure a shipment log has been created for this shipment
            #if not raise an Object Does not Exists exception and prevent save
            _ = self.shipment.transit_logs
            
        super(StatusLog,self).save(*args,**kwargs) 




class TransitLog(models.Model) :

    StatusChoices = (
        ("arrived","arrived"),
        ("processing","processing"),
        ("dispatched","dispatched")

    )
    shipment = models.ForeignKey(Shipment,related_name = 'transit_logs',on_delete = models.CASCADE)
    status  = models.CharField(max_length = 10,choices = StatusChoices)
    station = models.ForeignKey(Station,on_delete = models.CASCADE,related_name ="transit_logs")
    date = models.DateTimeField(auto_now_add=True)

    @property
    def status_verbose(self) :
        if self.status == "arrived" :
            return "Arrived at {} terminal".format(self.station.name)

        elif self.status == "processing" :
            return "Being processed at {} terminal".formst(self.station.name)  

        else : return "dispatched to the next terminal"      


    class Meta() :
        ordering = ['-date']
