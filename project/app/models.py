from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Base(models.Model):
    """拠点"""
    name = models.CharField('拠点名', max_length=20)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Seat(models.Model):
    """座席"""
    seatno = models.CharField('座席番号', max_length=20)
    base = models.ForeignKey(Base, verbose_name='拠点', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
    #    return f'{self.base.name} - {self.seatno}'
        return f'{self.seatno}'

class Schedule(models.Model):
    """予約スケジュール."""
    date = models.DateTimeField('予約日')    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    base = models.ForeignKey(Base, verbose_name='拠点', on_delete=models.CASCADE)
    seat = models.ForeignKey('Seat', verbose_name='座席番号', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "base", "seat"],
                name="schedule_unique"
            ),
        ]

    def __str__(self):
        date = timezone.localdate(self.date).strftime('%Y/%M/%D')
        #start = timezone.localdate(self.start)
        return f'{self.base.name} {self.seat} {self.date} {self.user}'
