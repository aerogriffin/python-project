class LogInUsuarios( forms.Form):
    username = forms.CharField( label='Nombre de usuario', max_length=10, widget=forms.TextInput(attrs={'placeholder':'Nombre de usuario'}))
    password = forms.CharField( label='Contraseña', max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'contraseña'}))
