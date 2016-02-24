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
        return "%s-%s [%s] | %f | %f | %f |" \
               % self.home, self.visitor, self.datetime, self.price_1, self.price_x, self.price_2

    def exists(self, origin, datetime, home, visitor):
        if Match.objects.filter(origin=origin, datetime=datetime, home=home, visitor=visitor):
            print "match", self, "already on DB"
        else:
            print "match must be saved"