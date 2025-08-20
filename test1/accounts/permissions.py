from rest_framework.permissions import BasePermission
from .models import BusinessElement, AccessRule
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotFound

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.role and 
            request.user.role.name == 'admin'
        )
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed('Требуется аутентификация')
        
        element_name = getattr(view, 'business_element', None)
        if not element_name:
            return False
            
        try:
            element = BusinessElement.objects.get(name=element_name)
            rule = AccessRule.objects.get(role=request.user.role, element=element)
        except BusinessElement.DoesNotExist:
            raise NotFound('Ресурс не найден')
        except AccessRule.DoesNotExist:
            raise PermissionDenied('Доступ запрещен')
            
        method = request.method
        if method == 'GET':
            if not rule.read_permission:
                raise PermissionDenied('Нет прав на просмотр')
            return True
        elif method == 'POST':
            if not rule.create_permission:
                raise PermissionDenied('Нет прав на создание')
            return True
        elif method in ['PUT', 'PATCH']:
            if not rule.update_permission:
                raise PermissionDenied('Нет прав на изменение')
            return True
        elif method == 'DELETE':
            if not rule.delete_permission:
                raise PermissionDenied('Нет прав на удаление')
            return True
            
        return False
        
