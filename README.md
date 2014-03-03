
установка старая версия!! aptitude install python-django

установка pip

apt-get install python-pip

установка последней версии
sudo pip install Django

апгрэйд до последней
sudo pip install Django --upgrade

конфигурация пользователей прав доступа админки
python manage.py syncdb

создание приложения
python manage.py startapp tasks

python manage.py sql tasks

python manage.py syncdb

$ python manage.py runserver
$ python manage.py runserver 0.0.0.0:8000
email debug

python -m smtpd -n -c DebuggingServer localhost:1025 &

valera 111111

все это здесь
http://djbook.ru/rel1.6/intro/tutorial01.html

http://127.0.0.1:8000/tasks/
http://127.0.0.1:8000/admin/

установка регистрации
   pip install django-registration

http://habrahabr.ru/post/74165/
