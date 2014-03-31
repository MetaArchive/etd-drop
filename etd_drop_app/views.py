import os
import json

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.views import login
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.servers.basehttp import FileWrapper

from forms import NewSubmissionForm


class DefaultContext(RequestContext):
	def __init__(self, request):
		super(DefaultContext, self).__init__(request)
		self['footer_text'] = settings.FOOTER_TEXT.strip()

def login_view(request):
	context = {
		'title': getattr(settings, 'HOMEPAGE_HEADING', 'Welcome').strip(),
		'body_text': getattr(settings, 'HOMEPAGE_TEXT', '').strip(),
		'contact_phone': getattr(settings, 'CONTACT_PHONE', '').strip(),
		'contact_email': getattr(settings, 'CONTACT_EMAIL', '').strip(),
		'footer_text': settings.FOOTER_TEXT.strip(),
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
				context = DefaultContext(request)
				context['title'] = "Submission Receipt"
				context['submission_id'] = result
				return render(request, 'etd_drop_app/receipt.html', context)
			else:
				messages.error(request, "Your submission failed to process for an unknown reason. Contact the help desk or try again.")
		else:
			messages.error(request, "There were errors in your submission. Correct them and try again.")
	else:
		form = NewSubmissionForm()

	context = DefaultContext(request)
	context['title'] = "New Submission"
	context['agreement'] = settings.SUBMISSION_AGREEMENT.strip()
	context['field_settings'] = settings.SUBMISSION_FORM_FIELDS
	context['form'] = form
	return render(request, 'etd_drop_app/submit.html', context)

def submissions(request):
	"""Administrative list of bags in the bag directory"""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/')

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
	submissions.sort(key=lambda x: x['identifier'], reverse=True)

	context = DefaultContext(request)
	context['title'] = "Submissions"
	context['submissions'] = submissions
	return render(request, 'etd_drop_app/submissions.html', context)

def submission_detail(request, id):
	"""Details for a single submission."""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/')

	storage_path = os.path.abspath(settings.ETD_STORAGE_DIRECTORY)
	json_path = os.path.join(storage_path, id, 'data', 'form.json')
	if os.path.isfile(json_path):
		# Load JSON
		with open(json_path, 'r') as json_file:
			json_dict = json.load(json_file)

		# Get bag tag files
		info_path = os.path.join(storage_path, id, 'bag-info.txt')
		with open(info_path, 'r') as info_file:
			info_string = info_file.read()
		manifest_path = os.path.join(storage_path, id, 'manifest-md5.txt')
		with open(manifest_path, 'r') as manifest_file:
			manifest_string = manifest_file.read()

		context = DefaultContext(request)
		context['title'] = "Submission Details"
		context['submission_id'] = id
		context['submission'] = json_dict
		context['bag_info'] = info_string
		context['bag_manifest'] = manifest_string
		return render(request, 'etd_drop_app/submission_detail.html', context)
	else:
		raise Http404

def submission_pdf(request, id):
	"""Direct PDF download for a single submission."""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/')

	storage_path = os.path.abspath(settings.ETD_STORAGE_DIRECTORY)
	pdf_path = os.path.join(storage_path, id, 'data', 'etd.pdf')
	if os.path.isfile(pdf_path):
		# Serve the file
		wrapper = FileWrapper(file(pdf_path))
		response = HttpResponse(wrapper, content_type='application/pdf')
		response['Content-Length'] = os.path.getsize(pdf_path)
		return response
	else:
		raise Http404

def submission_json(request, id):
	"""Direct JSON download for a single submission."""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/')

	storage_path = os.path.abspath(settings.ETD_STORAGE_DIRECTORY)
	file_path = os.path.join(storage_path, id, 'data', 'form.json')
	if os.path.isfile(file_path):
		# Serve the file
		wrapper = FileWrapper(file(file_path))
		response = HttpResponse(wrapper, content_type='application/json')
		response['Content-Length'] = os.path.getsize(file_path)
		return response
	else:
		raise Http404

def submission_contents(request, id, path):
	"""Download a file from the submission directory under the given
	path"""
	if not request.user.is_authenticated():
		messages.warning(request, "You must log in to view this page.")
		return redirect('/login')
	if not request.user.is_staff:
		messages.warning(request, "Forbidden.")
		return redirect('/')

	if '..' in path:
		raise Http404

	storage_path = os.path.abspath(settings.ETD_STORAGE_DIRECTORY)
	file_path = os.path.join(storage_path, id, path)
	if os.path.isfile(file_path):
		# Serve the file
		wrapper = FileWrapper(file(file_path))
		content_type = 'application/octet-stream'
		lowerpath = path.lower()
		if lowerpath.endswith('.pdf'):
			content_type = 'application/pdf'
		elif lowerpath.endswith('.json'):
			content_type = 'application/json'
		response = HttpResponse(wrapper, content_type=content_type)
		response['Content-Length'] = os.path.getsize(file_path)
		return response

	raise Http404
