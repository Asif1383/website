from django.shortcuts import render, redirect
from .models import Product, CartItem, MultipleProduct
from django.core.paginator import Paginator
import request
from .forms import Register
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MyUser as User
from django.contrib.messages import constants as messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.
def index(request):
    product_name = request.GET.get('item_name')
    if product_name != '' and product_name is not None:
        product = Product.objects.filter(title=product_name)
    else:
        product = Product.objects.all()
    # print(product)
    paginator = Paginator(product, 8)

    page = request.GET.get('page')
    # print(page)
    product = paginator.get_page(page)

    context = {
        'products': product,
        'user': request.user,
    }
    return render(request, 'index.html', context=context)


# view to Item Detail
def view(request, product_id):
    product = Product.objects.filter(id=int(product_id))
    path = request.path_info
    return render(request, 'view.html', {'product': product[0]})


# Add to Cart
@login_required()
def add_to_cart(request, product_id):
    user = User.objects.filter(id=request.user.id).first()
    cart = CartItem.objects.filter(cart_to_user=user).first()
    # print(cart)
    product = Product.objects.filter(id=product_id).first()
    product.cart_to_product.add(cart)
    multiple_product = MultipleProduct.objects.filter(product=product).filter(user=user).first()

    if multiple_product is None:
        multiple_product = MultipleProduct(product=product, user=user)

    multiple_product.total_product += 1
    multiple_product.save()

    return redirect('home')


# show Cart
@login_required()
def show_cart(request):
    user = User.objects.filter(id=request.user.id).first()
    cart = CartItem.objects.filter(cart_to_user=user).first()
    if cart is None:

        cart = CartItem(cart_to_user=user)
        cart.save()
    products = Product.objects.filter(cart_to_product=cart)
    print(cart)
    multiple_product = []
    sum = 0
    size = 0
    for product in products:
        mp = MultipleProduct.objects.filter(product=product).filter(user=user).first()
        sum += mp.total_product * mp.product.discount_price
        size += mp.total_product
        multiple_product.append(mp)

    return render(request, 'cart.html', {'mp': multiple_product, 'size':size ,'sum_of_products': sum})


# Register a user
def register(request):
    register_form = Register()
    if request.method == "POST":
        if request.POST.get('email'):
            messages.info(request, "User already exist")
            return redirect('login_user')
        new_user = User(
            email=request.POST['email']
        )

        new_user.set_password(request.POST['password'])
        new_user.save()
        cart = CartItem(
            cart_to_user=new_user
        )
        cart.save()
        login(request, new_user)
        return redirect('home')
    return render(request, 'register.html', {'form': register_form})

#payment-completed
@csrf_exempt
def payment_complete(request):

    if request.method == "POST":
        cart = CartItem.objects.filter(cart_to_user=request.user).first()
        products = Product.objects.filter(cart_to_product=cart)
        mp = MultipleProduct.objects.filter(user=request.user)

        for product in products:
            product.cart_to_product.clear()


    return redirect('home')

# #Process-Complete
# def payment(request):
#     return render(request,  'address.html')


# Login
def login_user(request):
    if request.method == "POST":
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if not request.POST.get('remember'):
                request.session.set_expiry(0)
            return redirect('home')
        messages.error(request, "Entered data is invalid")
    return render(request, 'login.html', )


# logout
@login_required()
def logout_user(request):
    logout(request)
    return redirect('home')


# Delete of product
@login_required()
def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    multiple_product = MultipleProduct.objects.filter(product=product, user=request.user).first()
    print(multiple_product.total_product)
    multiple_product.total_product -= 1
    multiple_product.save()

    if multiple_product.total_product == 0:
        product.cart_to_product.clear()

    return redirect('show_cart')
