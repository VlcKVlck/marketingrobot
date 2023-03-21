from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def index(request):
    if request.user.is_authenticated:
        return redirect('/campaigns')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not password or not username:
        return render(request, 'index.html')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "Login successful." )
        return redirect('/campaigns')
    else:
        print("invalid login",username,  password)
        messages.error(request, "Unsuccessful sign in. Invalid information.\n" )
    return render(request, 'index.html')
    

def logout_view(request):
    logout(request)
    return redirect('/')