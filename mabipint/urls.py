from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Utilisateurs (Admin seulement)
    path('utilisateurs/', views.user_list, name='user_list'),
    path('utilisateurs/ajouter/', views.user_create, name='user_create'),
    path('utilisateurs/<int:pk>/modifier/', views.user_edit, name='user_edit'),

    # Aide
    path('aide/statuts/', views.aide_statuts, name='aide_statuts'),

    # Devis
    path('devis/', views.devis_list, name='devis_list'),
    path('devis/nouveau/', views.devis_create, name='devis_create'),
    path('devis/<int:pk>/', views.devis_detail, name='devis_detail'),
    path('devis/<int:pk>/modifier/', views.devis_edit, name='devis_edit'),
    path('devis/<int:pk>/supprimer/', views.devis_delete, name='devis_delete'),
    path('devis/<int:pk>/pdf/', views.devis_pdf, name='devis_pdf'),
]
