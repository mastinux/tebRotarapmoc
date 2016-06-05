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
        string = "[%s] \t%s-%s [%s] \t| %4.2f | %4.2f | %4.2f |" % \
                 (self.origin, self.home, self.visitor, self.datetime, self.price_1, self.price_x, self.price_2)
        return string

    def is_stored(self):
        tmp = Match.objects.filter(origin=self.origin
                                   #, datetime=self.datetime
                                   , home=self.home, visitor=self.visitor)
        if tmp:
            return tmp
        else:
            return None

    @staticmethod
    def get_last_match_stored(origin, date, home, visitor):
        # you must pass tomorrow as date
        match_list = Match.objects.filter(origin=origin, datetime__lte=date, home=home, visitor=visitor)
        if len(match_list) > 0:
            return match_list[0]
        else:
            return None