### INSTA_COMMENTER ###

Необходимо иметь запущщенный **postgres** сервер

Все настройки в **settings.py**


Установи **firefox-geckodriver** на свою тачку. В Ubuntu это:\
`sudo apt install firefox-geckodriver`

`python3 -m venv env`

`source env/bin/activate`

`pip i -r requirements.txt`

`python3 insta_commenter.py -m 1`

#### modes: ####
- 0 - обнулить всех целевых пользователей
- 1 - получение подписчиков с целевой страницы
- 2 - создание комментария с указанием пользователей, их колличество в settings.py
- 3 - непрерывные процесс комментирования, период в settings.py
