from django.contrib import admin
from django.urls import path
from accounts.views import (
    RegisterView, LoginView, ProductView, UserView, OrderView,
    RoleListCreateView, RoleDetailView, BusinessElementListCreateView,
    BusinessElementDetailView, AccessRuleListCreateView, AccessRuleDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('products/', ProductView.as_view(), name='products'),
    path('users/', UserView.as_view(), name='users'),
    path('orders/', OrderView.as_view(), name='orders'),
    
    path('admin/roles/', RoleListCreateView.as_view(), name='role-list'),
    path('admin/roles/<uuid:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('admin/elements/', BusinessElementListCreateView.as_view(), name='element-list'),
    path('admin/elements/<uuid:pk>/', BusinessElementDetailView.as_view(), name='element-detail'),
    path('admin/rules/', AccessRuleListCreateView.as_view(), name='rule-list'),
    path('admin/rules/<uuid:pk>/', AccessRuleDetailView.as_view(), name='rule-detail'),
]