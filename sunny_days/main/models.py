from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name}"


class Forecast(models.Model):
    condition = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, db_index=True, related_name='forecasts')
    date = models.DateField()

    objects = models.Manager()

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.condition} on {self.date}"
