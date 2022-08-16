from django.shortcuts import render
from .models import Contest

# Create your views here.


def byRecency():
    contests = Contest.objects.all().order_by('when')
    platform = 'All'
    params = {'platform': platform, 'contests': contests}
    return params


def byCategory(opt):
    if opt == 'cc':
        platform = 'Code-Chef'
        contests = Contest.objects.filter(platform='CodeChef').order_by('when')
        params = {'platform': platform, 'contests': contests}

    elif opt == 'cf':
        platform = 'Code-Forces'
        contests = Contest.objects.filter(platform='CodeForces').order_by('when')
        params = {'platform': platform, 'contests': contests}

    return params


def index(request):
    opt = request.POST.get('userOpt', 'default')

    if opt == 'all' or opt == 'default':
        params = byRecency()

    elif opt == 'cc':
        params = byCategory(opt)

    elif opt == 'cf':
        params = byCategory(opt)

    return render(request, 'OnAlert/index.html', params)
