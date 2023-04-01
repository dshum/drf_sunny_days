from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import City, Forecast
from .serializers import CitySerializer, CityViewSerializer


class CityViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    serializer_classes = {
        'list': CitySerializer,
        'retrieve': CityViewSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    @method_decorator(cache_page(24 * 60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(args, kwargs)

    @method_decorator(cache_page(60 * 60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(args, kwargs)


def index(request):
    cities = City.objects.all()
    return render(request, 'index.html', {'cities': cities})
