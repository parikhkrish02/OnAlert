from django.shortcuts import render, redirect
from .models import Contest, Platform, User, MyContest
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def login(request):
    # redirect()
    return render(request, "OnAlert/login.html")


def byRecency():
    contests = Contest.objects.all().order_by("when")
    platform_name = "All"
    params = {"platform_name": platform_name, "contests": contests}
    return params


def byCategory(opt):
    if opt == "cc":
        platform_name = "Code-Chef"
        contests = Contest.objects.filter(platform_name="CodeChef").order_by("when")
        params = {"platform_name": platform_name, "contests": contests}

    elif opt == "cf":
        platform_name = "Code-Forces"
        contests = Contest.objects.filter(platform_name="CodeForces").order_by("when")
        params = {"platform_name": platform_name, "contests": contests}

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

    # u1 = User.objects.filter(username=request.user)
    # for i in u1:
    #     con1 = MyContest.objects.filter(user=i)
    #     for mycnt in con1:
    #         print(mycnt.selectedContest.all())

    return render(request, "OnAlert/index.html", params)


@login_required
def setNotification(request):
    if request.method == "POST":
        user_sel = request.POST.getlist("platform_name[]")
        mycnt = MyContest.objects.get(user=request.user)
        platforms = mycnt.selectedContest.all()
        platform_list = []
        for pl in platforms:
            platform_list.append(pl.platform_name)

        # for pl in platforms:
        for us in user_sel:
            if us in platform_list:
                print("yes")
            else:
                # p = Platform.objects.get(platform_name=platform_list)
                # mycnt.selectedContest.add(p)
                print("no")

        # messages.success(request, "Contests Notification details updated.")
        return redirect("get_notification")
    else:
        contests = Platform.objects.all()
        params = {"contests": contests}
        return render(request, "OnAlert/editContest.html", params)


@login_required
def get_notification(request):

    contest = MyContest.objects.get(user=request.user)
    contests = contest.selectedContest.all()
    params = {"contests": contests}
    return render(request, "OnAlert/Notify.html", params)
