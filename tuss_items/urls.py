from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'medicamentos', views.MedicamentoViewSet, basename='medicamento')
router.register(r'materiais', views.MaterialViewSet, basename='material')
router.register(r'diarias_taxas', views.DiariaTaxaViewSet, basename='diaria_taxa')
router.register(r'procedimentos', views.ProcedimentoViewSet, basename='procedimento')
router.register(r'demais_terminologias', views.DemaisTerminologiaViewSet, basename='demais_terminologia')
router.register(r'tabelas', views.TabelasViewSet, basename='tabelas')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.GeneralSearchView.as_view(), name='search_view_set'),
]
