from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import Department, Menu, OperationLog, Role, User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username','first_name','email','phone','department','is_active','is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (('扩展信息',{'fields':('phone','gender','department','avatar','remark')}),)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin): list_display = ['name','code','is_active','sort']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin): list_display = ['name','code','parent','leader','is_active','sort']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin): list_display = ['name','code','menu_type','parent','path','sort','is_visible','is_active']

@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ['user','action','module','ip_address','created_at']
    list_filter = ['action','module']
    search_fields = ['user__username','detail']
