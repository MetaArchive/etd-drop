from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	# / (Home page)
	url(r'^$', 'etd_drop_app.views.index', name='index'),

	# /login
    url(r'^login$', 'django.contrib.auth.views.login', {'extra_context': {'title': 'Log In'}}),
    # /logout
    url(r'^logout$', 'etd_drop_app.views.logout_view'),

    # /submit
    url(r'^submit$', 'etd_drop_app.views.submit'),

    # /submissions (staff only)
    url(r'^submissions$', 'etd_drop_app.views.submissions'),
)