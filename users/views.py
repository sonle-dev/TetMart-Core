from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

# LOGIC ĐĂNG KÝ
def register_view(request):
    if request.method == 'POST':
        
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            messages.success(request, f"Chào mừng {user.username} đến với TetMart!")
            return redirect('home') 
    else:
      
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

#  LOGIC ĐĂNG NHẬP
def login_view(request):
    if request.method == 'POST':
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            messages.success(request, "Đăng nhập thành công!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

# LOGIC ĐĂNG XUẤT
def logout_view(request):
    logout(request) 
    return redirect('home')
