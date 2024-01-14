from django.shortcuts import render,HttpResponse,redirect
from django import forms
from web import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "输入用户名"}),
        # validators=[RegexValidator(r'^\w{6,}$', '用户名格式错误')]
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "输入密码"}, render_value=True),
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "输入验证码"}),
    )
# Create your views here.
def login(request):
    """用户登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {"form":form})
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})
    image_code = request.session.get("image_code")
    if not image_code:
        form.add_error("code","验证码过期")
        return render(request, "login.html", {"form": form})
    if image_code.upper() != form.cleaned_data["code"].upper():
        form.add_error("code", "验证码错误")
        return render(request, "login.html", {"form": form})
    pwd = form.cleaned_data["password"]
    from utils.encrypt import md5
    encrypt_password = md5(pwd)
    print(encrypt_password)
    admin_object = models.Admin.objects.filter(username=form.cleaned_data["username"], password= encrypt_password).first()
    if not admin_object:
        return render(request, "login.html", {"form": form, "error":"用户名或密码错误"})

    request.session['info'] = {"id": admin_object.id, "name": admin_object.username}
    request.session.set_expiry(60 * 60 * 24 * 7)
    return redirect("/home/")







from utils.helper import check_code
from io import BytesIO
def img_code(request):
    image_object, code_str = check_code()
    stream = BytesIO()
    image_object.save(stream, 'png')
    request.session['image_code'] = code_str
    request.session.set_expiry(60)

    return HttpResponse(stream.getvalue())


def home(request):
    return render(request, "home.html")


def logout(request):
    request.session.clear()
    return redirect("/login/")