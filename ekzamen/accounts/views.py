from django.shortcuts import render, redirect
from .forms import UserCreateForm, UserAuthenticationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def user_register_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    
    else:
        form = UserCreateForm()
    return render(request, 'auth/register.html', {'form': form})

def user_login_view(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            
    else:
        form = UserAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})
    
def user_logout_view(request):
    logout(request)
    return redirect('login')    
