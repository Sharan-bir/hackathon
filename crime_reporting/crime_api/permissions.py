from rest_framework import permissions
from crime_api.models import PoliceStation

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 1

class IsPolice(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 2

class IsDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 3

class IsPoliceOrDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type in [2, 3]

class IsReportOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsStationHead(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or request.user.user_type != 2:
            return False
        return PoliceStation.objects.filter(head=request.user).exists()