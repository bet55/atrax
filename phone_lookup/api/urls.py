from django.urls import path
from api.views import PhoneLookupAPIView

urlpatterns = [
    path('lookup/', PhoneLookupAPIView.as_view(), name='phone_lookup'),
]
