login = ''
password = ''
target_url = '' # страница с пользователями

post_url = '' # пост на фейковой странице
# post_url = [''] # или списком публикаций

main_page = '' # рекламируемая страница
need_users_add = 4 # по сколько пользователей добавлять
hours = 1 # интервал, в часах

browser='chrome' # or rirefox

db_data = {
    'db': '',
    'user': 'postgres',
    'password': ''
}
table_name = 'folowers'

text = f"""Привет чел!!! Мы тут тебе предлагаем какую то хрень на вот зацени
{'='*10}
Вот тут: @{main_page}
{'='*10}
"""
