"""Serializers for users app."""
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.users.models import Department, Menu, OperationLog, Role, User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user: raise serializers.ValidationError('用户名或密码错误')
        if not user.is_active: raise serializers.ValidationError('用户已被禁用')
        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']: raise serializers.ValidationError({'confirm_password': '两次密码不一致'})
        return attrs
    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value): raise serializers.ValidationError('原密码不正确')
        return value

class DepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta: model = Department; fields = ['id', 'name', 'code']

class RoleSimpleSerializer(serializers.ModelSerializer):
    class Meta: model = Role; fields = ['id', 'name', 'code']

class UserSerializer(serializers.ModelSerializer):
    department_info = DepartmentSimpleSerializer(source='department', read_only=True)
    roles_info = RoleSimpleSerializer(source='roles', many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(source='roles', queryset=Role.objects.all(), many=True, write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=6)
    class Meta:
        model = User
        fields = ['id','username','first_name','email','phone','avatar','gender','department','department_info','is_active','is_staff','roles_info','role_ids','password','date_joined','created_at','updated_at','remark']
        extra_kwargs = {'password': {'write_only': True}}
    def validate_password(self, value): return make_password(value)
    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        if 'password' not in validated_data: validated_data['password'] = make_password('123456')
        user = User.objects.create(**validated_data)
        if roles: user.roles.set(roles)
        return user
    def update(self, instance, validated_data):
        roles = validated_data.pop('roles', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items(): setattr(instance, attr, value)
        if password: instance.password = password
        instance.save()
        if roles is not None: instance.roles.set(roles)
        return instance

class UserListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True, default='')
    class Meta: model = User; fields = ['id','username','first_name','email','phone','department_name','is_active','date_joined']

class MenuTreeNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta: model = Menu; fields = ['id','name','code','menu_type','path','component','icon','sort','is_visible','children']
    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('sort')
        return MenuTreeNodeSerializer(children, many=True).data if children else []

class RoleSerializer(serializers.ModelSerializer):
    user_count = serializers.IntegerField(source='users.count', read_only=True, default=0)
    menu_ids = serializers.PrimaryKeyRelatedField(source='menus', queryset=Menu.objects.all(), many=True, write_only=True, required=False)
    class Meta: model = Role; fields = ['id','name','code','description','is_active','sort','user_count','menu_ids','created_at']
    def create(self, validated_data):
        menus = validated_data.pop('menus', [])
        role = Role.objects.create(**validated_data)
        if menus: role.menus.set(menus)
        return role
    def update(self, instance, validated_data):
        menus = validated_data.pop('menus', None)
        for attr, value in validated_data.items(): setattr(instance, attr, value)
        instance.save()
        if menus is not None: instance.menus.set(menus)
        return instance

class DepartmentTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta: model = Department; fields = ['id','name','code','sort','is_active','leader','children']
    def get_children(self, obj):
        children = obj.children.filter(is_deleted=False).order_by('sort')
        return DepartmentTreeSerializer(children, many=True).data if children else []

class DepartmentSerializer(serializers.ModelSerializer):
    leader_name = serializers.CharField(source='leader.username', read_only=True, default='')
    class Meta: model = Department; fields = ['id','name','code','parent','leader','leader_name','sort','is_active','created_at']

class MenuSerializer(serializers.ModelSerializer):
    class Meta: model = Menu; fields = ['id','name','code','menu_type','parent','path','component','icon','sort','is_visible','is_active']

class OperationLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta: model = OperationLog; fields = ['id','username','action','module','detail','ip_address','created_at']
