from django.db import models
from datetime import datetime
import django.utils.timezone
from datetime import timedelta

USER_CHOICES = [
    ('Phat', "Phat")
]

ROUTINE_CHOICES = [
    ('Pushday', "Pushday"),
    ('Pullday', "Pullday"),
    ('Legday', "Legday"),
    ('Absday', "Absday"),
    ('Cardio', "Cardio")
]

class GymTrack(models.Model):
    user = models.CharField(max_length=50,choices=USER_CHOICES,blank=True,
    null=True,default='Phat')
    date = models.DateField()
    start = models.DateTimeField(default=django.utils.timezone.now)
    end = models.DateTimeField(default=django.utils.timezone.now)
    duration = models.CharField(editable=False,default='0')
    routine = models.CharField(max_length=100, choices=ROUTINE_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate the duration when saving the instance
        if self.start and self.end:
            # Ensure that the duration is a timedelta
            self.duration = str(self.end - self.start)
            print("start",self.start)
            print("end",self.end)
            print("duration",self.end - self.start,type(self.end - self.start))
        else:
            self.duration = timedelta(0)  # Default to zero duration if times are not set
        super().save(*args, **kwargs)