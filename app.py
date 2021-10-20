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
def whatsyourname():

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
def gamelist():
        articles = Article.query.all()
        return render_template("gameselection.html", articles=articles)


def gameadd():
    if request.method == "POST":
        gamename = request.form['gamename']

        article = Article(gamename=gamename)

        try:
            db.session.add(article)
            db.session.commit()
            text = "Готово"
            return render_template("gameselection.html", text=text)
        except:
            return "При добавлении игры произошла ошибка"

    else:
        return render_template("gameselection.html")






if __name__ == "__main__":
    app.run(debug=True)
