from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


@login_required
def search_name(request):
    username = request.session.get("user", "")
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


def sql_inject(request):
    return render(request, "sql_inject.html")


def sql_inject_func(request):
    ctx = {}
    if request.GET:
        ctx['error'] = "GET:"
        name = request.GET['search']
        query_string = "SELECT * FROM sign_event WHERE name = '" + name + "'"
        ctx['query_string'] = query_string
        res = Event.objects.raw(query_string)
        for eve in res:
            ctx['error'] += str(eve.id) + " /_/ " + eve.name + " /_/ " + \
                str(eve.limit) + " /_/ " + str(eve.status) + " /_/ " + eve.address + \
                " /_/ " + str(eve.start_time) + " /_/ " + str(eve.create_time)
    response = render(request, "sql_inject.html", ctx)
    return response


def sql_inject_update(request):

    import pymysql
    db = pymysql.connect('localhost', 'root', '', 'guest')
    cursor = db.cursor()

    ctx = {}
    if request.GET:
        ctx['error'] = "GET:"
        name = request.GET['update']
        query_string = "update sign_event set name = '" + name + "' where id = 15"
        ctx['query_string'] = query_string
        data = cursor.execute(query_string)
        db.commit()
        ctx['error'] += str(data)

    db.close()
    response = render(request, "sql_inject.html", ctx)
    return response


def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
#         if username == "admin" and password == "admin123":
            # return HttpResponse("login success!")
#             response = HttpResponseRedirect("/event_manage/")
            # response.set_cookie("user", username, 3600)
            request.session["user"] = username
            response = HttpResponseRedirect("/event_manage/")
            return response
        else:
            return render(request, "index.html", {"error": "username or password error!"})
    else:
        return render(request, "index.html", {"error": "username or password error!"})


@login_required
def event_manage(request):
    # username = request.COOKIES.get("user", "")
    #     username = request.session.get("user", "")
    #     return render(request, "event_manage.html", {"user": username})
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer,deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range,deliver last page of results
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, event_id):
    # 查询总共参加人数和已签到人数
    total_guest = Guest.objects.filter(event_id=event_id)
    total_number = total_guest.count
    sign_guest = Guest.objects.filter(event_id=event_id, sign=True)
    sign_number = sign_guest.count

    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone', '')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone error.', 'total_number': total_number, 'sign_number': sign_number})

    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.', 'total_number': total_number, 'sign_number': sign_number})

    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has already sign in.", 'total_number': total_number, 'sign_number': sign_number})
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result, 'total_number': total_number, 'sign_number': sign_number})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
