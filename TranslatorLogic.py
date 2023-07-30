from models import Words, UsersTable
from settings import session
from sqlalchemy import update, func, desc
import random


def check_alphabet(txt, func):
    if 'А' <= txt[0] <= 'я':
        return func(txt, Words.eng, Words.ua)
    elif 'A' <= txt[0] <= 'z':
        return func(txt, Words.ua, Words.eng)
    else:
        return "we support only"


def translate_func(txt, frst, scnd):
    results = session.query(frst).filter(scnd == txt).all()
    if results:
        column_values = [result[0] for result in results]
        return column_values
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


def text_changing(txt):
    if txt == "ua":
        word_lang = [0, 1]

    elif txt == "eng":
        word_lang = [1, 0]

    return word_lang


def get_number(txt):
    # word_lang = text_changing(txt)
    fields = [Words.ua, Words.eng] if txt == "ua" else [Words.eng, Words.ua]
    results = session.query(*fields).order_by(func.random()).limit(5).all()
    choices = [results[0][1]] + [i[1] for i in results[1:4]]
    # print(results, type(results))
    # values = [result[word_lang[0]] for result in results]
    # y = random.randint(0, len(values)-1)
    #
    # obj = session.query(Words.ua, Words.eng).order_by(func.random()).limit(3).all()
    # random_objects = [result[word_lang[1]] for result in obj]
    # random_objects.append([result[word_lang[1]] for result in results][y])
    # random.shuffle(random_objects)
    dct = {"origin": results[0][0], "choices": choices}
    return dct


def updating_result(filt, login, eq):
    points_value = f"{filt[0]}{eq}{1}"
    new_points = eval(points_value)
    session.execute(
        update(UsersTable).where(UsersTable.login == login["login"]).values({UsersTable.points: new_points}))
    session.commit()


def check_test(original, txt, lang, login):
    word_lang = {Words.eng: Words.ua}
    if lang == "ua":
        word_lang = {Words.ua: Words.eng}
    filt = session.query(UsersTable.points).filter(UsersTable.login == login["login"]).first()
    values = session.query(next(iter(word_lang.values()))).filter(next(iter(word_lang.keys())) == original).first()
    if txt == values[0]:
        if filt:
            updating_result(filt, login, "+")
            return "good, you won"
        else:
            return "User not found"
    else:
        updating_result(filt, login, "-")
        return "that isn't right:("


def edit_word(words_list, frst, scnd):
    filt = update(Words).where(scnd == words_list[0]).values({scnd: words_list[1]})
    session.execute(filt)
    session.commit()
    return "Word edited successfully"


def top():
    last_three_records = session.query(UsersTable).order_by(desc(UsersTable.points)).limit(3).all()
    users_list = []
    for user in last_three_records:
        users_list.append({user.login: user.points})
    return users_list