login = ''
password = ''
target_url = '' # страница с пользователями
post_url = '' # пост на фейковой странице
main_page = '' # основная страница
need_users_add = 10 # по сколько пользователей добавлять
hours = 1 # интервал, в часах

db_data = {
    'db': 'insta_poster',
    'user': 'postgres',
    'password': 'bad'
}

text = f"""Привет чел!!! Мы тут тебе предлагаем какую то хреньб на вот зацени
{'='*10}
Вот тут: @{main_page}
{'='*10}
"""
