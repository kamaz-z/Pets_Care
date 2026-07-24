import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Order, OrderItem, Product

#________ api ________
from .nova_posta import get_cities

@login_required(login_url='login')
def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})


@login_required(login_url='login')
def cart_page(request):
    """Кошик повністю на localStorage, сервер лише віддає шаблон."""
    return render(request, 'shop/cart.html')


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
                product = Product.objects.select_for_update().get(id=item.get('id'))
                quantity = int(item.get('quantity', 1))

                if quantity < 1:
                    raise ValueError(f'Некоректна кількість для товару «{product.name}»')

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
        return JsonResponse({'status': 'error', 'message': 'Один із товарів більше не існує'}, status=400)
    except (ValueError, KeyError, TypeError) as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Помилка сервера при створенні замовлення'}, status=500)

    return JsonResponse({'status': 'success', 'message': 'Замовлення успішно створено', 'order_id': order.id})