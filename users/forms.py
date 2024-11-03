from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, DriverLicense, DriverLicenseCategory


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists')
        return email

    def save(self, commit=True) -> User:
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # check if user with this email exists
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email or password is incorrect')

        # check if the password is correct
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise forms.ValidationError('Email or password is incorrect')

        return self.cleaned_data


class DriverLicenseForm(forms.ModelForm):
    class Meta:
        model = DriverLicense
        fields = ['surname', 'name_patronymic', 'iin', 'date_of_issue', 'date_of_expiry', 'license_number', 'photo',
                  'category']

    def clean_iin(self):
        iin = self.cleaned_data.get('iin')
        if DriverLicense.objects.filter(iin=iin).exists():
            raise forms.ValidationError('Driver license with this IIN already exists')
        return iin
