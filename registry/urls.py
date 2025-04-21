from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'animals', views.AnimalViewSet)
router.register(r'owners', views.OwnerViewSet)
router.register(r'animal-search', views.AnimalSearchViewSet, basename='animal-search')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/animals/<int:pk>/set-parents/', views.AnimalViewSet.as_view({'patch': 'set_parents'}), name='animal-set-parents'),
    path('api/animals/<int:pk>/tree/', views.AnimalTreeView.as_view(), name='animal-tree'),  # Corrigido com o nome 'animal-tree'
    path('api/animals/<int:pk>/descendants/', views.AnimalDescendantsView.as_view(), name='animal-descendants'),  # Corrigido com o nome 'animal-descendants'
]
