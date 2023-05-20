from django.db import models
from django.utils import timezone


# Create your models here.


class Rate(models.Model):
    date = models.DateField(default=timezone.now, null=False)
    vendor = models.CharField(max_length=255)
    currency_a = models.CharField(max_length=3)
    currency_b = models.CharField(max_length=3)
    sell = models.DecimalField(max_digits=10, decimal_places=5)
    buy = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "vendor", "currency_a", "currency_b"],
                name="unique_rate",
            )
        ]
