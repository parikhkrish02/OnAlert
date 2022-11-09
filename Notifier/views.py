from datetime import datetime
import warnings
from django.shortcuts import render, redirect
from .models import Contest, Platform, User, MyContest
from django.contrib.auth.decorators import login_required

from bs4 import BeautifulSoup
import requests
import time

# Create your views here.


def home(request):
    recentFive = Contest.objects.order_by("when")[:5]
    params = {"contests": recentFive}

    return render(request, "index.html", params)


def login(request):
    return render(request, "login.html")


# @login_required
def contests(request):
    opt = "default"
    if request.method == "POST":
        opt = request.POST["userOpt"]

    if opt == "all" or opt == "default":
        params = {
            "platform_name": "All",
            "platforms": Platform.objects.all(),
            "contests": Contest.objects.order_by("when"),
        }

    else:
        platform = Platform.objects.get(platform_name=opt)
        contests = Contest.objects.filter(platform=platform)
        params = {
            "platform_name": opt,
            "platforms": Platform.objects.all(),
            "contests": contests,
            "this_platform": platform,
        }

    return render(request, "contests.html", params)


def aboutUs(request):
    return render(request, "about.html")


def contactUs(request):
    return render(request, "contact.html")


@login_required
def add(request, platform):
    MyContest.objects.get(user=request.user).selectedContest.add(
        Platform.objects.get(platform_name=platform)
    )
    return redirect("setNotification")


@login_required
def remove(request, platform):
    MyContest.objects.get(user=request.user).selectedContest.remove(
        Platform.objects.get(platform_name=platform)
    )
    return redirect("setNotification")


@login_required
def setNotification(request):
    if not MyContest.objects.filter(user=request.user).exists():
        MyContest.objects.create(user=request.user)

    all_platforms = Platform.objects.all()
    selected_contest = MyContest.objects.get(user=request.user).selectedContest.all()
    unselected_contests = []

    for contest in all_platforms:
        if not (contest in selected_contest):
            unselected_contests.append(contest)

    params = {
        "selected_contests": selected_contest,
        "unselected_contests": unselected_contests,
    }
    return render(request, "plat.html", params)


@login_required
def myContest(request):
    selected_platforms = MyContest.objects.get(user=request.user).selectedContest.all()
    contests = []

    for platform in selected_platforms:
        temp_contests = Contest.objects.filter(platform=platform)
        for temp_contest in temp_contests:
            contests.append(temp_contest)

    params = {"contests": contests}
    return render(request, "MyContest.html", params)


def scrape(requests):

    CodeChef()
    CodeForces()
    AtCoder()
    # HackerEarth()

    return redirect("/")


def CodeChef():
    CodeChef = "https://www.codechef.com/api/list/contests/all?sort_by=START"
    r = requests.get(CodeChef)
    all_contest = r.json()["future_contests"]

    # contest(charField)
    contest_name = []
    # when
    contest_start = []
    # duration
    contest_duration = []
    # contest_link
    contest_link = []

    for contest in all_contest:
        contest_name.append(contest["contest_name"])
        contest_start.append(contest["contest_start_date_iso"])
        contest_duration.append(contest["contest_duration"])
        contest_link.append("https://www.codechef.com/" + contest["contest_code"])

    for (name, start, duration, link) in zip(
        contest_name, contest_start, contest_duration, contest_link
    ):
        if Contest.objects.filter(contest=name).exists():
            pass
        else:
            duration_hrs = str(int(duration) // 60) + ":" + str(int(duration) % 60)
            temp = Contest(
                platform=Platform.objects.get(platform_name="CodeChef"),
                contest=name,
                contest_link=link,
                when=start,
                duration=duration_hrs,
            )
            temp.save()
            print(
                name + " :: " + start + " :: " + duration_hrs + " :: " + link,
                end="\n\n",
            )


def CodeForces():

    CodeForces = "https://codeforces.com/contests"

    data = requests.get(CodeForces)

    htmlContent = data.content
    soupData = BeautifulSoup(htmlContent, "html.parser")
    futureContest = soupData.find_all("table")[0].find_all("tr")

    # contest(charField)
    contest_name = []
    # when
    contest_start = []
    # duration
    contest_duration = []
    # contest_link
    contest_link = []

    for index, contest in enumerate(futureContest):
        if index != 0:
            contest_link.append(
                "https://codeforces.com/contests/"
                + (contest.get("data-contestid")).strip()
                + "/"
            )
            contest_name.append(((contest.find_all("td")[0]).text).strip())
            contest_start.append(((contest.find_all("td")[2]).text).strip())
            contest_duration.append(((contest.find_all("td")[3]).text).strip())

    for (name, start, duration, link) in zip(
        contest_name, contest_start, contest_duration, contest_link
    ):
        if not Contest.objects.filter(contest=name).exists():
            format = "%b/%d/%Y"
            datetime_str = datetime.strptime(start[0:11], format)
            time = start[11:]
            start_modified = str(datetime_str)[0:10] + time

            warnings.filterwarnings(action="ignore", category=RuntimeWarning)
            temp = Contest(
                platform=Platform.objects.get(platform_name="CodeForces"),
                contest=name,
                contest_link=link,
                when=start_modified,
                duration=duration,
            )
            temp.save()
            print(
                name + " :: " + start_modified + " :: " + duration + " :: " + link,
                end="\n\n",
            )


def AtCoder():
    AtCoder = "https://atcoder.jp/contests/"

    r = requests.get(AtCoder)

    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, "html.parser")
    upcomingContest = soup.find(id="contest-table-upcoming").find_all("tr")

    # contest(charField)
    contest_name = []
    # when
    contest_start = []
    # duration
    contest_duration = []
    # contest_link
    contest_link = []

    for index, contest in enumerate(upcomingContest):
        if index != 0:
            contest_name.append(((contest.find_all("a")[1]).text).strip())
            contest_duration.append(((contest.find_all("td")[2]).text).strip())
            time_japnese = ((contest.find("td")).text)[0:16]
            contest_start.append(time_japnese)
            for index, href in enumerate(contest.find_all("a")):
                if index % 2 != 0:
                    contest_link.append("https://atcoder.jp" + href.get("href"))

    for (name, start, duration, link) in zip(
        contest_name, contest_start, contest_duration, contest_link
    ):
        if not Contest.objects.filter(contest=name).exists():
            warnings.filterwarnings(action="ignore", category=RuntimeWarning)
            temp = Contest(
                platform=Platform.objects.get(platform_name="AtCoder"),
                contest=name,
                contest_link=link,
                when=start,
                duration=duration,
            )
            temp.save()
            print(name + " :: " + start + " :: " + duration + " :: " + link, end="\n")


def HackerEarth():
    try:
        HackerEarth = "https://www.hackerearth.com/challenges/"

        data = requests.get(HackerEarth)

        htmlContent = data.content
        soupData = BeautifulSoup(htmlContent, "html.parser")
        futureContest = soupData.find("div", class_="upcoming challenge-list").find_all(
            "div", class_="challenge-card-modern"
        )

        # contest(charField)
        contest_name = []
        # when
        contest_start = []
        # duration
        contest_duration = []
        # contest_link
        contest_link = []

        for contest in futureContest:
            contest_name.append(
                ((contest.find("div", class_="challenge-name")).text).strip()
            )
            contest_start.append(((contest.find("div", class_="date")).text).strip())
            # contest_duration.append(((contest.find_all("td")[3]).text).strip())
            # contest_link.append(
            #     "https://codeforces.com/contests/"
            #     + (contest.get("data-contestid")).strip()
            #     + "/"
            # )

        for (name, start, duration, link) in zip(
            contest_name, contest_start, contest_duration, contest_link
        ):
            print(name + " :: " + start + " :: " + duration + " :: " + link, end="\n\n")
    except:
        print("Error")
