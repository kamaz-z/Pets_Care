import json
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from .models import Order, OrderItem, Product


# ________ Views для сторінок ________

@login_required(login_url='login')
def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})


@login_required(login_url='login')
def cart_page(request):
    """Кошик повністю на localStorage, сервер лише віддає шаблон."""
    return render(request, 'shop/cart.html')


# ________ NovaPost API proxy ________

@require_GET
def np_settlements(request):
    """Пошук міст за введеним текстом (мінімум 2 символи)."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'items': []})

    headers = {
        'Authorization': getattr(settings, 'NOVAPOST_API_KEY', ''),
        'Accept': 'application/json',
    }
    params = {
        'countryCodes[]': 'UA',
        'textSearch': query,
        'limit': 10,
    }

    try:
        base_url = getattr(settings, 'NOVAPOST_BASE_URL', 'https://api.novapost.com/v.1.0')
        response = requests.get(f"{base_url}/settlements", headers=headers, params=params, timeout=5)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({'status': 'error', 'message': f'Помилка запиту до NovaPost: {str(e)}'}, status=502)


@require_GET
def np_divisions(request, settlement_id):
    """Отримання відділень/поштоматів для обраного міста."""
    headers = {
        'Authorization': getattr(settings, 'NOVAPOST_API_KEY', ''),
        'Accept': 'application/json',
    }
    params = {
        'countryCodes[]': 'UA',
        'settlementIds[]': settlement_id,
        'limit': 100,
    }

    try:
        base_url = getattr(settings, 'NOVAPOST_BASE_URL', 'https://api.novapost.com/v.1.0')
        response = requests.get(f"{base_url}/divisions", headers=headers, params=params, timeout=5)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.RequestException as e:
        return JsonResponse({'status': 'error', 'message': f'Помилка запиту до NovaPost: {str(e)}'}, status=502)


# ________ Створення замовлення ________

@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Некоректний формат запиту'}, status=400)

    full_name = (data.get('full_name') or '').strip()
    phone = (data.get('phone') or '').strip()
    address = (data.get('address') or '').strip()
    items = data.get('items') or []

    if not full_name or not phone or not address:
        return JsonResponse({'status': 'error', 'message': 'Заповніть усі поля доставки'}, status=400)

    if not items:
        return JsonResponse({'status': 'error', 'message': 'Кошик порожній'}, status=400)

    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                phone=phone,
                address=address,
            )

            for item in items:
                product_id = item.get('id')
                if not product_id:
                    raise ValueError('Некоректний ідентифікатор товару')

                product = Product.objects.select_for_update().get(id=product_id)
                
                try:
                    quantity = int(item.get('quantity', 1))
                except (ValueError, TypeError):
                    raise ValueError(f'Некоректна кількість товару «{product.name}»')

                if quantity < 1:
                    raise ValueError(f'Кількість товару «{product.name}» має бути більшою за 0')

                if product.count < quantity:
                    raise ValueError(
                        f'Недостатньо товару «{product.name}» на складі (залишилось {product.count} шт.)'
                    )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )

                product.count -= quantity
                product.save(update_fields=['count'])

    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Один із товарів у кошику більше не існує'}, status=400)
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Помилка сервера при створенні замовлення'}, status=500)

    return JsonResponse({'status': 'success', 'message': 'Замовлення успішно створено', 'order_id': order.id})