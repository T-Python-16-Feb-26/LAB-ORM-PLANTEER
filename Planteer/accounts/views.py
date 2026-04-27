from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import SignUpForm, SignInForm


def sign_up(request):
	if request.user.is_authenticated:
		return redirect('main:home')

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				email=form.cleaned_data['email'],
				password=form.cleaned_data['password'],
			)
			login(request, user)
			return redirect('main:home')
	else:
		form = SignUpForm()

	return render(request, 'accounts/signup.html', {'form': form})


def sign_in(request):
	if request.user.is_authenticated:
		return redirect('main:home')

	form = SignInForm(request.POST or None)
	error_message = None

	if request.method == 'POST' and form.is_valid():
		user = authenticate(
			request,
			username=form.cleaned_data['username'],
			password=form.cleaned_data['password'],
		)
		if user is not None:
			login(request, user)
			return redirect('main:home')
		error_message = 'Invalid username or password'

	return render(request, 'accounts/signin.html', {
		'form': form,
		'error_message': error_message,
	})


def log_out(request):
	logout(request)
	return redirect('main:home')
