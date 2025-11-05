from django.urls import path
from .views import index, gallery, templates_view, profile, create_profile


urlpatterns = [
    path('', index, name='frontend-index'),
    path('gallery/', gallery, name='frontend-gallery'),
    path('templates/', templates_view, name='frontend-templates'),
    path('profile/', profile, name='frontend-profile'),
    path('profile/create/', create_profile, name='frontend-profile-create'),
]


 