from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'main/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    for p_id, quantity in cart.items():
        product = get_object_or_404(Product, id=p_id)
        total_price += product.price * quantity
        products.append({'product': product, 'quantity': quantity})
    
    return render(request, 'main/cart.html', {'products': products, 'total_price': total_price})
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart_detail')

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    action = request.GET.get('action') # 'plus' или 'minus'
    
    if str(product_id) in cart:
        if action == 'plus':
            cart[str(product_id)] += 1
        elif action == 'minus':
            cart[str(product_id)] -= 1
            if cart[str(product_id)] < 1:
                del cart[str(product_id)]
    
    request.session['cart'] = cart
    return redirect('cart_detail')