from . import views
from django.urls import path
urlpatterns = [
    path('', views.index, name='home'),
    path('<int:product_id>/', views.view, name='view'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    path('cart/', views.show_cart, name='show_cart'),
    path('cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('delete/<int:product_id>', views.delete_product, name='delete'),
    path('payment/', views.payment_complete, name='payment_complete'),

]
