from django.conf.urls import url
from . import  views

app_name = 'SCPapp'
urlpatterns = [
    url(r'^index$', views.Index.as_view(), name="index"),
    url(r'^main$', views.Main.as_view(), name="main"),
    url(r'listar_familias$', views.listar_familias, name="listar_familias"),
    url(r'listar_solicitudes$', views.listar_solicitudes, name="listar_solicitudes"),
    url(r'solicitar$', views.solicitar, name="solicitar"),
    url(r'aceptar$', views.aceptar, name="aceptar"),
    url(r'listar_matches$', views.listar_matches, name="listar_matches"),
    url(r'registrar_dia$', views.registrar_dia, name="registrar_dia")

]