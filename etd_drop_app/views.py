from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib import messages


def logout_view(request):
	'''Logs the user out and redirects home'''
	logout(request)
	messages.success(request, "You have been logged out successfully.")
	return redirect('/login')

def index(request):
	'''Homepage, with login form'''
	return redirect('/login')

def submit(request):
	'''Submit page, with submission form'''
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in before submitting.")
		return redirect('/login')
	context = RequestContext(request)
	context['title'] = "New Submission"
	return render(request, 'etd_drop_app/submit.html', context)

def submissions(request):
	'''Administrative list of bags in the bag directory'''
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/login')
	context = RequestContext(request)
	context['title'] = "Submissions"

	# Do work
	messages.info(request, "The code for doing this isn't here yet.")
	submissions = []

	context['submissions'] = submissions
	return render(request, 'etd_drop_app/submissions.html', context)