from django.shortcuts import render,redirect
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from app.models import Profile
# Create your views here.


def register(request):
    EUFO = UserForm()
    EPFO = ProfileForm()

    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            pw = UFDO.cleaned_data.get('password')
            MUFDO = UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO = PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            message = f"Hello {UFDO.cleaned_data.get('first_name')} your registration completed"
            email = UFDO.cleaned_data.get('email')
            send_mail(
                'Registration Successfull',
                message,
                'das.15122003@gmail.com',
                [email],
                fail_silently=False,
            )
            return HttpResponse('registration is Done')
        return HttpResponse('Invalid Data')
    context = {
        'EUFO':EUFO,
        'EPFO':EPFO,
    }

    return render(request, 'register.html',context)
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('pw')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # return render(request, 'home.html', {'user':user} )
            return redirect('home')
        else:
            return HttpResponse('Invalid Credentials')
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return render(request, 'home.html')

def user_profile(request):
    profile = Profile.objects.get(username=request.user)
    return render(request, 'user_profile.html',{'profile':profile})