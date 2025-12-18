from django.urls import path
from core.views import phone_lookup_form

app_name = 'core'

urlpatterns = [
    path('', phone_lookup_form, name='phone_lookup_form'),
]