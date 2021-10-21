from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamebase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Работа с базой данных
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gamename = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Article %r' % self.id


# Показать главную страницу
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


# Вычисление суммы двух чисел
@app.route('/summ', methods=["POST", "GET"])
def summ():
    if request.method == "GET":
        return render_template("summ.html")

    if request.method == "POST":
        a = request.form["a"]
        b = request.form["b"]
        try:
            a, b = int(a), int(b)
            c = a + b
        except:
            c = "Вы не ввели 2 числа. Повторте попытку."

        return render_template("summ.html", a=a, b=b, c=c)


# Как тебя зовут?
@app.route('/whatsyourname', methods=["POST", "GET"])
def what_is_your_name():

    if request.method == "GET":
        return render_template("whatsyourname.html")

    if request.method == "POST":
        username = request.form["username"]
        if not username:
            hi = "Вы ничего не ввели"
        else:
            hi = "Привет, " + username + "!"
        return render_template("whatsyourname.html", username=username, hi=hi)


# Выбор игры
@app.route('/gameselection', methods=["POST", "GET"])
def game_selection():
    """
    Отображение списка игр
    """
    if request.method == "POST":
        if request.form.get('game_add'):
            game_name = request.form["game_name"]
            result = game_add(game_name=game_name)
            articles = Article.query.all()
            return render_template("gameselection.html", result=result, articles=articles)
        elif request.form.get("game_delete"):
            game_name = request.form["game_name"]
            result = game_delete(game_name=game_name)
            articles = Article.query.all()
            return render_template("gameselection.html", result=result, articles=articles)

    else:
        articles = Article.query.all()
        return render_template("gameselection.html", articles=articles)


def game_add(game_name):
    """
    Ввод данных в БД
    """
    if not game_name:
        return "Вы ничего не ввели"
    articles = Article.query.all()
    for el in articles:
        if game_name == el.gamename:
            return "Такая игра уже есть в базе"
    article = Article(gamename=game_name)

    try:
        db.session.add(article)
        db.session.commit()
        result = "Готово"
    except:
        result = "При добавлении игры произошла ошибка"
    return result


def game_delete(game_name):
    """
    Удалее данных из БД
    """
    if not game_name:
        return "Вы ничего не ввели"
    articles = Article.query.all()
    try:
        found = False
        for el in articles:
            if game_name == el.gamename:
                found = True
                db.session.delete(el)
                db.session.commit()
        if found:
            result = "Запись удалена"
        else:
            result = "Такой записи нет в базе"
    except Exception as e:
        result = f"При удалении игры произошла ошибка: {e}"
    return result


if __name__ == "__main__":
    app.run(debug=True)
