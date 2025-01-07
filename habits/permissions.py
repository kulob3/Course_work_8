from rest_framework import permissions

class IsOwnerOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.is_public:
            return True
        return obj.user == request.user