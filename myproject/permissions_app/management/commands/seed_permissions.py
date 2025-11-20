from django.core.management.base import BaseCommand
from users.models import User
from permissions_app.models import Role, BusinessElement, AccessRoleRule


class Command(BaseCommand):
    help = "Seed initial roles, business elements, permissions, and test users."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # ---------------------------------------------------------
        # Create Roles
        # ---------------------------------------------------------
        admin_role, _ = Role.objects.get_or_create(name="admin")
        manager_role, _ = Role.objects.get_or_create(name="manager")
        viewer_role, _ = Role.objects.get_or_create(name="viewer")

        # ---------------------------------------------------------
        # Create Business Elements
        # ---------------------------------------------------------
        business_objects, _ = BusinessElement.objects.get_or_create(name="business_objects")
        user_management, _ = BusinessElement.objects.get_or_create(name="user_management")

        # ---------------------------------------------------------
        # Access Rules (using correct field = element)
        # ---------------------------------------------------------

        # ADMIN: full access on everything
        AccessRoleRule.objects.get_or_create(
            role=admin_role,
            element=business_objects,
            defaults={
                "read_permission": True,
                "create_permission": True,
                "update_permission": True,
                "delete_permission": True,
                "read_all_permission": True,
                "update_all_permission": True,
                "delete_all_permission": True,
            }
        )

        AccessRoleRule.objects.get_or_create(
            role=admin_role,
            element=user_management,
            defaults={
                "read_permission": True,
                "create_permission": True,
                "update_permission": True,
                "delete_permission": True,
                "read_all_permission": True,
                "update_all_permission": True,
                "delete_all_permission": True,
            }
        )

        # MANAGER: read/write business objects
        AccessRoleRule.objects.get_or_create(
            role=manager_role,
            element=business_objects,
            defaults={
                "read_permission": True,
                "create_permission": True,
                "update_permission": True,
                "delete_permission": False,
                "read_all_permission": False,
                "update_all_permission": False,
                "delete_all_permission": False,
            }
        )

        # VIEWER: read-only business objects
        AccessRoleRule.objects.get_or_create(
            role=viewer_role,
            element=business_objects,
            defaults={
                "read_permission": True,
                "create_permission": False,
                "update_permission": False,
                "delete_permission": False,
                "read_all_permission": False,
                "update_all_permission": False,
                "delete_all_permission": False,
            }
        )

        # ---------------------------------------------------------
        # Create Test Users
        # ---------------------------------------------------------

        if not User.objects.filter(email="admin@example.com").exists():
            user = User.objects.create_superuser(
                email="admin@example.com",
                password="admin123",
                first_name="Admin",
                last_name="User"
            )
            user.role = admin_role
            user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user"))

        if not User.objects.filter(email="manager@example.com").exists():
            user = User.objects.create_user(
                email="manager@example.com",
                password="manager123",
                first_name="Manager",
                last_name="User"
            )
            user.role = manager_role
            user.save()
            self.stdout.write(self.style.SUCCESS("Created manager user"))

        if not User.objects.filter(email="viewer@example.com").exists():
            user = User.objects.create_user(
                email="viewer@example.com",
                password="viewer123",
                first_name="Viewer",
                last_name="User"
            )
            user.role = viewer_role
            user.save()
            self.stdout.write(self.style.SUCCESS("Created viewer user"))

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
