from django.urls import path
from django.http import HttpResponse
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views


urlpatterns = [
    path('', views.home, name="home"),

    path('user/', views.userPage, name="user"),

    path('register/', views.registerUser, name="register"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile_setting', views.profileSetting, name="profile_setting"),

    path('products/', views.products, name="products"),

    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('add_customer/', views.addCustomer, name="add_customer"),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),

    path('create_order/', views.createOrder, name="create_order"),
    path('place_order_cus/<str:pk>/', views.placeOrderCus, name="place_order_cus"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),



    # Password Reset Start here________________________________________________
     path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset/password_reset_form.html',
             subject_template_name='password_reset/password_reset_subject.txt',
             email_template_name='password_reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Password Reset End here________________________________________________

]