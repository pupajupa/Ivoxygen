from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from decouple import config
from store.models import Product
from django.core.mail import EmailMessage
import requests
from django.template.loader import render_to_string


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': str(grand_total).replace(',', '.'),
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

def get_paypal_access_token():
    client_id = config('PAYPAL_CLIENT_ID')
    secret = config('PAYPAL_SECRET')

    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, data=data, auth=(client_id, secret), headers={"Accept": "application/json"})
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to get access token")
    
def create_paypal_order(request):
    if request.method == 'POST':
        total_str = request.POST.get('total')

        if not total_str:
            return JsonResponse({'error': 'Total amount is required'}, status=400)

        try:
            # Replace comma with dot if necessary (e.g., European decimal format)
            total = float(total_str.replace(',', '.'))
        except ValueError:
            return JsonResponse({'error': 'Invalid total amount format'}, status=400)
        
        currency = request.POST.get('currency', 'USD')
        access_token = get_paypal_access_token()
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",  # Замените YOUR_ACCESS_TOKEN на ваш access token
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": str(total),
                    }
                }
            ],
            "application_context": {
                "brand_name": "IVOXYGEN",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "PAY_NOW",
            },
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            order_id = response.json().get("id")
            return JsonResponse({"orderID": order_id})
        else:
            return JsonResponse({"error": "Failed to create order"}, status=400)

def capture_paypal_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        trans_id = request.POST.get('transID')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        # Сохраняем информацию о платеже в базе данных
        payment = Payment(
            user=request.user,
            payment_id=trans_id,
            payment_method=payment_method,
            amount_paid=status,  # Здесь можно использовать сумму из заказа
            status=status,
        )
        payment.save()

        # Обновляем статус заказа
        order = Order.objects.get(order_number=request.session.get('order_number'))
        order.payment = payment
        order.is_ordered = True
        order.save()

        return JsonResponse({
            "order_number": order.order_number,
            "transID": payment.payment_id,
        })
    
    