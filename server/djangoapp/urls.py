# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    path(route='login', view=views.login_user, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    path(route='register', view=views.registration, name='registration'),
    path('get_cars/', views.get_cars, name='getcars'),
    path('get_dealers', views.get_dealerships, name='getdealers'),
    path(
        'get_dealers/<str:state>',
        views.get_dealerships,
        name='getdealersbystate'
    ),
    path(
        'dealer/<int:dealer_id>',
        views.get_dealer_details,
        name='getdealer'
    ),
    path(
        'reviews/dealer/<int:dealer_id>',
        views.get_dealer_reviews,
        name='dealerreview'
    ),
    path('add_review', views.add_review, name='addreview'),


    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
