from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def pesquisar():
    if request.method == "POST":
        tipoConsulta = request.form["input"]
        return redirect(url_for("consultarDB", pesquisa=tipoConsulta))
    else:
        return render_template("search.html", content="Tipo de consulta")

@app.route("/consulta/<pesquisa>", methods=["POST", "GET"])
def consultarDB(pesquisa):
    if request.method == "POST":
        consulta = request.form["input"]
        return f"consulta de {pesquisa} no DB sobre {consulta}: RESULTADO"
    else:
        return render_template("search.html", content=f"Consultar {pesquisa}")

# if __name__ == '__main__':
#     app.run(debug=True)

# para usar o gunicorn:
# 1) pip install gunicorn
# 2) gunicorn app:app
# *só funciona no linux