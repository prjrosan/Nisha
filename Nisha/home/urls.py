from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),  # About Rosan page
    path('features/', views.features_view, name='features'),  # NISHA Features page
    path('test/', views.test_view, name='test'),  # Test view
]