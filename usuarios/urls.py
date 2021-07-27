from django.urls import path
from . import views

urlpatterns = [
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('perfil', views.perfil, name='perfil'),
    path('alterasenha', views.alterasenha, name='alterasenha'),
    path('extrato', views.extrato, name='extrato'),
    path('extratojson', views.extrato_json, name='extratojson'),
]
