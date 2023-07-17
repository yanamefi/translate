from models import Words
from settings import session
from sqlalchemy import update, func
import random

random_type = [None]
y = 0


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


def del_word(txt, frst, scnd):
    deleting_obj = session.query(Words).filter(scnd == txt).first()
    if deleting_obj:
        session.delete(deleting_obj)
        session.commit()
        return "Word was deleted"
    else:
        return f"Unfortunately, there is no word like {txt}"


def get_number(txt):
    random_type = [Words.ua, Words.eng]
    global y, x
    if txt == "ua":
        txt = Words.ua
    elif txt == "eng":
        txt = Words.eng
    results = session.query(txt).all()
    second_column_values = [result[0] for result in results]
    y = random.randint(0, len(second_column_values)-1)
    random_type.remove(txt)
    random_objects = session.query(random_type[0]).order_by(func.random()).limit(3).all()
    return f"{second_column_values[y]}, {random_objects}"


def check_test(txt):
    print(random_type)
    results = session.query(random_type[0]).all()
    second_column_values = [result[0] for result in results]
    print(y)
    if txt == second_column_values[y]:
        return "good, you won"
    else:
        return "that isn`t right:("


def edit_word(words_list, frst, scnd):
    filt = update(Words).where(scnd == words_list[0]).values({scnd: words_list[1]})
    session.execute(filt)
    session.commit()
    return "Word edited successfully"

