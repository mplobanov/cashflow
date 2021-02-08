from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as lgn
from django.contrib.auth import logout as lgt
from django.shortcuts import redirect
from .models import * #User_info, Cheque
from django.contrib.auth.models import User
from random import randint as rnd
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
# Create your views here.


def make_message(request, mes):
    ##if request.user.is_authenticated:
    ##    h = HistoryNote(user=request.user, date=timezone.now(), text="Пользователь получил сообщение {}".format(mes))
    ##    h.save()
    return render(request, 'cheque/message.html', {'message': mes})

def login_page(request):
    return render(request, 'cheque/login_page.html', {})

def login_process(request):
    login = request.POST['login']
    password = request.POST['password']
    user = authenticate(request, username=login, password=password)
    if user is not None:
        lgn(request, user)
        h = HistoryNote(user=user, date=timezone.now(), text="Пользователь вошел в систему")
        h.save()
        if not hasattr(user, 'user_info'):
            u_info = User_info(user=user, money=10000)
            u_info.save()
        return redirect('index')
    else:
        return make_message(request, 'Неправильный логин или пароль')#HttpResponse("FAIL")
    #return HttpResponse(request.POST['login'] + '*' + request.POST['password'])#HttpResponseRedirect('')


def index(request):
    if request.user.is_authenticated:
        cheques = Cheque.objects.filter(author=request.user).order_by('-id')[:10]
        info = {
            'u': request.user,
            'ch_list': cheques,
        }
        return render(request, 'cheque/profile.html', info)
    else:
        return redirect('login_page')

def make_cheque(request):
    if request.user.is_authenticated:
        return render(request, 'cheque/index_page.html', {'user': request.user})
    else:
        return redirect('login_page')

def process_cheque(request):
    if request.user.is_authenticated:
        try:
            amount = int(request.POST['amount'])
        except ValueError:
            return make_message(request, "Введите целое число для перевода")
            amount = 0
        u = request.user
        if u.user_info.money - amount >= 0:
            s = ''
            for i in range(5):
                s += str(rnd(1, 9))
            while len(Cheque.objects.filter(sequrity_code=int(s))) != 0:
                s += 1
                s %= 100000
            ch = Cheque(author=u, amount=amount, activated=False, sequrity_code=int(s))
            ch.save()
            info = {
                'u': request.user,
                'ch': ch,
                'status_color': 'red' if ch.activated else 'green',
                'status': 'Активирован' if ch.activated else 'НЕ активирован',
                'code': ' '.join(list(s)),
            }
            h = HistoryNote(user=request.user, date=timezone.now(), text='Вы выписали чек №{}'.format(ch.id))
            h.save()
            return render(request, 'cheque/show_cheque.html', info)
        else:
            return make_message(request, "У Вас недостаточно средств на такой чек")
        #return HttpResponse("Cheque {}".format(amount))
    else:
        return redirect('login_page')


def show_cheque(request, cheque_id):
    if request.user.is_authenticated:
        try:
            ch = Cheque.objects.get(pk=cheque_id)
            if request.user.id != ch.author.id and (not request.user.is_superuser):
                return make_message(request, "Вы не имеете доступа к этому чеку")#HttpResponse("Это не ваш чек")
            st_cl = 'red' if ch.activated else 'green'
            st = 'Активирован' if ch.activated else 'НЕ активирован'
            cd = ' '.join(list(str(ch.sequrity_code)))
            info = {
                'u': request.user,
                'ch': ch,
                'status_color': st_cl,
                'status': st,
                'code': cd,
            }
            return render(request, 'cheque/show_cheque.html', info)
        except ObjectDoesNotExist:
            if request.user.is_superuser:
                return make_message(request, 'Такого чека не существует')
            else:
                return make_message(request, "Вы не имеете доступа к этому чеку")
    else:
        return redirect('login_page')

def activate_cheque(request):
    if request.user.is_authenticated:
        return render(request, 'cheque/activate_cheque_page.html', {})
    else:
        return redirect('login_page')

def activate_cheque_process(request):
    u = request.user
    try:
        code = int(request.POST['code'])
    except ValueError:
        return make_message(request, "Код актвации должен состоять из 5 подряд идущих целых чисел.")
    try:
        ch = Cheque.objects.get(sequrity_code=code)
        if ch.activated:
            return make_message(request, "Чек уже был активирован")
        elif ch.author.user_info.money - ch.amount < 0 or u.user_info.money + ch.amount < 0:
            ch.activated = True
            ch.save()
            return make_message(request, "У одного из лиц (принимающего или отправляющего) недостаточно средств для операции")
        else:
            ch.activated = True
            ch.save()
            if u.id == ch.author.id:
                return make_message(request, 'Вы пытаетесь обналичить собственный чек. Чек деактивирован')
            else:
                if not u.is_superuser:
                    u.user_info.money += ch.amount
                    u.user_info.save()
                if not ch.author.is_superuser:
                    ch.author.user_info.money -= ch.amount
                    ch.author.user_info.save()
                h = HistoryNote(user=request.user, date=timezone.now(), text="Вы получили чек №{} на сумму {} CR от пользователя {}".format(ch.id, ch.amount, ch.author.username))
                h.save()
                h = HistoryNote(user=ch.author, date=timezone.now(), text="Пользователь {} обналичил Ваш чек №{} на сумму {} CR".format(request.user.username, ch.id, ch.amount))
                h.save()
            return redirect('index')
    except ObjectDoesNotExist:
        return make_message(request, 'Не существует такого чека')


def logout_process(request):
    lgt(request)
    return redirect('index')

def history(request):
    if request.user.is_authenticated:
        evs = HistoryNote.objects.filter(user=request.user).order_by('-date')
        info = {
            'u': request.user,
            'evs': evs,
        }
        return render(request, 'cheque/history.html', info)
    else:
        return redirect('login_page')


def user_view(request, user_id):
    return make_message(request, 'Страница находится в состоянии разработки')



