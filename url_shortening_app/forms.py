from django import forms
from django.contrib.auth.hashers import make_password

from .models import User, ShortenedURL


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set hashed password
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class ShortenURLForm(forms.ModelForm):

    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'custom_short_code', 'expires_at']

    def clean_custom_short_code(self):
        custom_short_code = self.cleaned_data.get('custom_short_code')
        if custom_short_code and ShortenedURL.objects.filter(custom_short_code=custom_short_code).exists():
            raise forms.ValidationError('This short code is already in use')
        return custom_short_code