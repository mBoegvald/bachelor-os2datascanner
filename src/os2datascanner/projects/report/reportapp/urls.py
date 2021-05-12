import django_saml2_auth.views
import django.contrib.auth.views
from django.conf.urls import url
from django.http import HttpResponse
from django.urls import include
from django.conf import settings
from django.urls import path

from .views import socketview
from .views.api import JSONAPIView
from .views.views import (MainPageView, LeaderStatisticsPageView, DPOStatisticsPageView, ApprovalPageView,
                          StatsPageView, SettingsPageView, AboutPageView, LogoutPageView, ReportListing,
                          getSensitivities, getScannerjobs)

urlpatterns = [
    url(r'^$',      MainPageView.as_view(),     name="index"),
    url('api$',     JSONAPIView.as_view(),     name="json-api"),
    url(r'^statistics/leader/$', LeaderStatisticsPageView.as_view(), name='statistics'),
    url(r'^statistics/dpo/$', DPOStatisticsPageView.as_view(), name='statistics'),
    url('approval', ApprovalPageView.as_view(), name="about"),
    url('stats',    StatsPageView.as_view(),    name="about"),
    url('settings', SettingsPageView.as_view(), name="settings"),
    url('about',    AboutPageView.as_view(),    name="about"),
    url(r'^health/', lambda r: HttpResponse()),
    #DRF
    # List of documentreports
    path("report_listing/", ReportListing.as_view(), name='listing'),
    # These urls are for getting the options for the select fields
    path("ajax/sensitivities/", getSensitivities, name='get_sensitivities'),
    path("ajax/scannerjobs/", getScannerjobs, name='get_scannerjobs'),
]

if settings.SAML2_ENABLED:
    urlpatterns.append(url(r"^saml2_auth/", include("django_saml2_auth.urls")))
    urlpatterns.append(url(r"^accounts/login/$", django_saml2_auth.views.signin))
    urlpatterns.append(url(r'^accounts/logout/$', django_saml2_auth.views.signout))

if settings.KEYCLOAK_ENABLED:
    settings.LOGIN_URL = "oidc_authentication_init"
    settings.LOGOUT_REDIRECT_URL = settings.SITE_URL + "accounts/logout/"
    urlpatterns.append(path('oidc/', include('mozilla_django_oidc.urls'))),
    urlpatterns.append(url(r'^accounts/logout/',
                           LogoutPageView.as_view(
                               template_name='logout.html',
                           ),
                           name='logout'))
else:
    urlpatterns.append(url(r'^accounts/login/',
                           django.contrib.auth.views.LoginView.as_view(
                               template_name='login.html',
                           ),
                           name='login'))
    urlpatterns.append(url(r'^accounts/logout/',
                           django.contrib.auth.views.LogoutView.as_view(
                               template_name='logout.html',
                           ),
                           name='logout'))
