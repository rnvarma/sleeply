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
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
