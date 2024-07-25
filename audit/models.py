from django.db import models

class company(models.Model):
    name = models.CharField(max_length=255)

class minerals(models.Model):
    name = models.CharField(max_length=255)

class mineralsYear(models.Model):
    companie = models.ForeignKey(company, on_delete=models.CASCADE)
    mineral = models.ForeignKey(minerals, on_delete=models.CASCADE)
    year = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
