from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Avg, Q
from .models import Product, Category, Brand, Review, Cart, Order, OrderItem, ProductVariant, ContactMessage, Wishlist


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    categories = Category.objects.all()
    brands = Brand.objects.all()

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True))

    return render(request, 'store/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'brands': brands,
        'wishlist_ids': wishlist_ids,
    })


def products(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category_filter = request.GET.get('category')
    brand_filter = request.GET.get('brand')
    sort_filter = request.GET.get('sort')

    current_category = None
    if category_filter:
        all_products = all_products.filter(category__name=category_filter)
        try:
            current_category = Category.objects.get(name=category_filter)
        except Category.DoesNotExist:
            pass

    if brand_filter:
        all_products = all_products.filter(brand__name=brand_filter)
    if sort_filter == 'price_low':
        all_products = all_products.order_by('price')
    elif sort_filter == 'price_high':
        all_products = all_products.order_by('-price')
    elif sort_filter == 'newest':
        all_products = all_products.order_by('-created_at')

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True))

    return render(request, 'store/products.html', {
        'products': all_products,
        'categories': categories,
        'brands': brands,
        'category_filter': category_filter,
        'brand_filter': brand_filter,
        'sort_filter': sort_filter,
        'wishlist_ids': wishlist_ids,
        'current_category': current_category,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    review_count = reviews.count()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)

    variants = {}
    for variant in product.variants.all():
        if variant.variant_type not in variants:
            variants[variant.variant_type] = []
        variants[variant.variant_type].append(variant.value)

    recommended = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:4]

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True))

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        if comment:
            review = Review(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment,
            )
            
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', pk=pk)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_count': review_count,
        'avg_rating': avg_rating,
        'variants': variants,
        'recommended': recommended,
        'wishlist_ids': wishlist_ids,
    })


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({
            'message': f'{product.title} added to cart!',
            'cart_count': cart_count
        })
    return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required
def update_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum([item.get_total() for item in cart_items])

    discount = 0
    discount_amount = 0
    coupon_message = ''
    coupon_code = request.session.get('coupon_code', '')

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        if coupon_code == 'AURETTE20':
            request.session['coupon_code'] = coupon_code
            coupon_message = 'success'
        else:
            request.session['coupon_code'] = ''
            coupon_message = 'invalid'

    if request.session.get('coupon_code') == 'AURETTE20':
        discount = 20
        discount_amount = subtotal * 20 / 100

    total = subtotal - discount_amount

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'discount_amount': discount_amount,
        'total': total,
        'coupon_code': request.session.get('coupon_code', ''),
        'coupon_message': coupon_message,
    })


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum([item.get_total() for item in cart_items])

    discount_amount = 0
    if request.session.get('coupon_code') == 'AURETTE20':
        discount_amount = subtotal * 20 / 100

    total = subtotal - discount_amount

    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        if full_name and address and phone:
            order = Order.objects.create(
                user=request.user,
                total=total,
                full_name=full_name,
                address=address,
                phone=phone,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart_items.delete()
            request.session['coupon_code'] = ''
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('home')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'total': total,
    })


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
    return render(request, 'store/contact.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'store/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            messages.success(request, f'Welcome to Aurette, {first_name}!')
            return redirect('home')
    return render(request, 'store/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/profile.html', {
        'orders': orders,
        'wishlist_items': wishlist_items,
    })


def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()
    return render(request, 'store/search.html', {
        'results': results,
        'query': query,
    })


def search_suggestions(request):
    query = request.GET.get('q', '')
    results = []
    if query and len(query) >= 2:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).distinct()[:6]
        results = [
            {
                'id': p.id,
                'title': p.title,
                'price': str(p.price),
                'brand': p.brand.name,
                'image': p.image_url,
            }
            for p in products
        ]
    return JsonResponse({'results': results})


@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed', 'message': f'{product.title} removed from wishlist!'})
    return JsonResponse({'status': 'added', 'message': f'{product.title} added to wishlist!'})


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {
        'wishlist_items': wishlist_items,
    })