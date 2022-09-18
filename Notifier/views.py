from django.shortcuts import render
from .models import Contest, User, MyContest
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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

    u1 = User.objects.filter(username=request.user)
    for i in u1:
        con1 = MyContest.objects.filter(user=i)
        for mycnt in con1:
            print(mycnt.selectedContest.all())

    return render(request, "OnAlert/index.html", params)


@login_required
def get_notification(request):

    if request.method == "POST":
        print(request.POST.getlist("platform[]"))
        messages.success(request, "Contests Notification details updated.")
    else:
        pass

    contests = Contest.objects.values("platform").distinct()
    params = {"contests": contests}
    return render(request, "OnAlert/Notify.html", params)
