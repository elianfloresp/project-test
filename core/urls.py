from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from registry.views import AnimalViewSet, OwnerViewSet, AnimalSearchViewSet, AnimalTreeView, AnimalDescendantsView
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bem-vindo à API!")

router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'animal-search', AnimalSearchViewSet, basename='animal-search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/animals/<int:pk>/set-parents/', AnimalViewSet.as_view({'patch': 'set_parents'}), name='animal-set-parents'),
    path('api/animals/<int:pk>/tree/', AnimalTreeView.as_view(), name='animal-tree'),
    path('api/animals/<int:pk>/descendants/', AnimalDescendantsView.as_view(), name='animal-descendants'),
    path('', home),
]