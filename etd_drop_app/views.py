from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib import messages


def logout_view(request):
	'''Logs the user out and redirects home'''
	logout(request)
	messages.success(request, "You have been logged out successfully.")
	return redirect('/')

def index(request):
	'''Homepage, with login form'''
	context = RequestContext(request)
	context['title'] = "Welcome"
	return render(request, 'etd_drop_app/index.html', context)

def submit(request):
	'''Submit page, with submission form'''
	context = RequestContext(request)
	context['title'] = "Submit an ETD"
	return render(request, 'etd_drop_app/submit.html', context)