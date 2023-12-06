from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Goal, UserGoal
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from calendar import Calendar
import requests
import random
months_list = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']


@login_required
def calendar_view(request):
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    obj = Calendar()
    dates = obj.itermonthdates(year, month)
    formated_dates = []
    for i in dates:
        try:
            user_goal = UserGoal.objects.get(user=request.user, date=i)
            color = 'greenCompleted' if user_goal.is_all_completed == True else 'redCompleted'

            formated_dates.append({'date': i, 'type': color})
        except Exception:
            formated_dates.append({'date': i, 'type': 'noneCompleted'})
    context = {'dates': formated_dates,
               'year': year, 'month': months_list[month]}

    return render(request, 'home/calendar.html', context)


def check_value(value):
    return value == 'on'


def create_date(date):
    date = date.split('-')
    year, month, day = int(date[0]), int(date[1]), int(date[2])
    return datetime.date(year, month, day)


@login_required
def home(request):

    date = request.GET.get('date')
    user = request.user
    today = datetime.date.today()
    if date is not None:
        date = create_date(date)
    else:
        date = today

    if date == today:
        date_status = 'today'
    elif date > today:
        date_status = 'tomorrow'
    elif date <= today + timedelta(days=-1):
        date_status = 'past'

    if request.method == "GET":

        if date_status != 'past':
            user_goal, created = UserGoal.objects.get_or_create(
                user=user, date=date)

            if created:
                for _ in range(3):
                    obj = Goal.objects.create(
                        user_goal=user_goal, goal='', is_completed=False)
                    obj.save()
        else:
            try:
                user_goal = UserGoal.objects.get(user=user, date=date)
            except Exception:
                user_goal = UserGoal.objects.get(user=user, date=today)
                date_status = 'today'

    response = requests.get('https://type.fit/api/quotes')
    response_data = response.json()
    ran_no = random.randint(0, len(response_data)-1)
    quote = response_data[ran_no]

    if request.method == "POST":

        input_data_list = [
            (
                request.POST.get(f'goal{i}Input'),
                check_value(request.POST.get(f'goal{i}Check', 'off')),
                request.POST.get(f'uid{i}')
            )
            for i in range(1, 4)
        ]
        user_goal = UserGoal.objects.get(user=request.user, date=date)
        for i in input_data_list:
            goal_obj = Goal.objects.get(uid=i[2])
            goal_obj.goal = i[0]
            goal_obj.is_completed = i[1]
            goal_obj.save()
    next_date = date + timedelta(days=1)
    try:
        prev_date = date + timedelta(days=-1)
        prev_user_goal = UserGoal.objects.get(user=user, date=prev_date)
    except Exception:
        prev_date = False

    context = {'user_goal': user_goal, 'date_status': date_status,
               'prev_date': prev_date, 'next_date': next_date, 'home': True, 'quote': quote}
    return render(request, 'home/index.html', context)


def sign_in(request):
    email = False
    if request.method == "POST":
        email = request.POST.get('emailInput')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Signed In Successfull !")
            return redirect('home')
        else:
            messages.error(request, "Enter valid credentials !")

    return render(request, 'home/signIn.html', {'email': email, 'sign_in': True})


def sign_up(request):
    if request.method == "POST":
        email = request.POST.get('emailInput')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if email_obj := User.objects.filter(username=email).exists():
            messages.error(request, "User already exist!")
        elif password1 == password2:
            user = User.objects.create_user(username=email, password=password1)
            user.save()
            messages.success(request, "User Created Successfully !")
            return redirect('sign_in')
        else:
            messages.error(request, "Password must be same!")

    return render(request, 'home/signUp.html', {'sign_up': True})


def sign_out(request):
    logout(request)
    return redirect('home')
