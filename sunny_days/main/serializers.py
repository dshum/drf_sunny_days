from abc import ABC
from datetime import datetime, date

from django.db import connection
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import serializers

from .models import City, Forecast


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class CityViewSerializer(serializers.ModelSerializer):
    longest_sunshine_period = serializers.SerializerMethodField()
    month_max_sunshine_period = serializers.SerializerMethodField()
    current_sunshine_period = serializers.SerializerMethodField()

    @staticmethod
    def get_longest_sunshine_period(obj: City) -> int:
        """
        Historical longest period of sunny days in given city.

        The article on Gaps and islands problem was used:
        https://www.sqlservercentral.com/articles/group-islands-of-contiguous-dates-sql-spackle
        """
        query = '''
            SELECT MAX(c) max
            FROM (
                SELECT condition, COUNT(grp) c
                FROM (
                    SELECT
                        *,
                        ROW_NUMBER() OVER(ORDER BY date) - ROW_NUMBER() OVER(PARTITION BY condition ORDER BY date) grp
                    FROM main_forecast
                    WHERE city_id = %s
                ) t1
                GROUP BY grp, condition
            ) t2
            WHERE condition = %s;
        '''
        with connection.cursor() as cursor:
            cursor.execute(query, [obj.pk, 'Sunny'])
            row = cursor.fetchone()
        return row[0]

    @staticmethod
    def get_month_max_sunshine_period(obj: City) -> int:
        month_start = date.today().replace(day=1)
        current_month_forecasts = Forecast.objects.filter(city=obj) \
            .filter(date__gte=month_start) \
            .order_by('-date')
        max_period = count = 0
        for forecast in current_month_forecasts:
            if forecast.condition == 'Sunny':
                count += 1
                if count > max_period:
                    max_period = count
            else:
                count = 0
        return max_period

    @staticmethod
    def get_current_sunshine_period(obj: City) -> int:
        last_overcast_day = Forecast.objects.filter(city=obj) \
            .filter(~Q(condition='Sunny')) \
            .order_by('-date')
        delta = date.today() - last_overcast_day[0].date
        return delta.days

    class Meta:
        model = City
        fields = ['id', 'name', 'longest_sunshine_period', 'month_max_sunshine_period', 'current_sunshine_period']
