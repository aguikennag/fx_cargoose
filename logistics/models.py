from django.db import models
from django.core.exceptions import ObjectDoesNotExist
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
    weight = models.FloatField(help_text="in kg")   #in kg
    tracking_number = models.CharField(default= get_tracking_number, max_length=8,blank = True)
    is_fragile = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False,blank = True)
    shipment_fee = models.DecimalField(decimal_places=2,max_digits=100,blank = True,help_text = "in dollars($)")
    
    #shipment info
    source_country = models.ForeignKey(Country,on_delete = models.CASCADE,related_name="shipment_source")
    source_address = models.CharField(max_length = 200) 
    destination_country = models.ForeignKey(Country,on_delete = models.CASCADE,related_name = "shipment_destination")
    destination_address = models.CharField(max_length = 200)
    
    #sender info
    sender_name = models.CharField(max_length = 40)
    sender_address = models.CharField(max_length = 200)
    sender_phone_number = models.CharField(max_length = 20)
    sender_email = models.EmailField()

    date = models.DateTimeField(auto_now_add = True)

    def save(self,*args,**kwargs) :
        super(Shipment,self).save(*args,**kwargs)

    def update_status_log(self)   :
        statuses = [value for name,value in StatusLog.StatusChoices]
        current_status = self.last_status_log.status
        #update to next
        #get current index 
        _index = statuses.index(current_status) 
        if _index < len(statuses) - 1 :
            #anything above means its already in transit then we do nothing
            StatusLog.objects.create(shipment = self,status = statuses[_index + 1])
        else : 
            return "You cannot update status log any further, shipment is already in {}".format(current_status)  #meaning error     
       

    def roll_back_status_log(self) :
        statuses = [value for name,value in StatusLog.StatusChoices]
        current_status = self.last_status_log.status
        #update to next
        #get current index 
        _index = statuses.index(current_status) 
        if _index > 0 :
            #anything below 1 means its already in transit in the beigining, we cannot roll back further]
            #delete last log
            self.last_status_log.delete()
        else : 
            return "You cannot roll back status log any further, shipment is in {} status".format(current_status)  #meaning error  
 
    @property
    def is_in_transit(self) :
        try : 
            #if the shipment has a transit log then its in transit
            transit_logs = self.transit_logs.all() 
            if transit_logs.count() > 0 : return True   
        except ObjectDoesNotExist :  pass

        return False


    @property
    def timeline_logs(self) :
        status_logs = self.status_logs.all()
        try : transit_logs = self.transit_logs.all()    
        except ObjectDoesNotExist : transit_logs = None
       
        #combine
        timeline = []
        for log in status_logs :
            logs = {}
            logs['date'] = log.date
            logs['status'] = log.status_verbose
            timeline.append(logs)

        if transit_logs :  
            for log in transit_logs : 
                logs = {}
                logs['date'] = log.date
                logs['status'] = log.status_verbose
                timeline.append(logs)

        return timeline    

    @property
    def last_status_log(self) :
        return self.status_logs.all()[0]

    @property
    def last_transit_log(self) :
        try : return self.transit_logs.all()[0]
        except ObjectDoesNotExist : return    

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
    initial_terminal_name = "Collecting"
    
    StatusChoices = (
        ("registered","registered"),
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
    
    @property
    def status_verbose(self) :
        if self.status == "registered" :
            return "Package has just been registered, but not yet received at initial terminal".format(self.initial_terminal_name)
        
        elif self.status == "received" :
            return "Package has been received at {} terminal, awaiting processing.".format(self.initial_terminal_name)
        
        elif self.status == "processing" :
            return "Package is been processed at {} terminal".format(self.initial_terminal_name)

        else :
            return "Package has left {} terminal and is now in transit".format(self.initial_terminal_name)


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
            return "Package has arrived at {} terminal, awaiting processing".format(self.station.name)

        elif self.status == "processing" :
            return "Package is being processed at {} terminal".formst(self.station.name)  

        else : return "Package has been dispatched to the next terminal"      


    class Meta() :
        ordering = ['-date']
