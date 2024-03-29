from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create-account/', views.create_account, name="create_account"),
    path('login/', views.login, name="login"),
    path('pay/debit/', views.make_payment, name="make_payment"),
    path('pay/credit/', views.add_credit, name="add_credit")
]
