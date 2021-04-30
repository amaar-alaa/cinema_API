"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router=DefaultRouter()
router.register('guests',views.Viewsets_guests)
router.register('movies',views.Viewsets_movies)
router.register('resevations',views.Viewsets_reservations)

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/no-rest-no-model/',views.no_rest_no_model),
    #2
    path('django/no-rest-from-model/',views.no_rest_from_model),
    #3.1 FBV function based view GET & Post 
    path('rest/fbv/',views.FBV_List),
    #3.2 FBV function based view GET & PUT &DELETE
    path('rest/fbv/<int:pk>',views.FBV_pk),

    #4.1 List and create == GET & POST %% class based view 
    path('rest/cbv/',views.CBV_List.as_view()),

    #4.2 update & delete & show ==PUT & DELETE &GET       
    path('rest/cbv/<int:pk>',views.CBV_pk.as_view()),  

    #5.1 mixins List and create
    path('rest/mixins/',views.mixins_List.as_view()),

    #5.2 mixins update delete and show item 
    path('rest/mixins/<int:pk>',views.mixins_pk.as_view()),  

    #6.1 Generics list and create 
    path('rest/generics/',views.Generics_List.as_view()),

    #6.2 Generics update and delete and show item 

    path('rest/generics/<int:pk>',views.Generics_pk.as_view()),  

    #7 Viewsets

    path('rest/viewsets/',include(router.urls)),

    #8 find movies 
    path('fbv/findmovies',views.find_movie),

    #9 new reservations 
    path('fbv/newreservation',views.new_reservations),

    #10 api auth 
    path('api-auth/',include('rest_framework.urls')),

    #11 Token authentication
    path('api-token',obtain_auth_token)
 





]
