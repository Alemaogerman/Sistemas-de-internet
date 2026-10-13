from flask import Flask, redirect, url_for, render_template, request, jsonify
import psycopg2

# host = db-server 
# port = 5432 ou 5433
# database = dados_governo
# user = postgres
# password = postgres

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

try:
    conn = psycopg2.connect(host="localhost",
                            port="5433",
                            database="dados_governo",
                            user="postgres",
                            password="postgres")
    
    print("Banco de dados conectado")

except:
    print(f"Erro ao conectar o db!")

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/api/servidores", methods=["POST", "GET"])
def consulta():
    args = request.args.to_dict()

    argsPermitidos = ["nome", "cargo", "uf", "orgao", "limit", "similar"]

    argsCarreiras = {
                     "nome": "nome",
                     "cargo": "descricao_cargo_emprego",
                     "uf": "uf_upag_vinculacao",
                     "orgao": "denominacao_orgao_atuacao"
                    }

    argsAposentados = {
                       "nome": "nome",
                       "cargo": "cargo",
                       "orgao": "nome_orgao"
                      }

    print(args)

    cur = conn.cursor()

    parametrosCarreira = []
    parametrosAposentados = []
    condicoesCarreira = []
    condicoesAposentados = []
    limite = None

    for arg, value in args.items():
        if arg in argsPermitidos:
            if arg == "limit":
                limite = value

            elif arg == "similar":
                condicoesCarreira.append(f"{argsCarreiras['nome']} LIKE %s") ################
                condicoesAposentados.append(f"{argsAposentados['nome']} LIKE %s") ################

                parametrosCarreira.append(value.upper())
                parametrosAposentados.append(value.upper())

            elif arg == "uf":
                condicoesCarreira.append(f'{argsCarreiras[arg]} = %s')
                parametrosCarreira.append(value.upper())

            else:
                condicoesCarreira.append(f'{argsCarreiras[arg]} = %s')
                condicoesAposentados.append(f'{argsAposentados[arg]} = %s')
                parametrosCarreira.append(value.upper())
                parametrosAposentados.append(value.upper())

    comandoCarreira = "SELECT * FROM carreira" # aposentados / carreira
    comandoAposentados = "SELECT * FROM aposentados" # aposentados / carreira

    comandoCarreira += " WHERE " + " AND ".join(condicoesCarreira)
    comandoAposentados += " WHERE " + " AND ".join(condicoesAposentados)

    if limite:
        comandoCarreira += " LIMIT %s"
        comandoAposentados += " LIMIT %s"
        parametrosCarreira.append(limite)
        parametrosAposentados.append(limite)

    conn.rollback() # debug

    cur.execute(comandoCarreira, parametrosCarreira)
    nomesColunaCarreira = [desc[0] for desc in cur.description]
    print(f"NOMES COLUNAS DE CARREIRA: {nomesColunaCarreira}")

    resultadoCarreira = cur.fetchall()

    cur.execute(comandoAposentados, parametrosAposentados)
    nomesColunaAposentados = [desc[0] for desc in cur.description]
    print(f"NOMES COLUNAS DE APOSENTADOS: {nomesColunaAposentados}")

    resultadoAposentados = cur.fetchall()

    print(f'----------resultado CARREIRA---------: {resultadoCarreira}')
    print(f'----------resultado APOSENTADOS--------: {resultadoAposentados}')

    jsonOutput = {}
    jsonOutput["carreira"] = []
    jsonOutput["aposentados"] = []

    for result in resultadoCarreira:
        registro = {}
        for i in range(0, len(nomesColunaCarreira)):
            registro[nomesColunaCarreira[i]] = result[i]

        jsonOutput["carreira"].append(registro)

    for result in resultadoAposentados:
        registro = {}
        for i in range(0, len(nomesColunaAposentados)):
            registro[nomesColunaAposentados[i]] = result[i]

        jsonOutput["aposentados"].append(registro)

    cur.close()

    return jsonify(jsonOutput)

if __name__ == '__main__':
    app.run(debug=True)

# para usar o gunicorn:
    # 1) pip install gunicorn
    # 2) comentar o if __name__ == '__main__'
    # 3) gunicorn app:app no terminal para rodar
    # *só funciona no linux

# flask tem que rodar em linux para conectar ao banco de dados
# o banco de dados deverá estar no docker seguindo o leiame da branch DB

# em caso de colocar esse código no docker, é preciso
# trocar em conn o host="localhost" por host="db-server"

# busca por cargo - OK
# busca por uf - deu erro
# busca por instituição/órgão - OK
# busca por similaridade - OK
