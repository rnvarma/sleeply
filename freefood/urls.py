from django.conf.urls import patterns, include, url
from django.contrib import admin

from freefood import views

# Override the Admin Site header
admin.site.site_header = "Django Template Administration"

# Set the error handlers
handler403 = views.PermissionDeniedView.as_view()
handler404 = views.NotFoundView.as_view()
handler500 = views.ErrorView.as_view()

urlpatterns = patterns('',
    url(r'^$', views.IndexPage.as_view(), name='home'),
    url(r'^executelogin', views.login_user),
    url(r'^login', views.LoginPage.as_view()),
    url(r'^1/create_user', views.UserView.as_view())
)
