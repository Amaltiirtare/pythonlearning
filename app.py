from flask import Flask, render_template, url_for, request


app = Flask(__name__)


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
        hi = "Привет, " + username + "!"


#        hi = "Вы ничего не ввели"

    return render_template("whatsyourname.html", username=username, hi=hi)


if __name__ == "__main__":
    app.run(debug=True)
