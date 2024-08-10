from datetime import timedelta
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm,otp
from django.contrib.auth import  login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.db.models.signals import post_save
from django.utils import timezone

def home(request):
    return render(request, 'user/home.html')

def generate_otp():
    otp_num = random.randint(1000, 9999)
    return otp_num
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password1'])
            )
            request.session['user_id'] = user.id
            otp_num=generate_otp()
            print(otp_num)
            request.session['otp_num'] = otp_num
            UserProfile.objects.create(user=user,otp_code=otp_num,otp_created_at=timezone.now())
            #post_save.send(sender=UserProfile, instance=user, created=True)
            
            print('user_data',user)
            return redirect('otp')  
        else:
            #
            return render(request, 'user/signup.html', {'form': form})
    else:
        
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form': form})

def otpw(request):
    if request.method == 'POST':
        form = otp(request.POST)
        if form.is_valid():
             user_id = request.session.get('user_id')
             print("user_id",user_id)
             user=get_object_or_404(UserProfile, id=user_id)
             print("user",user)
             otp_new = str(form.cleaned_data['code'])
             
             print("otp_new",otp_new)
             old_otp = str(request.session.get('otp_num'))
             print("old_otp",old_otp)
             otp_valid=(user.otp_code == old_otp and user.otp_created_at>=timezone.now()-timedelta(minutes=15))
             if  otp_valid:
                 print("succes")
                 if user is not None:
                     print("user not none")
                     login(request,user)
                     print("user saved")
                     Refresh_token=RefreshToken.for_user(user)#test
                     access_token=str(Refresh_token.access_token)
                     print(access_token)
                     print(Refresh_token)
                     response=redirect('home')##change when u need
                     response.set_cookie('access_token',access_token,httponly=True,samesite='None',secure=True)
                     response.set_cookie('refresh_token',str(Refresh_token),httponly=True,samesite='None',secure=True)
                     print("token set")
                     request.session.pop('otp_num', None)
                    
                     print('poopes')
                     return  response# Redirect to a success page or another view
                 else :
                     return render(request,'user/signup.html',{'form': form, 'error': 'no user'})
             else:
                    return render(request, 'user/otp.html', {'form': form, 'error': 'Invalid OTP'})
        else:
              return render(request, 'user/otp.html', {'form': form})      
    else:
         form = otp()
         return render(request, 'user/otp.html', {'form': form})                
              
def home(request):
    # Example of checking if a user is authenticated
    if request.user.is_authenticated:
        return render(request, 'user/home.html')
    else:
        return render(request,{"message":"please login"}, 'user/home.html')


