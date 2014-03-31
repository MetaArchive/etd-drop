from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
	# / (Home page)
	url(r'^$', 'etd_drop_app.views.index', name='index'),

	# /login
    url(r'^login$', 'etd_drop_app.views.login_view'),
    # /logout
    url(r'^logout$', 'etd_drop_app.views.logout_view'),

    # /submit
    url(r'^submit$', 'etd_drop_app.views.submit'),

    # /submissions (staff only)
    url(r'^submissions$', 'etd_drop_app.views.submissions'),

    # /submissions/[ID]/contents/[path] (staff only)
    url(r'^submissions/(?P<id>.+)/contents/(?P<path>.+)$', 'etd_drop_app.views.submission_contents'),
    # /submissions/[ID].pdf (staff only)
    url(r'^submissions/(?P<id>.+)\.pdf$', 'etd_drop_app.views.submission_pdf'),
    # /submissions/[ID].json (staff only)
    url(r'^submissions/(?P<id>.+)\.json$', 'etd_drop_app.views.submission_json'),
    # /submissions/[ID] (staff only)
    url(r'^submissions/(?P<id>.+)$', 'etd_drop_app.views.submission_detail'),
)
