import django
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path('', views.home, name='homepage'),
   path('course/<str:slug>',views.course_slug, name='course_page'),
   path('signup/', views.signupView.as_view(), name='signupage'),
   path('login/', views.loginView.as_view(), name='login'),
   path('logout/', views.signout, name='logout'),
   path('checkout/<str:slug>',views.checkout, name='checkoutpage'),
   path('verify_payment', views.verify_payment, name='verify_payment'),
   path('mycourses/',views.mycourses, name='mycoursespage'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)