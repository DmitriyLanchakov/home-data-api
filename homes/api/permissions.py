from rest_framework import permissions

class SignUpPermission(permissions.BasePermission):
    """ Only allows POST methods from non authenticated users.
    """
    message = "Endpoint only allows a POST form a non authenticated user."

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated():
            return True
        return False


class UserConfirmedPermission(permissions.BasePermission):
    """ Only allows users to take action if they have confirmed their account.
    """
    message = "Account not confirmed."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated():
            return request.user.profile.confirmed
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated():
            return request.user.profile.confirmed
        else:
            return False
