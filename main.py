from settings import app
from BackLogic import translate_func, add_words, del_word, check_alphabet, get_number, check_test, edit_word
from models import AddWord, EditWord


@app.post("/add")
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
async def check(txt:str):
    return check_test(txt.lower())


@app.put("/edit")
async def edit(txt: EditWord):
    return check_alphabet([txt.before_word, txt.after_word], edit_word)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)