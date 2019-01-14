from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponse
from django.http import JsonResponse
from iiiedu.models import Branch, Tag, Cate, Course, Role, UserProfile, Favorite, Reply, Menu, Series, Theme
from iiiedu.mongohelper import MongoHelper
import json
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# mongo = MongoHelper(host="mongodb://mario:69538463@ds155288.mlab.com:55288/course", db_name='course',
#                     collection='iiiedu')

chart = MongoHelper(host="mongodb://mario:69538463@ds155288.mlab.com:55288/course", db_name='course',
                    collection='chart')


# chert

def TopCourse(request):
    data = chart.collection.find_one({'chart': 'class'}, {'_id': 0, 'data': 1})
    ret = {"data": data["data"], "title": "十大課程"}
    return render(request, "chert/index.html", ret)


def TopCertified(request):
    data = chart.collection.find_one({'chart': 'cert'}, {'_id': 0, 'data': 1})
    ret = {"data": data["data"], "title": "十大認證"}

    return render(request, "chert/index.html", ret)


def TopLang(request):
    data = chart.collection.find_one({'chart': 'lang'}, {'_id': 0, 'data': 1})
    ret = {"data": data["data"], "title": "十大語言(待優化)"}

    # ![](https://i.imgur.com/FDIbFL5.jpg)

    return render(request, "chert/index.html", ret)


def TopTheme(request):
    data = chart.collection.find_one({'chart': 'theme'}, {'_id': 0, 'data': 1})
    ret = {"data": data["data"], "title": "主題"}

    # ![](https://i.imgur.com/FDIbFL5.jpg)

    return render(request, "chert/index.html", ret)


# theme

def theme(request, pk):
    data = chart.collection.find_one({'chart': pk}, {'_id': 0, 'data': 1})
    t = Theme.objects.get(en=pk)
    series = Series.objects.filter(theme=t)

    ret = {"data": data["data"], "title": t.name, 'url': t.en, 'menu': series}
    return render(request, "theme/index.html", ret)


# series

def series(request, pk):
    s = Series.objects.get(en=pk)

    t = s.theme.all()[0]
    series = Series.objects.filter(theme=t)

    contact_list = Course.objects.filter(series=s)

    # contact_list = Course.objects.exclude(Cate__name='認證').exclude(Cate__name="養成班")
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    page = {
        'theme': {'name': t.name, 'url': t.en},
        'series': {'name': s.name, 'url': s.en},
    }

    ret = {'data': data, 'menu': series, 'page': page}

    return render(request, "series/index.html", ret)


# Course

def course(request):
    title = '專業課程'
    contact_list = Course.objects.exclude(Tag__name='認證').exclude(Tag__name="養成班")
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': title}

    return render(request, "course/index.html", ret)


def course_cert(request):
    q = '認證'
    contact_list = Course.objects.filter(Tag__name=q)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': q}
    return render(request, "course/index.html", ret)


def course_full(request):
    q = '養成班'

    contact_list = Course.objects.filter(Tag__name=q)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': q}
    return render(request, "course/index.html", ret)


# search

def search(request):
    name = request.GET.get('name')
    print(request.GET.get('anc'))
    print(request.GET.get('pppp'))

    contact_list = Course.objects.filter(name__icontains=name)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    ret = {'data': data, 'title': "%s 搜尋結果" % name}

    return render(request, "search.html", ret)


def testmap(request):
    # Create two threads as follows
    return HttpResponse("ok")


def test_page(request):
    ret = {}

    return render(request, "test.html", ret)


def test_ajax(request):
    if request.POST:

        data = request.POST['data']
        print(data)
    else:
        data = "ok"
    return HttpResponse(data)


def cleardb(request):
    Tag.objects.all().delete()
    Cate.objects.all().delete()
    Course.objects.all().delete()
    Role.objects.all().delete()
    UserProfile.objects.all().delete()
    Favorite.objects.all().delete()
    Reply.objects.all().delete()
    Menu.objects.all().delete()
    Branch.objects.all().delete()

    return HttpResponse("清理OK")


def testdb(request):
    t = Tag.objects.filter(**{'name': "tag1"})
    print(t)
    print(len(t))
    # x = mongo.collection.find_one()
    return HttpResponse(len(t))

# redirect
def home_redirect(request):
    return HttpResponseRedirect(
        reverse('chart_theme')
    )