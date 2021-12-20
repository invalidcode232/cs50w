import calendar
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
import math
import simplejson

from .models import *
from .forms import *

PAGINATE_BY = 4


# Create your views here.
@login_required(login_url='/login')
def index(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            distance = form.cleaned_data["distance"]
            duration = form.cleaned_data["duration"]
            time = form.cleaned_data["time"]
            date = form.cleaned_data["date"]
            image = form.cleaned_data["image"]
            elevation = form.cleaned_data["elevation"]
            pace = float(duration) / float(distance)

            activity = Activity(user=request.user, distance=distance, time=time, date=date, image=image, elevation=elevation, duration=duration, pace=pace)
            activity.save()

        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        # Get run statistics filter
        filter_by = request.GET.get("filter")

        # Get activity filter
        # Check if filter is set
        if 'filter_by' not in request.session:
            request.session['filter_by'] = 'week'

        if filter_by:
            request.session['filter_by'] = filter_by

        if request.session['filter_by'] == "month":
            # Get activity from this month and sort it by date descending
            activities = Activity.objects.filter(user=request.user, date__month=datetime.date.today().month).order_by('-date')
            # activities = Activity.objects.filter(user=request.user).filter(date__gte=datetime.date.today() - datetime.timedelta(days=30))
        elif request.session['filter_by'] == "year":
            # Get activity from this year
            activities = Activity.objects.filter(user=request.user, date__year=datetime.date.today().year).order_by('-date')
            # activities = Activity.objects.filter(user=request.user).filter(date__gte=datetime.date.today() - datetime.timedelta(days=365))
        elif request.session['filter_by'] == "alltime":
            activities = Activity.objects.filter(user=request.user).order_by('-date')
        else:
            activities = Activity.objects.filter(user=request.user).filter(date__gte=datetime.date.today() - datetime.timedelta(days=7)).order_by('-date')

        # Get sum of distance
        distance = activities.aggregate(Sum('distance'))['distance__sum']

        # Get number of activities
        num_activities = activities.count()

        # Get number of activities with pace
        num_activities_with_pace = activities.filter(pace__isnull=False).count()
        # Get sum of pace
        pace_sum = activities.aggregate(Sum('pace'))['pace__sum']

        if pace_sum is not None:
            pace_avg = float(pace_sum) / float(num_activities_with_pace)
        else:
            pace_avg = 0

        # Convert activities to json template for chart
        activities_json = serializers.serialize('json', activities)

        # Get decimal point of pace and convert it to seconds
        frac, whole = math.modf(pace_avg)
        pace_min = int(whole)
        pace_sec = int(round(frac * 60))

        stats = {
            'distance': distance,
            'num_activities': num_activities,
        }

        # activities = Activity.objects.filter(user=request.user)
        # Paginate the activities to display PAGINATE_BY per page
        paginator = Paginator(activities, PAGINATE_BY)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Get logged in user
        user = User.objects.get(username=request.user)

        activity_form = ActivityForm()

        return render(request, 'run50/index.html', {
            'activities': activities,
            'activity_form': activity_form,
            'user': user,
            'create_activity': True,
            'show_profile': False,
            'page_obj': page_obj,
            'show_stats': True,
            'stats': stats,
            'pace_min': pace_min,
            'pace_sec': pace_sec,
            'activities_json': activities_json,
            'filter_by': request.session['filter_by'],
        })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'run50/login.html', {
                'error_message': 'Invalid login'
            })
    elif request.method == 'GET':
        # if request.user.is_authenticated:
        #     return HttpResponseRedirect('/')
        return render(request, 'run50/login.html')


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "run50/register.html", {
                "error_message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "run50/register.html", {
                "message": "Username/email already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "run50/register.html")


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/login')
def profile(request, user_id):
    user = User.objects.get(id=user_id)

    if user.share_preference == 0 or user == request.user:
        activities = Activity.objects.filter(user=user)
    else:
        activities = []

    # Paginate the activities to display 5 per page
    paginator = Paginator(activities, PAGINATE_BY)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # TODO: Display follower count after follower function is added
    # Get follower count
    followers_count = Follower.objects.filter(user=user).count()

    # Check if user is following
    is_following = Follower.objects.filter(user=user, follower=request.user).count()
    print(is_following)

    return render(request, 'run50/index.html', {
        'user': user,
        'show_profile': True,
        'activities': activities,
        'page_obj': page_obj,
        'followers_count': followers_count,
        'is_following': is_following,
    })


@login_required(login_url='/login')
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user)

            username = form.cleaned_data["username"]
            if username != request.user.username and username != "":
                user.username = username

            profile_picture = request.FILES.get("profile_picture")
            if profile_picture:
                user.profile_picture = profile_picture

            # TODO: Uncomment this
            share_preference = 0
            # share_preference = form.cleaned_data["share_preference"]
            if share_preference != request.user.share_preference:
                user.share_preference = share_preference

            user.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = EditProfileForm(initial={
            "username": request.user.username,
            "share_preference": request.user.share_preference,
        })
        return render(request, 'run50/edit_profile.html', {
            'form': form,
        })


# TODO: Add view activity
@login_required(login_url='/login')
def view_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    return render(request, 'run50/view_activity.html', {
        'activity': activity,
    })


@login_required(login_url='/login')
def edit_activity(request, activity_id):
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = Activity.objects.get(id=activity_id)

            if request.user != activity.user:
                return HttpResponseRedirect(reverse("index"))

            if form.cleaned_data['distance'] != activity.distance:
                activity.distance = form.cleaned_data['distance']
            if form.cleaned_data['time'] != activity.time:
                activity.time = form.cleaned_data['time']
            if form.cleaned_data['date'] != activity.date:
                activity.date = form.cleaned_data['date']
            if form.cleaned_data['duration'] != activity.duration:
                activity.duration = form.cleaned_data['duration']
            if form.cleaned_data['elevation'] != activity.elevation:
                activity.elevation = form.cleaned_data['elevation']
            if request.FILES.get("image"):
                activity.image = request.FILES.get("image")

            activity.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        activity = Activity.objects.get(id=activity_id)

        if request.user != activity.user:
            return HttpResponseRedirect(reverse("index"))

        form = ActivityForm(initial={
            "duration": activity.duration,
            "elevation": activity.elevation,
            "distance": activity.distance,
            "time": activity.time,
            "date": activity.date,
        })
        return render(request, 'run50/edit_activity.html', {
            'activity': activity,
            'form': form,
        })


@login_required(login_url='/login')
def delete_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    if request.user != activity.user:
        return HttpResponseRedirect(reverse("index"))

    activity.delete()
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='/login')
def discover(request):
    # Get users with recent activities in the last two weeks that is not the current user
    users = User.objects.exclude(username=request.user.username).filter(
        activity__date__gte=datetime.date.today() - datetime.timedelta(days=14),
        share_preference=0,
    ).distinct()

    # Paginate users
    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'run50/discover.html', {
        'users': users,
        'page_obj': page_obj,
    })


@login_required(login_url='/login')
def follow(request, user_id):
    user = User.objects.get(id=user_id)

    # is_following = User.objects.filter(
    #     followers=request.user,
    #     user=user
    # ).exists()

    if request.user != user:
        Follower.objects.create(user=user, follower=request.user)

    return HttpResponseRedirect(reverse("profile", args=(user_id,)))


@login_required(login_url='/login')
def unfollow(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user != user:
        Follower.objects.filter(user=user, follower=request.user).delete()

    return HttpResponseRedirect(reverse("profile", args=(user_id,)))


@login_required(login_url='/login')
def feed(request):
    # Get activities from the current user and the users that the current user is following
    activities = Activity.objects.filter(
        Q(user=request.user) |
        Q(user__in=Follower.objects.filter(follower=request.user).values_list('user', flat=True))
    ).order_by('-date')

    # Paginate activities
    paginator = Paginator(activities, PAGINATE_BY)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'run50/index.html', {
        'activities': activities,
        'page_obj': page_obj,
    })


@login_required(login_url='/login')
def leaderboard(request):
    if 'filter' in request.GET:
        request.session['filter'] = request.GET['filter']
    else:
        request.session['filter'] = datetime.datetime.now().month

    # Get the last date of the month
    last_day = calendar.monthrange(datetime.datetime.now().year, int(request.session['filter']))[1]

    # Get users with their total distance in the current month
    users = User.objects.filter(
        activity__date__gte=datetime.date.today().replace(day=1, month=int(request.session['filter'])),
        # activity__date__gte=datetime.date.today() - datetime.timedelta(days=30),
        activity__date__lte=datetime.date.today().replace(day=last_day, month=int(request.session['filter'])),
        activity__distance__isnull=False,
        activity__distance__gt=0,
    ).annotate(
        total_distance=Sum('activity__distance'),
    ).order_by('-total_distance')

    # Get months name for the dropdown
    months = []
    for month in range(1, 13):
        months.append(datetime.date.today().replace(month=month).strftime("%B"))

    return render(request, 'run50/leaderboard.html', {
        'users': users,
        'months': months,
    })
