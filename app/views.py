import random
from django.shortcuts import render,redirect
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
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
    request.session.modified = True
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('pw')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username']= username
            # return render(request, 'home.html', {'user':user} )
            return redirect('home')
        else:
            return HttpResponse('Invalid Credentials')
    return render(request, 'user_login.html')

def user_logout(request):
    logout(request)
    return render(request, 'home.html')

# def user_profile(request):
#     profile = Profile.objects.get(username=request.session)
#     return render(request, 'user_profile.html',{'profile':profile})
def user_profile(request):
    try:
        un = request.session['username']
        user = User.objects.get(username=un)
        d = {
            'UO':user
        }
        request.session.modified = True
        return render(request, 'user_profile.html', d)
    except:
        # return render(request, 'user_login.html')
        return redirect('user_login')
    
def change_password(request):
    username = request.session['username']
    user = User.objects.get(username = username)
    context ={
        'user': user
    }
    email = user.get('email')
    # print(user.email)
    if request.method == "POST":
        newpassword = request.POST.get('newpassword')
        Cnewpassword = request.POST.get('Cnewpassword')
        otp = random.randint(1000,9999)
        # print(user.email)
        message = f"Your Otp is {otp} is valid for 3 mimnutes"
        if newpassword == Cnewpassword:
            send_mail(
                'OTP for change Password',
                message,
                'das.15122003@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['otp'] = otp
            request.session['newpassword'] = newpassword
            return redirect('otp_verification')
        else:
            return HttpResponse("dont match")
        

    return render(request, 'change_password.html')


def otp_verification(request):
    otp = request.session['otp']
    newpassword = request.session['newpassword']

    username = request.session['username']
    user = User.objects.get(username = username)

    print(newpassword)
    if request.method == "POST":
        verify_otp = request.POST.get('otp')
        print(type(verify_otp), "enter otp")
        print(otp, "session otp")
        if otp == int(verify_otp):
            user.set_password(newpassword)
            user.save()
            print("Password changed successfully")
            return redirect('user_login')
        else:
            return HttpResponse("Otp not matching")
    return render(request, 'otp_verification.html')


def forgot_password(request):
    try:
        if request.method == 'POST':
            un = request.POST.get('username')
            user = User.objects.get(username = un)
            print(user.email)
            if user:

                otp = random.randint(1000,9999)
                message = f"Your Otp is {otp} is valid for 3 mimnutes"
                send_mail(
                    'OTP for change Password',
                    message,
                    'das.15122003@gmail.com',
                    [user.email],
                    fail_silently=False,
                )

                request.session['otp']  = otp
                request.session['username'] = user.username
                return render(request, 'forgot_password_otp.html')
                # return redirect('forgot_password_otp')
    except:    
        return HttpResponse("User not found")
    

            # messages.error("user does not exist")
            # return redirect('forgot_password')
                
    return render(request, 'forgot_password.html')

def forgot_password_otp(request):
    GOTP = request.session['otp']
    if request.method == "POST":
        GOTP = request.session['otp']
        UOTP = request.POST.get('otp')

        if str(GOTP) == UOTP:
            return render(request, 'forgot_password_update.html')
        
        return HttpResponse("Otp not matching")

            
    return render(request, 'forgot_password_otp.html')

def forgot_password_update(request):
    return render(request, 'forgot_password_update.html')