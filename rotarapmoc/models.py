from django.db import models


class Match(models.Model):
    home = models.CharField()
    visitor = models.CharField()
    price_1 = models.FloatField()
    price_x = models.FloatField()
    price_2 = models.FloatField()