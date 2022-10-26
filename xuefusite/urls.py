"""zhongyifangji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns
from xuefuapp import views,restapi

api_urlpatterns = [
    path('xuefu/api-root/', restapi.api_root),
    path('xuefu/api/cars/', restapi.CarList.as_view(),name='car-list'),
    path('xuefu/api/queues/ground/', restapi.ground_list,name='ground-list'),
    path('xuefu/api/queues/underground/', restapi.underground_list,name='underground-list'),
    path('xuefu/api/queues/underground-2/', restapi.underground_list_2,name='underground-list-2'),
    path('xuefu/api/fees/', restapi.fee_list,name='fee-list'),
    path('xuefu/api/cars/<pk>/', restapi.CarDetail.as_view(),name = 'car-detail'),
    path('xuefu/api/owners/', restapi.OwnerList.as_view(),name='owner-list'),
    path('xuefu/api/owners/<int:pk>/', restapi.OwnerDetail.as_view(),name='owner-detail'),
    path('xuefu/api/jwt-auth/',obtain_jwt_token),
    path('xuefu/api/on-wx-login/', restapi.on_wx_login),
    path('xuefu/api/open-door/auth/', restapi.on_open_door, name='open-door'),
]
urlpatterns = [
    path('xuefu/admin/', admin.site.urls,name="admin"),
    path('xuefu/overview', views.overview, name="overview"),
    path('xuefu/fee/list/', views.FilterFeeView.as_view(), name="fee_list"),
    path('xuefu/car/query/', views.FilterCarView.as_view(),name='car_query'),
    path('xuefu/car/detail/<pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('xuefu/fee/detail/<pk>/', views.FeeDetailView.as_view(), name='fee_detail'),
    path('xuefu/queue/ground/', views.FilterGroundView.as_view(),name='ground_list'),
    path('xuefu/queue/underground/', views.FilterUndergroundView.as_view(), name='underground_list'),
    path('xuefu/queue/underground2/', views.FilterUndergroundView2.as_view(), name='underground_list_2'),
    path('xuefu/', views.FilterFeeView.as_view()),
    path('xuefu/port/', views.port,name="port")] \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + format_suffix_patterns(api_urlpatterns)
    #format_suffix_patterns

