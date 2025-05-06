from django.db import models

class TrackInvestment(models.Model):
    date = models.DateField(auto_now=True)
    acbs = models.PositiveIntegerField(blank=True,default=0)
    mio = models.PositiveIntegerField(blank=True,default=0)
    dragon = models.PositiveIntegerField(blank=True,default=0)
    ssi = models.PositiveIntegerField(blank=True,default=0)
    idle_cash = models.PositiveIntegerField(blank=True,default=0)
    crypto = models.PositiveIntegerField(blank=True,default=0)
    total = models.PositiveIntegerField(blank=True,default=0,editable=False)

    def save(self, *args, **kwargs):
        self.total = self.acbs + self.mio + self.dragon + self.ssi + self.idle_cash + self.crypto
        super().save(*args, **kwargs)