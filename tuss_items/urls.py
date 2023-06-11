from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'tabelas', views.TabelasViewSet, basename='tabelas')
router.register(r'grupos', views.GruposViewSet, basename='grupos')
router.register(r'termos_tuss', views.TermoTussViewSet, basename='termos_tuss')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.SearchViewSet.as_view(), name='search'),
    path('autocomplete/', views.AutoCompleteViewSet.as_view(), name='autocomplete'),
]
