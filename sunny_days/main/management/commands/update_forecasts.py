from datetime import date

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import City, Forecast


class Command(BaseCommand):
    help = 'Daily update of city forecasts'
    api_url = 'http://api.weatherstack.com/current'

    def handle(self, *args, **options):
        cities, today, added = City.objects.all(), date.today(), 0

        for city in cities:
            today_forecast = Forecast.objects.filter(city=city).filter(date=today).count()
            if today_forecast:
                continue

            try:
                params = {'access_key': settings.APIXU_KEY, 'query': city.name}
                response = requests.get(self.api_url, params=params).json()
                condition = response.get('current').get('weather_descriptions')[0]
                condition.replace('Clear', 'Sunny')

                Forecast.objects.create(city=city, condition=condition, date=today)
                print(f'Added forecast for {city.name} on {today}: {condition}')
                added += 1
            except Exception as e:
                print(e)

        print(f'Added forecast for {added} cities' if added else 'Everything is up-to-date')
