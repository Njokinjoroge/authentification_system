from permissions_app.models import BusinessElement, AccessRoleRule

def check_permission(user, element_name, action):
    """
    Check if a user has permission to perform an action on a business element.
    action: read, read_all, create, update, update_all, delete, delete_all
    """
    if not user or not user.role:
        return False

    try:
        element = BusinessElement.objects.get(name=element_name)
        rule = AccessRoleRule.objects.get(role=user.role, element=element)
    except (BusinessElement.DoesNotExist, AccessRoleRule.DoesNotExist):
        return False

    permission_field = f"{action}_permission" if action.endswith("_all") else f"{action}_permission"
    return getattr(rule, permission_field, False)
