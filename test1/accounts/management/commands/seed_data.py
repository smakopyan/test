from django.core.management.base import BaseCommand
from accounts.models import Role, BusinessElement, AccessRule

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными для системы доступа'

    def handle(self, *args, **options):
        admin_role, created = Role.objects.get_or_create(name='admin')
        if created:
            self.stdout.write(f'Создана роль: {admin_role.name}')
        
        user_role, created = Role.objects.get_or_create(name='user')
        if created:
            self.stdout.write(f'Создана роль: {user_role.name}')
            
        manager_role, created = Role.objects.get_or_create(name='manager')
        if created:
            self.stdout.write(f'Создана роль: {manager_role.name}')

        users_element, created = BusinessElement.objects.get_or_create(name='users')
        if created:
            self.stdout.write(f'Создан бизнес-элемент: {users_element.name}')
            
        products_element, created = BusinessElement.objects.get_or_create(name='products')
        if created:
            self.stdout.write(f'Создан бизнес-элемент: {products_element.name}')
            
        orders_element, created = BusinessElement.objects.get_or_create(name='orders')
        if created:
            self.stdout.write(f'Создан бизнес-элемент: {orders_element.name}')
            
        access_rules_element, created = BusinessElement.objects.get_or_create(name='access_rules')
        if created:
            self.stdout.write(f'Создан бизнес-элемент: {access_rules_element.name}')

        rule, created = AccessRule.objects.get_or_create(
            role=admin_role,
            element=users_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': True,
                'delete_permission': True,
                # 'delete_all_permission': True
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: admin → users')
        
        rule, created = AccessRule.objects.get_or_create(
            role=admin_role,
            element=products_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': True,
                'delete_permission': True,
                # 'delete_all_permission': True
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: admin → products')
            
        rule, created = AccessRule.objects.get_or_create(
            role=admin_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': True,
                'delete_permission': True,
                # 'delete_all_permission': True
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: admin → orders')
            
        rule, created = AccessRule.objects.get_or_create(
            role=admin_role,
            element=access_rules_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': True,
                'delete_permission': True,
                # 'delete_all_permission': True
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: admin → access_rules')

        rule, created = AccessRule.objects.get_or_create(
            role=user_role,
            element=products_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': False,
                'update_permission': False,
                # 'update_all_permission': False,
                'delete_permission': False,
                # 'delete_all_permission': False
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: user → products')
            
        rule, created = AccessRule.objects.get_or_create(
            role=user_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': False,  
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': False,  
                'delete_permission': False,
                # 'delete_all_permission': False
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: user → orders')

        rule, created = AccessRule.objects.get_or_create(
            role=manager_role,
            element=products_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': True,
                'delete_permission': False,
                # 'delete_all_permission': False
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: manager → products')
            
        rule, created = AccessRule.objects.get_or_create(
            role=manager_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                # 'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                # 'update_all_permission': True,
                'delete_permission': True,
                # 'delete_all_permission': False  
            }
        )
        if created:
            self.stdout.write(f'Создано правило доступа: manager → orders')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))