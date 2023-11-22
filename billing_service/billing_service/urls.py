"""
URL configuration for billing_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from subscription_plans.views import CompleteClickPaymentView, PrepareClickPaymentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', include("subscription_plans.urls")),
    path('prepare/', PrepareClickPaymentView.as_view(),
         name='prepare_click_payment'),
    path('complete/', CompleteClickPaymentView.as_view(),
         name='complete_click_payment'),
    path('', include('billing_statistics.urls'))
]
