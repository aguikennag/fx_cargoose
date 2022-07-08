from django import forms

from logistics.models import Shipment, StatusLog, TransitLog




class ShipmentForm(forms.ModelForm) :

    class Meta() :
        model = Shipment
        exclude = [
            "is_paid",
            "tracking_number"
        ]


class StatusLogForm(forms.ModelForm) :

    class Meta() :
        model = StatusLog
        fields = [
            'status'
        ]


class TransitLogForm(forms.ModelForm) :

    class Meta() :
        model = TransitLog
        fields = [
            'status',
            'station'
        ]

