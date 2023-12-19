from django import forms


class LogInUsers(forms.Form):
    username = forms.CharField(label="User", max_length=10, widget=forms.TextInput(attrs={"placeholder": "user"}))
    password = forms.CharField(
        label="Password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "password"}),
    )
