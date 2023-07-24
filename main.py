from settings import app
from BackLogic import translate_func, add_words, del_word, check_alphabet, get_number, check_test, edit_word, acts, top
from JWT_OP import verify_token
from fastapi import Depends
from models import AddWord, EditWord, CreateUser


@app.post("/add/account")
async def account(txt: CreateUser):
    return acts.add_user(txt.login, txt.password)


@app.post("/login")
async def log(txt: CreateUser):
    return acts.login(txt.login, txt.password)


@app.get("/records")
async def best():
    return top()

@app.post("/add/word")
async def add_word(txt: AddWord):
    add_words(txt.eng.lower(), txt.ua.lower())


@app.get("/")
async def fing_word(txt: str):
    return check_alphabet(txt.lower(), translate_func)


@app.delete("/del")
async def delete(txt: str):
    return check_alphabet(txt.lower(), del_word)


@app.get("/test")
def take_number(txt: str):
    return get_number(txt)


@app.get("/check/resault")
async def check(txt: str, decoded_token: dict = Depends(verify_token)):
    return check_test(txt.lower(), decoded_token)


@app.put("/edit")
async def edit(txt: EditWord):
    return check_alphabet([txt.before_word, txt.after_word], edit_word)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)