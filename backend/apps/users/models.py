"""User, Role, Department, Menu models."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.mixins import UUIDModel, SoftDeleteModel

class Department(UUIDModel, SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='部门名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='部门编码')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='上级部门')
    leader = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='led_departments', verbose_name='负责人')
    sort = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    class Meta:
        db_table = 'sys_department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['sort']
    def __str__(self): return self.name

class User(AbstractUser, UUIDModel):
    GENDER_CHOICES = (('M', '男'), ('F', '女'))
    avatar = models.URLField(max_length=500, null=True, blank=True, verbose_name='头像')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='手机号')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='性别')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name='部门')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self): return f'{self.username}({self.first_name or self.last_name})'

class Role(UUIDModel, SoftDeleteModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='角色编码')
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='描述')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    sort = models.IntegerField(default=0, verbose_name='排序')
    users = models.ManyToManyField(User, related_name='roles', blank=True, verbose_name='用户')
    menus = models.ManyToManyField('Menu', related_name='roles', blank=True, verbose_name='菜单')
    class Meta:
        db_table = 'sys_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['sort']
    def __str__(self): return self.name

class Menu(UUIDModel):
    MENU_TYPE_CHOICES = (('D', '目录'), ('M', '菜单'), ('B', '按钮'))
    name = models.CharField(max_length=50, verbose_name='菜单名称')
    code = models.CharField(max_length=100, unique=True, verbose_name='权限标识')
    menu_type = models.CharField(max_length=1, choices=MENU_TYPE_CHOICES, default='M', verbose_name='类型')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='上级菜单')
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name='路由路径')
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name='组件路径')
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='图标')
    sort = models.IntegerField(default=0, verbose_name='排序')
    is_visible = models.BooleanField(default=True, verbose_name='可见')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    class Meta:
        db_table = 'sys_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['sort']
    def __str__(self): return self.name

class OperationLog(UUIDModel):
    ACTION_CHOICES = (('CREATE', '创建'), ('UPDATE', '更新'), ('DELETE', '删除'), ('LOGIN', '登录'), ('LOGOUT', '登出'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operation_logs', verbose_name='操作人')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作类型')
    module = models.CharField(max_length=50, verbose_name='操作模块')
    detail = models.TextField(null=True, blank=True, verbose_name='操作详情')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    class Meta:
        db_table = 'sys_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    def __str__(self): return f'{self.user.username} - {self.get_action_display()} - {self.module}'
