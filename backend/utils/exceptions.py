"""Custom exception handler."""
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        msgs = {400:'请求参数有误',401:'未认证，请先登录',403:'没有权限执行此操作',404:'请求的资源不存在',405:'不支持的请求方法',500:'服务器内部错误'}
        response.data = {'code': response.status_code, 'message': msgs.get(response.status_code,'未知错误'), 'errors': response.data}
    return response
