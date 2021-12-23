from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from .forms import LoginForm, RegisterForm

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('/')

    if form.is_valid():
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')        

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name  
            user.save()          

        except:
            user = None
        
        if user != None:
            login(request, user)
            return redirect('/')
        else:
            request.session['register_error'] = 1 # 1 = True     

    return render(request, 'forms.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user != None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect('/')

        else:
            # Simple way to check amount of password attempts
            # attempt = request.session['attempt'] or 0
            # request.session['attempt'] = attempt + 1
            # return redirect('/invalid-password') # An option for incorrect password
            request.session['invalid_user'] = 1 # 1 = True            

    return render(request, 'forms.html', {'form': form})

def logout_view(request):
    logout(request)
    # request.user == Anon user
    return redirect('/login')