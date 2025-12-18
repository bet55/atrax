from django.shortcuts import render
from core.services.phone_lookup_service import PhoneLookupService


def phone_lookup_form(request):
    """
    Веб-форма для поиска информации по номеру телефона.
    """
    context = {}

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()

        if phone:
            # Сохраняем введенный номер для отображения в форме
            context['phone_input'] = phone

            # Ищем информацию
            result = PhoneLookupService.lookup(phone)

            if result:
                context['result'] = result
                context['success'] = True
            else:
                context['error'] = 'Номер не найден в реестре'
        else:
            context['error'] = 'Введите номер телефона'

    return render(request, 'phone_lookup.html', context)