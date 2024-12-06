from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


DEFAULT_MENU = {
    'homeInfo': {
        'title': '首页',
        'href': 'home',
    },
    'logoInfo': {
        'title': 'MySOC平台',
        'image': '/static/console/img/logo.png',
        'href': '',
    },
    'menuInfo': [
        {
            "title": "主页",
            "icon": "layui-icon layui-icon-home",
            "href": "home",
        },
    ],
}


# Create your views here.
def console_layout(request):
    return render(request, 'console/layout.html')


def console_menu(request):
    return JsonResponse(DEFAULT_MENU)


def console_home(request):
    return render(request, 'console/home.html')


def console_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'code': 0, 'msg': '登录成功'})
        else:
            return JsonResponse({'code': 1, 'msg': '用户名或密码错误'})

    return render(request, 'console/login.html')


def console_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
