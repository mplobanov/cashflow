# Сервис для игры Денежный Поток (Cashflow)

Это сервис, автоматизирующий бумажную работу в игре Cashflow (аналог Монополии).
Работает на Django.

На данный момент реализована система чеков.

## Система чеков

Система чеков позволяет участникам обмениваться деньгами.

Алгоритм таков: 
1. Участник получает от администратора логин и пароль, на аккаунте уже есть какое-то базовое количество денег.
2. Когда участнику нужно совершить сделку с другим участником, он выписывает чек на сайт и показывает карточку чека партнеру.
3. Если участнику нужно получить еньги по чеку (обналичить чек), то он вводит код активации и деньги поступают на его счет.
4. Участник не может выписать чек на сумму больше, чем у него есть сейчас.

Участнику и администрации доступна история транзакций.<br>

<strong>ВНИМАНИЕ</strong> Участники могут выписать чек на отрицательную сумму. Тогда сумма спишется у того, кто <strong>активирует чек</strong>. Вот почему обязательно не устно сообщать партнеру код, а показывать карточку чека.

## Сервис администратора

Для выполнения роли банка доступен функционал администратора. Он позволяет управлять пользователями (создавать новых) и вести рассчеты. <br>

<strong>Если пользователь имеет статус суперпользователя, то его счет бесконечен и не изменяется при активации чеков.</strong> 

Чтобы заупстить сервис на локальной машине, скачайте репозиторий, перейдите в папку cashflow (верх.) и выполните  
```python manage.py runserver```
Сервис будет доступен по `127.0.0.1:8000`

Сервис администрации `127.0.0.1:8000/admin`

Демо-пользователи:
<strong>admin</strong> - admin <br>
user1 - python3.7 <br>
user2 - python3.7 <br>