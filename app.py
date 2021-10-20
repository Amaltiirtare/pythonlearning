from flask import Flask, render_template, url_for, request


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


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
if __name__ == "__main__":
    app.run(debug=True)
