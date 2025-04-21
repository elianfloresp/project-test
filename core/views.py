from rest_framework import viewsets, filters
from registry.models import Animal, Owner
from registry.serializers import AnimalSerializer, OwnerSerializer, AnimalSearchSerializer
from django.http import HttpResponse



def home(request):
    return HttpResponse("Bem-vindo à API!")

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class AnimalSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['species', 'breed', 'name']

    
