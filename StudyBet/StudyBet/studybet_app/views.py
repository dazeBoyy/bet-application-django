from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from .models import *


@login_required()
def index(request):
    if request.user.is_superuser:
        bets = Fixture.objects.all()
        return render(request, 'admin_pages/admin_page.html', {'bets': bets})
    if request.user.is_authenticated:
        bets = Fixture.objects.all()
        user_bet = Bet.objects.all()
        return render(request, 'user_pages/home_page.html', {'bets': bets, 'user_bets': user_bet})

@login_required()
def show_finished(request):
    bets = Fixture.objects.all()
    user_bet = Bet.objects.all()
    return render(request, 'user_pages/bet_finished_page.html', {'bets': bets, 'user_bets': user_bet})

@login_required()
def get_balance(request, account_id):

        account = get_object_or_404(Account, id=account_id)


        return render(request, 'user_pages/balance.html', {'account': account})


@login_required()
def go_bet(request, account_id, fixture_id):
    account = get_object_or_404(Account, id=account_id)
    fixture = get_object_or_404(Fixture, id=fixture_id)

    return render(request, 'user_pages/bet_page.html', {'account': account, 'fixture': fixture})

@login_required()
def account_bets(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    bets = Bet.objects.filter(bet_user = account)

    return render(request, 'user_pages/account_bets_page.html', {'bets':  bets})


@login_required()
def make_bet(request, account_id, fixture_id):

    account = get_object_or_404(Account, id=account_id)
    fixture = get_object_or_404(Fixture, id=fixture_id)

    bet_vote = request.POST['vote']
    bet_vote = int(bet_vote)
    if bet_vote == 0:
        bet_vote = 0
    elif bet_vote == 1:
        bet_vote = 1
    else:
        print("Ошибка в поставке")
        return 404
    print(bet_vote)
    money = request.POST['bet']
    money = int(money)
    if money == 500:
        money = 500
    elif money == 1000:
        money = 1000
    elif money == 1500:
        money = 1500
    else:

        print("Ошибка в деньгах:")
        return 404
    print(money)
    course = request.POST['course']
    course = int(course)
    if course == 2:
        course = 2
    elif course == 4:
        course = 4
    else:
        print("Ошибка в курсе")
        return 404
    print(course)

    bet = Bet(fixture = fixture, bet_user = account, bet_amount = money, bet = bet_vote, bet_course = course)
    bet.save()

    return HttpResponseRedirect(reverse('go_bet', args=(account_id, fixture_id)))


@login_required()
def deposit_balance(request, account_id):

    account = get_object_or_404(Account, id=account_id)

    money = request.POST['inlineRadioOptions']
    money = int(money)
    if money == 500:
        money = 500
    elif money == 1000:
        money = 1000
    elif money == 1500:
        money = 1500
    else:
        return 404
    print(money)
    account.cash += money
    account.save()

    return HttpResponseRedirect(reverse('get_balance', args=(account_id)))

@login_required()
def add_bet_admin(request):

    bet_win = request.POST['bet_win']
    bet_lose = request.POST['bet_lose']
    bet_name = request.POST['bet_name']


    bet = Fixture(bet_win=bet_win,bet_lose=bet_lose,bet_name=bet_name)
    bet.save()

    return HttpResponseRedirect(reverse('index'))
@login_required()
def admin_edit_bet(request, bet_id):
    bet = get_object_or_404(Fixture, id=bet_id)

    return render(request, 'admin_pages/admin_edit_bet.html', {'bet': bet})

@login_required()
def admin_delete_bet(request, bet_id):

    bet = Fixture.objects.get(id=bet_id)
    bet.delete()

    return HttpResponseRedirect(reverse('index'))


@login_required()
def admin_edit_bet_confirm(request, bet_id):
    bet = get_object_or_404(Fixture, id=bet_id)

    bet_vote = request.POST['vote']
    bet_vote = int(bet_vote)
    if bet_vote == 0:
        bet_vote = 0
    elif bet_vote == 1:
        bet_vote = 1
    else:
        print("Ошибка в поставке")
        return 404

    bet.fixture_result = bet_vote
    bet.save()

    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return HttpResponse('Username is already taken')
            elif User.objects.filter(email=email).exists():
                return HttpResponse('Email is already taken')
            else:
                user = User.objects.create_user(username=username, password=password,
                                                email=email, first_name=first_name, last_name=last_name)
                Account.objects.create(user=user,  cash=1000)
                user.save()

                return redirect('http://127.0.0.1:8000')


        else:
            return HttpResponse('Both passwords are not matching')


    else:
        return render(request, 'reg_and_login/register.html')

def logout_user(request):
    auth.logout(request)
    return redirect('http://127.0.0.1:8000')