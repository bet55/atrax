from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import PhoneLookupSerializer
from core.services.phone_lookup_service import PhoneLookupService


class PhoneLookupAPIView(APIView):
    """
    API для поиска информации по номеру телефона.

    Пример запроса:
    GET /api/lookup/?phone=79173453223

    Пример ответа (успех):
    {
        "phone": "79173453223",
        "operator": "ПАО \"Мобильные ТелеСистемы\"",
        "region": "Республика Татарстан"
    }

    Пример ответа (ошибка):
    {
        "error": "Номер не найден в реестре"
    }
    """

    def get(self, request):
        serializer = PhoneLookupSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        phone = serializer.validated_data['phone']

        result = PhoneLookupService.lookup(phone)

        if result:
            response_data = {
                'phone': phone,
                'operator': result['operator'],
                'region': result['region'],
            }

            # Добавляем ИНН если есть
            if result['inn']:
                response_data['inn'] = result['inn']

            return Response(
                response_data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Номер не найден в реестре'},
                status=status.HTTP_404_NOT_FOUND
            )
