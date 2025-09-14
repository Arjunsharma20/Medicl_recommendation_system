from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),                          # Homepage
    path("patient/", views.patient_dashboard, name="patient_dashboard"),  # Patient dashboard
    path("doctor/", views.doctor_dashboard, name="doctor_dashboard"),     # Doctor dashboard
    path("about/", views.about, name="about"),                  # About us page
    path("contact/", views.contact, name="contact"),            # Contact page
    path("blog/", views.blog, name="blog"),                     # Blog page
    path("developer/", views.developer, name="developer"),      # Developer (About Arjun Sharma)
]
