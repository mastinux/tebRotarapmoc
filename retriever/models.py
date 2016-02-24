from django.db import models


class Match(models.Model):
    origin = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    home = models.CharField(max_length=255)
    visitor = models.CharField(max_length=255)
    price_1 = models.FloatField()
    price_x = models.FloatField()
    price_2 = models.FloatField()

    def __unicode__(self):
        string = "%s-%s [%s] | %4.2f | %4.2f | %4.2f |" % \
                 (self.home, self.visitor, self.datetime, self.price_1, self.price_x, self.price_2)
        return string

    def is_stored(self):
        if Match.objects.filter(origin=self.origin, datetime=self.datetime, home=self.home, visitor=self.visitor):
            return True
        else:
            return False