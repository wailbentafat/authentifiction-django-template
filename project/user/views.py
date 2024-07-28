from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
def home(request):
    return render(request, 'user/home.html')

def signup(request):##craeteuser
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.check_passwords()
            form.user_exists()
            code=form.email_exists()
            render( 'user/otp.html', {'form': form,'code':code})
        else:
         form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})
    
    
    
