from flask import Flask, render_template, url_for, request


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/summ', methods=["POST", "GET"])
def summ():
    if request.method == "GET":
        return render_template("summ.html", c="Введите значение a и b и нажмите \"Вычислить\"")

    if request.method == "POST":
        a = request.form["a"]
        b = request.form["b"]
        c = None
        try:
            a, b = int(a), int(b)
            c = int(a) + int(b)
        except:
            c = "a и b должны быть числами"
        return render_template("summ.html", c=c)




if __name__ == "__main__":
    app.run(debug=True)
