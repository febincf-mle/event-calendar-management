from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def loginPage(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            return render(request, 'eventmanagement/login.html', context={ 'error': 'user does not exist' })
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'eventmanagement/login.html', context={ 'error': 'username and password doesnt match' })
        

    elif request.method == 'GET':
        return render(request, 'eventmanagement/login.html')
    


def registerUser(request):
            
    form = UserCreationForm()
    
    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        print(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)

            return redirect('home')
        
        else:
            render(request, 'eventmanagement/register.html', { 'error': 'something went wrong' })

    return render(request, 'eventmanagement/register.html', { 'form': form })



@login_required
def logoutUser(request):
    logout(request)
    return redirect("login")