import time
import os
import sys
from random import randint

from selenium import webdriver

import db
import settings


class BaseClass:
    def __init__(self, browser):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.image_path = self.BASE_DIR + '/logo.jpg'
        self.folowers_url_list = []
        self.folowers_count = 0
        self.complete_folowers_list = []
        self.added_to_base = 0
        self.browser = browser
        self.Followers = None

    def init_db_and_user(self, *args, **kwargs):
        connect = db.connect_to_db(**kwargs)
        self.Followers = db.Folowers(connect)
        if not self.Followers.check_on_table_created():
            self.Followers.create_table()


class Loginer(BaseClass):
    def __init__(self, browser):
        super().__init__(browser)

    def login(self):
        # Вход в аккаунт
        self.browser.get('https://instagram.com/accounts/login')
        time.sleep(4)
        input_fields = self.browser.find_elements_by_class_name('_2hvTZ')
        submit_button = self.browser.find_element_by_class_name('L3NKy')
        input_fields[0].send_keys(settings.login)
        input_fields[1].send_keys(settings.password)
        submit_button.click()
        time.sleep(4)
        errors = self.browser.find_elements_by_css_selector('#error_message')
        if errors:
            print('bad login')
            return


class FolowersGetter(BaseClass):
    def __init__(self, browser):
        super().__init__(browser)

    def no_complet_controll(self):
        no_complete_urls = self.Followers.get_data_from_column_param_user('completed', False)
        if no_complete_urls:
            return [url[1] for url in no_complete_urls]
        return []

    def get_count_folowers(self):
        link_on_folowers = self.browser.find_elements_by_class_name('g47SY ')
        return int(link_on_folowers[1].get_attribute('title').replace(' ', ''))

    def open_list_folowers_and_get_followers_win(self):
        # Открываю окно с подписчиками
        self.browser.find_elements_by_class_name('Y8-fY')[1].click()
        time.sleep(2)
        return self.browser.find_element_by_class_name('isgrP')

    def scroll(self, heigth=1):
        self.browser.execute_script(f'arguments[0].scrollTop = arguments[0].scrollHeight/{heigth}', self.followers_win)

    def get_folowers_urls(self):
        try:
            folowers = self.browser.find_elements_by_class_name('FPmhX')
            folowers = folowers[-250:len(folowers)]
            folowers = [f.get_attribute('href').split('/')[-2] for f in folowers]
            users_list = []
            for folower in folowers:
                check = self.Followers.check_follower_in_db(folower)
                if check:
                    if check[2]: # is completed
                        if folower not in self.complete_folowers_list:
                            self.complete_folowers_list.append(folower)
                            continue
                    users_list.append(folower)

                if folower not in users_list:
                    self.Followers.add_folower(folower)
                    self.added_to_base += 1
                    users_list.append(folower)
            if not users_list:
                print('Похоже что все пользователи уже в базе')
                return []
            return users_list
        except:
            return []

    def scroll_list_and_get_folowers_urls(self):
        heigth_list = [6, 4, 3, 2]
        map(self.scroll, heigth_list)
        num_scroll = 0

        while len(self.folowers_url_list) + len(self.complete_folowers_list) < self.folowers_count:
            num_scroll += 1
            self.scroll()
            if num_scroll % 10 == 0:
                self.folowers_url_list += self.get_folowers_urls()
                if not self.folowers_url_list:
                    print('Не могу найти пользователей')
                    break
                print('Всего: {0} Получил для обработки: {1} Добавлено в базу: {2} В пропуске: {3}'.format(
                    self.folowers_count,
                    len(self.folowers_url_list),
                    self.added_to_base,
                    len(self.folowers_url_list) + len(self.complete_folowers_list) - self.added_to_base
                ))
            time.sleep(randint(5, 20))

class Commenter(BaseClass):
    def __init__(self, browser):
        super().__init__(browser)

    def create_comment(self):
        users = self.folowers_url_list[:settings.need_users_add]
        self.folowers_url_list = self.folowers_url_list[settings.need_users_add:]
        if not users:
            print('Все пользователи обработаны')
            return False
        finally_text = settings.text
        for u in users:
            if u in self.complete_folowers_list:
                continue
            finally_text += f' @{u}'
            self.complete_folowers_list.append(u)
            self.Followers.set_is_completed(u)
        comment_field = self.browser.find_element_by_class_name('Ypffh')
        comment_field.click()
        time.sleep(1)
        comment_field = self.browser.find_element_by_class_name('focus-visible')
        comment_field.send_keys(finally_text)
        time.sleep(2)
        btn_add_comment = self.browser.find_element_by_class_name('y3zKF')
        btn_add_comment.click()
        time.sleep(1)
        print(f'Добавил пользователей: {users}')
        return True


class Runner(Loginer, FolowersGetter, Commenter):
    def __init__(self, browser):
        super().__init__(browser)

    def get_users(self):
        self.login()
        self.browser.get(settings.target_url)
        time.sleep(3)
        self.folowers_count = self.get_count_folowers() # для всех подписчиков
        print(f'Подписчиков на странице - {self.folowers_count}')
        self.followers_win = self.open_list_folowers_and_get_followers_win()
        self.scroll_list_and_get_folowers_urls()

    def public_creator(self):
        self.login()
        self.folowers_url_list = self.no_complet_controll()
        if not self.folowers_url_list:
            self.get_users()
            if not self.folowers_url_list:
                return False
        self.browser.get(settings.post_url)
        time.sleep(3)

        if self.create_comment():
            return True
        return False

    def set_all_is_not_completed(self):
        self.Followers.set_all_is_not_completed()


def control_args():
    if not settings.login:
        print('Error. Not login')
        return False
    if not settings.password:
        print('Error. Not password')
        return False
    return True

def start():
    if '-m' not in sys.argv or len(sys.argv) < 3:
        print('Error. Not -m parametr')
        return
    if not control_args():
        return
    mode = int(sys.argv[-1])
    if mode not in [1,2,3,4]:
        print('Не известный параметр')
        return

    db_params = settings.db_data
    browser = webdriver.Firefox()
    runner = Runner(browser)
    runner.init_db_and_user(**db_params)

    if mode == 1:
        if not settings.target_url:
            raise Exception('Error. Select mode 0, but not target_url')
        runner.get_users()
        browser.close()
    if mode == 2:
        runner.public_creator()
        browser.close()
    if mode == 3:
        while True:
            if not runner.public_creator():
                break
            time.sleep(60*60*settings.hours)
        browser.close()
    if mode == 4:
        answ = input('Обнулить всех пользователей, вы уверены? y/N: ')
        if answ == 'y':
            runner.set_all_is_not_completed()

if __name__ == '__main__':
    start()
