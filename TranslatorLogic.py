from models import Words, UsersTable
from settings import session
from sqlalchemy import update, func, desc
from JWT_OP import create_access_token
import random

random_type = [None]
y = 0
word_lang = None


class UserActions():
    def add_user(self, name, password):
        x = session.query(UsersTable).filter(UsersTable.login==name).all()
        if x:
            return "this name is already registered"
        else:
            session.add(UsersTable(login=name, password=password, points=0))
            session.commit()
            jwt_payload = {"login": name}
            jwt_token = create_access_token(jwt_payload)
            return f"account created, your token is: ' {jwt_token} '"

    def login(self, login, password):
        info = session.query(UsersTable).filter(UsersTable.login == login, UsersTable.password == password).first()
        if info:
            jwt_payload = {"login": login}
            jwt_token = create_access_token(jwt_payload)
            return f"your token is: ' {jwt_token} '"
        else:
            return "that`s wrong information"


acts = UserActions()


def check_alphabet(txt, func):
    if 'А' <= txt[0] <= 'я':
        return func(txt, Words.eng, Words.ua)
    elif 'A' <= txt[0] <= 'z':
        return func(txt, Words.ua, Words.eng)


def translate_func(txt, frst, scnd):
    results = session.query(frst).filter(scnd == txt).all()
    if results:
        second_column_values = [result[0] for result in results]
        return second_column_values
    else:
        return f"Unfortunately, there are no words like {txt}"


def add_words(eng, ua):
    user = Words(ua=ua, eng=eng)
    session.add(user)
    session.commit()
    return "Word added"


def del_word(txt, frst, scnd):
    deleting_obj = session.query(Words).filter(scnd == txt).first()
    if deleting_obj:
        session.delete(deleting_obj)
        session.commit()
        return "Word was deleted"
    else:
        return f"Unfortunately, there is no word like {txt}"


def get_number(txt):
    global y, x, word_lang

    if txt == "ua":
        word_lang = [0, 1]

    elif txt == "eng":
        word_lang = [1, 0]

    results = session.query(Words.ua, Words.eng).all()
    values = [result[word_lang[0]] for result in results]
    y = random.randint(0, len(values)-1)

    obj = session.query(Words.ua, Words.eng).order_by(func.random()).limit(3).all()
    random_objects = [result[word_lang[1]] for result in obj]
    random_objects.append([result[word_lang[1]] for result in results][y])
    random.shuffle(random_objects)
    return f"{values[y]}, {random_objects}"


def updating_res(filt, login, eq):
    points_value = f"{filt[0]}{eq}{1}"
    new_points = eval(points_value)
    session.execute(
        update(UsersTable).where(UsersTable.login == login["login"]).values({UsersTable.points: new_points}))
    session.commit()


def check_test(txt, login):
    results = session.query(Words.ua, Words.eng).all()
    values = [result[word_lang[1]] for result in results]
    filt = session.query(UsersTable.points).filter(UsersTable.login == login["login"]).first()
    print(txt, values[y])
    if txt == values[y]:
        if filt:
            updating_res(filt, login, "+")
            return "good, you won"
        else:
            return "User not found"
    else:
        updating_res(filt, login, "-")
        return "that isn't right:("


def edit_word(words_list, frst, scnd):
    filt = update(Words).where(scnd == words_list[1]).values({scnd: words_list[1]})
    session.execute(filt)
    session.commit()
    return "Word edited successfully"


def top():
    last_three_records = session.query(UsersTable).order_by(desc(UsersTable.points)).limit(3).all()
    users_list = {}
    for user in reversed(last_three_records):
        users_list.update({user.points: user.login})
    return users_list