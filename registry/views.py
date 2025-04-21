from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from registry.models import Animal, Owner
from registry.serializers import AnimalSerializer, OwnerSerializer, AnimalSearchSerializer
import django_filters
from rest_framework import status

class AnimalFilter(django_filters.FilterSet):
    species = django_filters.CharFilter(lookup_expr='icontains')
    breed = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Animal
        fields = ['species', 'breed', 'name']

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = AnimalFilter
    ordering_fields = ['name', 'species', 'breed']
    ordering = ['name']

    @action(detail=True, methods=['patch'])
    def set_parents(self, request, pk=None):
        animal = self.get_object()
        father_id = request.data.get('father')
        mother_id = request.data.get('mother')

        father = None
        mother = None

        if father_id:
            father = Animal.objects.filter(id=father_id).first()
            if not father:
                return Response({'error': 'Invalid father ID.'}, status=400)
        
        if mother_id:
            mother = Animal.objects.filter(id=mother_id).first()
            if not mother:
                return Response({'error': 'Invalid mother ID.'}, status=400)

        old_father = animal.father
        old_mother = animal.mother

        animal.father = father
        animal.mother = mother
        animal.save()

        return Response({
            'message': f'Parents updated for {animal.name}.',
            'old_father': AnimalSerializer(old_father).data if old_father else None,
            'old_mother': AnimalSerializer(old_mother).data if old_mother else None,
            'father': AnimalSerializer(father).data if father else None,
            'mother': AnimalSerializer(mother).data if mother else None,
        })

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class AnimalSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSearchSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['species', 'breed', 'name']
    ordering_fields = ['name', 'species', 'breed']
    ordering = ['name']
    pagination_class = PageNumberPagination
    page_size = 20

class AnimalTreeView(APIView):
    def get(self, request, pk):
        try:
            animal = Animal.objects.get(id=pk)
        except Animal.DoesNotExist:
            return Response({'error': 'Animal not found.'}, status=status.HTTP_404_NOT_FOUND)

        ancestors = animal.get_ancestors()
        serializer = AnimalSerializer(ancestors, many=True)
        return Response({'ancestors': serializer.data}, status=status.HTTP_200_OK)

class AnimalDescendantsView(APIView):
    def get(self, request, pk):
        try:
            animal = Animal.objects.get(id=pk)
        except Animal.DoesNotExist:
            return Response({'error': 'Animal not found.'}, status=status.HTTP_404_NOT_FOUND)

        descendants = animal.get_descendants()
        serializer = AnimalSerializer(descendants, many=True)
        return Response({'descendants': serializer.data}, status=status.HTTP_200_OK)