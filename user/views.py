from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile as Profiles
from django.contrib.auth.decorators import login_required
from . form import ProfileForm

# Create your views here.
def logReg(request): 
    if request.user.is_authenticated:
        return redirect('Home')
        
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
        
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user) 
            return redirect('Home')  
        else:
            messages.error(request, 'username or password is incorrect')     
       
    return render(request, 'user/login_register.html',)   
    
      
def logt(request):
    logout(request)
    messages.info(request, 'user loged out successfully!!')
    return redirect('Login')

@login_required(login_url='Login')
def ProfileEdit(request, pk):
    profile=Profiles.objects.get(id=pk)
    prof=Profiles.objects.all()
    profil=ProfileForm(instance=profile)
    
    if request.method == "POST":
        profil=ProfileForm(request.POST, instance=profile)
        if profil.is_valid():
            profil.save()
            return redirect('Profile')
    
    context={
        'profile':profil,
        'prof':prof,
        'profiles':prof,
    }
    return render(request, 'user/ProfileEdit.html', context)
     

@login_required(login_url='Login')
def Profile(request):
    profiles=Profiles.objects.all()
    profile=ProfileForm()
    
    if request.method == "POST":
        profile=ProfileForm(request.POST)
        if profile.is_valid():
            profile.save()
            return redirect('Profile')
    
    context={
        'profile':profile,
        'profiles':profiles
    }
    return render(request, 'user/profile.html', context)


def Nav(request):
    profiles=Profiles.objects.all()
    context={
        'profiles':profiles
    }
    return render(request, 'user/nav.html', context)
     