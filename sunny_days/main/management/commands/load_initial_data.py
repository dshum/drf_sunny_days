import random
from datetime import datetime, timedelta
from itertools import groupby
from collections import Counter

from django.core.management.base import BaseCommand

from ...models import City, Forecast


def group_in_isles(elements: list):
    print([list(j) for i, j in groupby(elements)])


def group_same_values(elements: list):
    print(Counter(elements))


class Command(BaseCommand):
    help = 'Load initial random forecast data'
    cities = {
        'Moscow': {
            'Sunny': 20,
            'Cloudy': 50,
            'Rain': 15,
            'Snow': 15,
        },
        'Novosibirsk': {
            'Sunny': 50,
            'Cloudy': 10,
            'Rain': 10,
            'Snow': 30,
        },
        'Sankt Petersburg': {
            'Sunny': 10,
            'Cloudy': 30,
            'Rain': 40,
            'Snow': 20,
        },
        'Vladivostok': {
            'Sunny': 30,
            'Cloudy': 50,
            'Rain': 15,
            'Snow': 5,
        },
    }

    def handle(self, *args, **options):
        Forecast.objects.all().delete()
        City.objects.all().delete()

        for city_name, conditions in self.cities.items():
            print(city_name, conditions)
            city = City(name=city_name)
            city.save()

            date = datetime.today() - timedelta(days=365)
            probable_weathers = random.choices(list(conditions.keys()),
                                               weights=list(conditions.values()),
                                               k=365)
            for day, weather in enumerate(probable_weathers):
                forecast = Forecast(city=city, condition=weather, date=date + timedelta(days=day))
                forecast.save()

        print('Done')
