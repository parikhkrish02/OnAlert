from cmath import log
from django.shortcuts import render
from .models import Contest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django import forms

# Create your views here.


def login(request):
    # redirect()
    return render(request, "OnAlert/login.html")


def byRecency():
    contests = Contest.objects.all().order_by("when")
    platform = "All"
    params = {"platform": platform, "contests": contests}
    return params


def byCategory(opt):
    if opt == "cc":
        platform = "Code-Chef"
        contests = Contest.objects.filter(platform="CodeChef").order_by("when")
        params = {"platform": platform, "contests": contests}

    elif opt == "cf":
        platform = "Code-Forces"
        contests = Contest.objects.filter(platform="CodeForces").order_by("when")
        params = {"platform": platform, "contests": contests}

    return params


def index(request):
    # opt = request.POST.get('userOpt', 'default')
    opt = "default"
    if request.method == "POST":
        opt = request.POST["userOpt"]
        print(opt)

    if opt == "all" or opt == "default":
        params = byRecency()

    elif opt == "cc":
        params = byCategory(opt)

    elif opt == "cf":
        params = byCategory(opt)

    return render(request, "OnAlert/index.html", params)


@login_required
def get_notification(request):
    contests = Contest.objects.values("platform").distinct()
    params = {"contests": contests}
    return render(request, "OnAlert/Notify.html", params)
