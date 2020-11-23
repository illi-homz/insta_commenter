login = 'illi_homz'
password = 'badbalance166998'
target_url = 'https://www.instagram.com/igromania/' # страница с пользователями
# target_url = [ # или списком публикаций
#     'https://www.instagram.com/matryoshka_games/',
#     'https://www.instagram.com/igra4ch/'
# ]

post_url = 'https://www.instagram.com/p/CFSAKpaoVy9/' # пост на фейковой странице
# post_url = ['https://www.instagram.com/p/CFSAKpaoVy9/'] # или списком публикаций

main_page = 'novusis' # рекламируемая страница
need_users_add = 4 # по сколько пользователей добавлять
hours = 1 # интервал, в часах

browser='chrome' # or rirefox

db_data = {
    'db': 'insta_poster',
    'user': 'postgres',
    'password': 'bad'
}
table_name = 'folowers'

text = f"""Привет чел!!! Мы тут тебе предлагаем какую то хрень на вот зацени
{'='*10}
Вот тут: @{main_page}
{'='*10}
"""
