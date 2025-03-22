from rest_framework import permissions


class IsCandidat(permissions.BasePermission):
    """
    Permission personnalisée pour restreindre l'accès aux candidats
    """

    def has_permission(self, request, view):
        return request.user.role == "candidat" and request.user.is_authenticated


class IsRecruteur(permissions.BasePermission):
    """
    Permission personnalisée pour restreindre l'accès aux recruteurs
    """

    def has_permission(self, request, view):
        return request.user.role == "recruteur" and request.user.is_authenticated
