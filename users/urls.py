from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu_view, name='menu'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('profile/', views.user_profile, name='user_profile'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:pk>/', views.remove_cart_item, name='remove_cart_item'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

]
