from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import MenuItem, CartItem, Cart, Order, UserProfile
from .forms import CartItemForm, UserProfileForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def menu_view(request):
    query = request.GET.get('q')
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    else:
        menu_items = MenuItem.objects.all()
    cart_items = CartItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items, 'cart_items': cart_items})

def view_cart(request):
    # Ensure only one active cart per user
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not created:
        # There are multiple active carts for the user; ensure only one active cart
        active_carts = Cart.objects.filter(user=request.user)
        if active_carts.count() > 1:
            # Merge carts if there are multiple
            primary_cart = active_carts.first()
            for extra_cart in active_carts[1:]:
                for item in extra_cart.cartitem_set.all():
                    cart_item, item_created = CartItem.objects.get_or_create(cart=primary_cart, menu_item=item.menu_item, toShow=True)
                    if not item_created:
                        cart_item.quantity += item.quantity
                    cart_item.save()
                extra_cart.delete()
            cart = primary_cart
    
    items = CartItem.objects.filter(cart=cart, toShow=True)
    for item in items:
        item.total_price = item.menu_item.price * item.quantity

    total_amount = sum(item.total_price for item in items)
    return render(request, 'cart/view_cart.html', {'cart': cart, 'items': items, 'total_amount': total_amount})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            print(f"Created new cart for user: {request.user.username}")
        else:
            print(f"Using existing cart for user: {request.user.username}")

        cart.is_active = True
        cart.save()

        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect('menu')

    return redirect('menu')

@login_required
def update_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('view_cart')
    return redirect('view_cart')

from django.shortcuts import get_object_or_404, redirect
from .models import CartItem

@login_required
def remove_cart_item(request, pk):
    try:
        item = CartItem.objects.get(pk=pk)
        item.delete()
    except CartItem.DoesNotExist:
        pass  # Handle the case where the item doesn't exist, if necessary
    
    return redirect('view_cart')

@login_required
def order_summary(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "You don't have any items in your cart.")
        return redirect('menu')

    items = CartItem.objects.filter(cart=cart,toShow=True)
    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('menu')

    total_amount = sum(item.menu_item.price * item.quantity for item in items)
    return render(request, 'cart/order_summary.html', {'items': items, 'total_amount': total_amount})

@login_required
def confirm_order(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        print(f"Found active cart for user: {request.user.username}")
    except Cart.DoesNotExist:
        messages.error(request, "You don't have any active cart.")
        print(f"No active cart found for user: {request.user.username}")
        return redirect('home')

    items = CartItem.objects.filter(cart=cart, toShow=True)
    if not items.exists():
        messages.error(request, "Your cart is empty.")
        print(f"Cart is empty for user: {request.user.username}")
        return redirect('view_cart')

    total_amount = sum(item.menu_item.price * item.quantity for item in items)

    # Create the order
    order = Order.objects.create(user=request.user, total_amount=total_amount)
    for item in items:
        order.items.add(item)
    order.save()

    # Deactivate the cart
    cart.is_active = False
    cart.save()
    
    for item in items:
        item.toShow = False
        item.save(update_fields=['toShow'])
        

    # Clear the cart items (optional)
    # cart.cartitem_set.all().delete()

    return render(request, 'cart/confirmation.html', {'order': order})

@login_required
def user_profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        orders = Order.objects.filter(user=user).order_by('-created_at')  # Adjust field name if necessary
        return render(request, 'profile.html', {'user_profile': user_profile, 'orders': orders})
    except UserProfile.DoesNotExist:
        return render(request, 'profile.html', {'user_profile': None, 'orders': None})
    
@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'edit_profile.html', {'form': form})