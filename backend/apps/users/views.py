"""Views for users app."""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import Department, Menu, OperationLog, Role, User
from apps.users.serializers import *

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ip = x_forwarded.split(',')[0].strip() if x_forwarded else request.META.get('REMOTE_ADDR', '')
        OperationLog.objects.create(user=user, action='LOGIN', module='认证', ip_address=ip)
        return Response({'code':200,'message':'登录成功','data':{'access':str(refresh.access_token),'refresh':str(refresh),'user':UserSerializer(user).data}})

class CurrentUserView(APIView):
    def get(self, request): return Response({'code':200,'data':UserSerializer(request.user).data})
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code':200,'message':'更新成功','data':serializer.data})

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'code':200,'message':'密码修改成功'})

class UserViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related('roles','department').all()
    filterset_fields = ['is_active','department_id']
    search_fields = ['username','first_name','email','phone']
    ordering_fields = ['created_at','date_joined']
    ordering = ['-date_joined']
    def get_serializer_class(self): return UserListSerializer if self.action == 'list' else UserSerializer
    @action(detail=False, methods=['put'], url_path='batch-status')
    def batch_status(self, request):
        ids = request.data.get('ids', [])
        is_active = request.data.get('is_active', True)
        User.objects.filter(id__in=ids).update(is_active=is_active)
        return Response({'code':200,'message':'批量更新成功'})

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_fields = ['is_active']
    search_fields = ['name','code']
    @action(detail=True)
    def menus(self, request, pk=None):
        role = self.get_object()
        menu_ids = list(role.menus.values_list('id', flat=True))
        return Response({'code':200,'data':{'role_id':role.id,'menu_ids':menu_ids}})
    @action(detail=False)
    def all_menus(self, request):
        roots = Menu.objects.filter(parent__isnull=True, is_active=True).order_by('sort')
        return Response({'code':200,'data':MenuTreeNodeSerializer(roots, many=True).data})

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer
    filterset_fields = ['is_active']
    search_fields = ['name','code']
    ordering = ['sort']
    @action(detail=False)
    def tree(self, request):
        roots = Department.objects.filter(parent__isnull=True, is_deleted=False).order_by('sort')
        return Response({'code':200,'data':DepartmentTreeSerializer(roots, many=True).data})
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted','deleted_at'])

class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.filter(is_active=True)
    serializer_class = MenuSerializer
    ordering = ['sort']
    @action(detail=False)
    def tree(self, request):
        roots = Menu.objects.filter(parent__isnull=True, is_active=True).order_by('sort')
        return Response({'code':200,'data':MenuTreeNodeSerializer(roots, many=True).data})
    @action(detail=False)
    def user_menus(self, request):
        user = request.user
        if user.is_superuser:
            menus = Menu.objects.filter(is_active=True, is_visible=True)
        else:
            role_ids = user.roles.values_list('id', flat=True)
            menus = Menu.objects.filter(roles__in=role_ids, is_active=True, is_visible=True).distinct()
        roots = menus.filter(parent__isnull=True).order_by('sort')
        return Response({'code':200,'data':MenuTreeNodeSerializer(roots, many=True).data})

class OperationLogListView(ListAPIView):
    queryset = OperationLog.objects.select_related('user').all()
    serializer_class = OperationLogSerializer
    filterset_fields = ['action','module']
    search_fields = ['user__username','detail']
    ordering = ['-created_at']
