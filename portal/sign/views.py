from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.views import View
from django.contrib.auth.forms import AuthenticationForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/index.html'


class LoginFormView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'sign/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            # Добавьте свою логику для обработки введенных данных формы
            return render(request, 'success.html')
        return render(request, 'sign/login.html', {'form': form})


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('news/')
