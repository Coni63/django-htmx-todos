from django.urls import include, path
from . import views

from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('load-message/', views.load_message, name='load_message'),

    path("oidc/", include("mozilla_django_oidc.urls")),
    path("login/", OIDCAuthenticationRequestView.as_view(), name="oidc_authentication_init"),
    path("logout/", OIDCLogoutView.as_view(), name="oidc_logout"),
]