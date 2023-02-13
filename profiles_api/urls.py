from profiles_api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('product', views.MotorcycleViewSet)
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('car', views.UserProfileViewSet)
router.register('invoice', views.InvoiceViewSet)
router.register('invoice_item', views.InvoiceItemViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]
