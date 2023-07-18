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
    global y, x

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


def check_test(txt):
    results = session.query(Words.ua, Words.eng).all()
    values = [result[0] for result in results]
    if txt == values[y]:
        return "good, you won"
    else:
        return "that isn`t right:("


def edit_word(words_list, frst, scnd):
    filt = update(Words).where(scnd == words_list[1]).values({scnd: words_list[1]})
    session.execute(filt)
    session.commit()
    return "Word edited successfully"

