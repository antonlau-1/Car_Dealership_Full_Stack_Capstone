# Uncomment the required imports before adding the code
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # context = {}

    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']
    usernameExists = False
    # emailExists = False
    try:
        User.objects.get(username == username)
        usernameExists = True
    except Exception as e:
        print(f"Unexpected {e=}, {type(e)=}")
        logger.debug("{} is new user".format(username))

    if not usernameExists:
        user = User.objects.create_user(
            username=username, 
            first_name=firstName, 
            last_name=lastName, 
            password=password, 
            email=email,
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {
            "userName": username, 
            "status": "Username already exists"
        }
        return JsonResponse(data)


def get_cars(request):
    # Count the number of CarMake records
    count = CarMake.objects.filter().count()
    print("CarMake count:", count)

    # Populate data if no CarMake records exist
    if count == 0:
        try:
            initiate()  # Call the populate function
            print("Database populated with initial data.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Fetch car models with related car makes
    car_models = CarModel.objects.select_related('car_make').all()
    cars = [{
        "CarModel": car_model.name, 
        "CarMake": car_model.car_make.name} 
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` render list of dealerships 
# all by default, particular state if state is passed
def get_dealerships(request, state = "All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        print(f"Dealer ID: {dealer_id}")
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        print(f"Requesting URL: {endpoint}")

        # Fetch the reviews from the endpoint
        reviews = get_request(endpoint)
        print(f"Response from {endpoint}: {reviews}")

        # Check if the reviews list is empty or None
        if not reviews:
            return JsonResponse({"status": 404, "message": "No reviews found"})

        # Process each review for sentiment analysis
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(f"Sentiment analysis for review: {response}")
            review_detail['sentiment'] = response['sentiment']

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "bad request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "bad request"})


# Create a `add_review` view to submit a review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "message": response})
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)=}")
            return JsonResponse(
                {
                    "status": 401, "message": 
                    "Error in posting review."
                }
            )
    else:
        JsonResponse(
            {
                "status": 403, 
                "message": "You must be logged in to post a review."
            }
        )
# ...
