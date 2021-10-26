from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamebase.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beansbase.db'
app.config['SQLALCHEMY_BINDS'] = {
    'games': 'sqlite:///gamebase.db',
    'beans': 'sqlite:///beansbase.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# База данных для игр
class Article(db.Model):
    __bind_key__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    gamename = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Article %r' % self.id


# База данных для Beans_Project
class BeansBasket(db.Model):
    __bind_key__ = 'beans'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<BeansBasket: {self.id} {self.date} {self.count}'


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
        elif request.form.get("game_random"):
            result_random = game_random()
            articles = Article.query.all()
            return render_template("gameselection.html", result_random=result_random, articles=articles)

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
        # f - форматированная строка. Применяется, когда нужно передать переменную
        result = f"При удалении игры произошла ошибка: {e}"
    return result


def game_random():
    articles = Article.query.all()
    # Проверка на вхождение элементов (есть ли хотя бы 1 элемент)
    if articles:
        result = random.choice(articles).gamename
    else:
        result = "В базе ничего нет"
    return result


@app.route('/test', methods=["POST", "GET"])
def test():
    if request.method == "GET":
        return render_template("test.html", answer="press the button")
    if request.method == "POST":
        answer = "nothing_to show"
        template = "You pressed "
        if request.form.get("a"):
            answer = get_c(template + request.form["a"])
        elif request.form.get("b"):
            answer = get_c(template + request.form["b"])
        return render_template("test.html", answer=answer)


def get_c(ans):
    answer = ans
    return answer


@app.route('/beans', methods=["POST", "GET"])
def beans_project():
    if request.method == "POST":
        description = request.form['description']
        count = request.form['count']

        beans_basket = BeansBasket(description=description, count=count)

        try:
            db.session.add(beans_basket)
            db.session.commit()
            beans = BeansBasket.query.order_by(BeansBasket.date.desc()).all()
            filtered_beans = beans[0:10]
            summ = beans_calculate(beans_list=beans)
            return render_template("beans.html", beans=filtered_beans, summ=summ)
        except Exception as e:
            return f"При добавлении записи произошла ошибка: {e}"
    else:
        beans = BeansBasket.query.order_by(BeansBasket.date.desc()).all()
        filtered_beans = beans[0:10]
        summ = beans_calculate(beans_list=beans)
        return render_template("beans.html", beans=filtered_beans, summ=summ)


def beans_calculate(beans_list):
    summ = 0
    for el in beans_list:
        summ += el.count
    return summ




if __name__ == "__main__":
    app.run(debug=True)
