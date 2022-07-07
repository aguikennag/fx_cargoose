from django import forms

from logistics.models import Shipment




class ShipmentForm(forms.ModelForm) :

    class Meta() :
        model = Shipment
        exclude = [
            "is_paid",
            "tracking_number"
        ]