import os
import random
import string

from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from user.forms import RegisterForm, UserAuthenticationForm, UserProfilForm, ResetPasswordForm
from user.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.save()
        # Создаем и сохраняем токен подтверждения
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        new_user.email_verification_token = token
        new_user.save()
        # Отправляем письмо с подтверждением
        current_site = get_current_site(self.request)
        mail_subject = ('Подтвердите ваш аккаунт. '
                        'Пройдите по этой ссылке для подтверждения регистрации:')
        message = render_to_string(
            'user/email_verified.html',
            {
                'domain': current_site.domain,
                'token': token,
            },
        )
        send_mail(mail_subject, message, os.getenv('EMAIL_HOST_USER'), [new_user.email])
        return response


class VerifyEmailView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.email_verified = True
            user.save()
            return redirect('user:login')  # Редирект на страницу входа
        except User.DoesNotExist:
            return HttpResponse('Неверная ссылка подтверждения.')


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data.get('username'))
        if user.email_verified:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Подтвердите пожалуйста свою почту')
            return self.form_invalid(form)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfilForm
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'user/user_form.html', {'form': form})

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        # Отправляем письмо с подтверждением
        current_site = get_current_site(self.request)
        mail_subject = ('Сброс пароля')
        message = render_to_string(
            'user/password_reset.html',
            {
                'domain': current_site.domain,
                'token': user.email_verification_token,
            },
        )
        send_mail(mail_subject, message, os.getenv('EMAIL_HOST_USER'), [user.email])
        return redirect('user:login')


class ConfirmPasswordResetView(View):
    def get(self, request, token):
        user = User.objects.get(email_verification_token=token)
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.set_password(new_password)
        user.save()
        return render(request, 'user/confirm_password_reset.html',
                      {'new_password': new_password})
