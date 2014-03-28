import os

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.views import login
from django.contrib import messages
from django.conf import settings

from forms import NewSubmissionForm


def login_view(request):
	context = {
		'title': getattr(settings, 'HOMEPAGE_HEADING', 'Welcome').strip(),
		'body_text': getattr(settings, 'HOMEPAGE_TEXT', '').strip(),
		'contact_phone': getattr(settings, 'CONTACT_PHONE', '').strip(),
		'contact_email': getattr(settings, 'CONTACT_EMAIL', '').strip(),
	}
	return login(request, extra_context=context)

def logout_view(request):
	"""Logs the user out and redirects home"""
	logout(request)
	messages.success(request, "You have been logged out successfully.")
	return redirect('/login')

def index(request):
	"""Homepage, with login form"""
	return redirect('/login')

def submit(request):
	"""Submit page, with submission form"""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in before submitting.")
		return redirect('/login')

	if request.method == 'POST':
		form = NewSubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			result = form.save(request.user)
			if result:
				messages.success(request, "Your submission was successfully uploaded.")
				context = RequestContext(request)
				context['title'] = "Submission Receipt"
				context['submission_id'] = result
				return render(request, 'etd_drop_app/receipt.html', context)
			else:
				messages.error(request, "Your submission failed to process for an unknown reason. Contact the help desk or try again.")
		else:
			messages.error(request, "There were errors in your submission. Correct them and try again.")
	else:
		form = NewSubmissionForm()

	context = RequestContext(request)
	context['title'] = "New Submission"
	context['agreement'] = settings.SUBMISSION_AGREEMENT.strip()
	context['form'] = form
	return render(request, 'etd_drop_app/submit.html', context)

def submissions(request):
	"""Administrative list of bags in the bag directory"""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/login')

	submissions = []
	storage_path = os.path.abspath(settings.ETD_STORAGE_DIRECTORY)
	for subdir in os.listdir(storage_path):
		# Quickly check if this is a bag
		if True:  # TODO
			# Add to submissions
			submissions.append({
				'identifier': subdir,
				'username': subdir.split('-', 2)[-1]
			})

	context = RequestContext(request)
	context['title'] = "Submissions"
	context['submissions'] = submissions
	return render(request, 'etd_drop_app/submissions.html', context)

def submission_detail(request, id):
	"""Details for a single submission."""
	messages.info(request, "Viewing submissions is not yet implemented.")
	return redirect('/')

def submission_pdf(request, id):
	"""Direct PDF download for a single submission."""
	messages.info(request, "PDF downloads are not yet implemented.")
	return redirect('/')
