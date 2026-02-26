from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from common.Forms import RegisterForm, LoginForm
from django.views import View

# Create your views here.

class LoginView(View):
    form = LoginForm
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form()})

    def post(self, request):
        user_login = self.form(request.POST)
        user_login.is_valid()
        user = auth.authenticate(request, username=user_login.cleaned_data["login"], password=user_login.cleaned_data["password"])
        if user is not None:
            auth.login(request, user)
            return redirect("/user/" + str(user.id) + "/")
        else:
            return render(request, self.template_name, context={'error': 'wrong login or password'})


class RegisterView(View):
    template_name = 'register.html'
    form = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        user = self.form(request.POST)
        user.is_valid()
        user.save()

        return redirect('login')


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")

@login_required(login_url="login")
def user_view(request, user_id):
    user = User.objects.get(id=user_id)
    user_group = user.groups.all()[0]
    return render(request, "user_page.html", context={"user": user, "group_name": user_group.name})
