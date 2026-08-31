
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from plants.models import Comment

def sign_up(request: HttpRequest):

    if request.method == 'POST':

        try:
            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name']
            )
            new_user.save()

            # Create profile for user
            profile = Profile(user=new_user,
                              about=request.POST["about"],
                              avatar=request.FILES.get("avatar", Profile.avatar.field.get_default()),
                              x_link=request.POST["x_link"])
            profile.save()


            messages.success(request, 'Account created successfully! Please sign in.', extra_tags='alert-success')
            return redirect('accounts:sign_in')

        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}", extra_tags='alert-danger')
            print(e)

    return render(request, 'accounts/signup.html', {})


def sign_in(request: HttpRequest):

    if request.method == 'POST':

        # checking user credentials
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            # Log the user in
            login(request, user)
            messages.success(request, 'Logged in successfully!', extra_tags='alert-success')
            return redirect(request.GET.get('next','/'))
        else:
            messages.error(request, 'Invalid username or password. Please try again.', extra_tags='alert-danger')

    return render(request, 'accounts/signin.html', {})

def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, 'Logged out successfully!', extra_tags='alert-success')

    return redirect(request.GET.get('next','/'))

def user_profile_view(request: HttpRequest, user_name):

    try:
        user = User.objects.get(username=user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()
        #profile: Profile = user.profile
        #profile = Profile.objects.get(user=user)

    except Exception as e:
        return render(request, 'main/404.html')


    return render(request, 'accounts/profile.html', {"user" : user})

