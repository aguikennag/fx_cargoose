from django.db import models




class Country(models.Model) :
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=5)

    def __str__(self) :
        return "{}({})".format(self.name,self.short_name)