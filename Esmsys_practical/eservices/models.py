from django.db import models


class District(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'District'

class Taluka(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Taluka'

class Village(models.Model):
    name = models.CharField(max_length=100)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Village'
