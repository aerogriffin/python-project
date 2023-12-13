from django.shortcuts import render
from .forms import LogInUsers
from django.urls import reverse_lazy, reverse

def home(request):
    return render(request, "main/base.html")


def members(request):
    return render(request, "main/members.html")

def logIn( request ):
    if ( request.method == 'POST'):
        form = LogInUsers(request.POST)
        if ( form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if ( user is not None):
                if ( request.user.is_authenticated ):
                    logout(request)
                login(request, user)
                nextPage=request.GET.get('next')
                if ( nextPage is None ):
                    nextPage = reverse('home') 
                return redirect (nextPage)
            else:
                error='User or password incorrect'
                return render(request, LOGIN_USUARIOS, {'form':form, 'errorMsg':error })
        else:
            error="The data in some form field is incorrect"
            return render(request, LOGIN_USUARIOS, {'form':form, 'errorMsg':error })
    else:
        form = LogInUsers()
        if ( request.GET.get('error403') is None):
            error=None
        else:
            error='Operation not permitted. Use an account with sufficient permissions'
        return render(request, LOGIN_USUARIOS, {'form':form, 'errorMsg': error })

def logOut( request ):
    logout( request )
    return redirect ('home') 
