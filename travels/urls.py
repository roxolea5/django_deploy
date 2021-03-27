from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

from rest_framework import routers

#router = routers.DefaultRouter()
#router.register() # crear set de rutas

urlpatterns = [
    
    path("tour/eliminar/<int:idTour>/",
        views.eliminar_tour, name="eliminar_tour"),
    path('', views.index, name="index"),
    #path("login/", views.login_user, name="login_user")
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    #path("logout/", views.logout_user, name="logout_user")
    path("logout/", auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),

    #path('api', include(router.urls)), #importar rutas
    #path('api/auth', include("rest_framework.urls",namespace="rest_framework")), # toma las urls default de rest
]
