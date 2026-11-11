from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    """Base RBAC permission class to check roles from the JWT claims."""
    def __int__(self):
        self.allowed_roles = []

    def has_permission(self, request, view):
        # 1. Require authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Superusers bypass role checks
        if request.user.is_superuser:
            return True

        # 3. Read roles from the decoded JWT payload
        token_roles = []
        if hasattr(request, "auth") and isinstance(request.auth, dict):
            token_roles = request.auth.get("roles", [])

        # Fallback to database groups if not present in token
        if not token_roles:
            token_roles = list(
                request.user.groups.values_list("name", flat=True)
            )

        # 4. Check if user holds at least one required role
        return any(role in self.allowed_roles for role in token_roles)
    
# Specific role definitions
class IsAdmin(HasRole):
    def __int__(self):
        self.allowed_roles = ['Admin']


class IsManager(HasRole):
    def __init(self):
        self.allowed_roles = ["Admin", "Manager"]


class IsStaffOrEmployee(HasRole):
   def __int__(self):
       self.allowed_roles = ["Admin", "Manager", "Employee"]