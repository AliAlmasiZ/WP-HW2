from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates default groups and permissions for Achare system'

    def handle(self, *args, **options):
        # 1. Create Groups
        contractor_group, _ = Group.objects.get_or_create(name='contractor')
        customer_group, _ = Group.objects.get_or_create(name='customer')
        support_group, _ = Group.objects.get_or_create(name='support')

        # 2. Get Permissions (Assuming models are migrated)
        try:
            # Ads Permissions
            can_apply = Permission.objects.get(codename='can_apply')
            can_assign = Permission.objects.get(codename='can_assign')
            
            # Tickets Permissions
            can_answer = Permission.objects.get(codename='can_answer_ticket')
            can_see_all = Permission.objects.get(codename='can_see_all_tickets')

            # 3. Assign Permissions to Groups
            # Contractor: Can apply for ads
            contractor_group.permissions.add(can_apply)
            
            # Customer: Can assign providers to their ads
            customer_group.permissions.add(can_assign)
            
            # Support: Can answer and manage tickets
            support_group.permissions.add(can_answer, can_see_all)

            self.stdout.write(self.style.SUCCESS('Successfully setup groups and permissions!'))
        
        except Permission.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Error: Permission not found. Please run migrations first. Details: {e}'))