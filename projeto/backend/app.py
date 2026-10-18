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

except Exception as e:
    print(f"Erro ao conectar o db {e}!")

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
                condicoesCarreira.append(f"UPPER(TRIM({argsCarreiras['nome']})) LIKE %s") ################
                condicoesAposentados.append(f"UPPER(TRIM({argsAposentados['nome']})) LIKE %s") ################

                parametrosCarreira.append(value.upper())
                parametrosAposentados.append(value.upper())

            
            elif arg == "uf":
                condicoesCarreira.append(f'UPPER({argsCarreiras[arg]}) = %s')
                parametrosCarreira.append(value.strip().upper())
                
                condicoesAposentados.append("1 = 0")

            elif arg in ("cargo", "orgao"):
                condicoesCarreira.append(f'UPPER({argsCarreiras[arg]})LIKE %s')
                condicoesAposentados.append(f'UPPER({argsAposentados[arg]}) LIKE %s')

                parametrosCarreira.append(f'%{value.strip().upper()}%')
                parametrosAposentados.append(f'%{value.strip().upper()}%')

            elif arg == "nome":
                condicoesCarreira.append("UPPER(TRIM(nome)) = %s")
                condicoesAposentados.append("UPPER(TRIM(nome)) = %s")

                parametrosCarreira.append(value.strip().upper())
                parametrosAposentados.append(value.strip().upper())

            else:
                condicoesCarreira.append(f'{argsCarreiras[arg]} = %s')
                condicoesAposentados.append(f'{argsAposentados[arg]} = %s')
                parametrosCarreira.append(value.upper())
                parametrosAposentados.append(value.upper())


    comandoCarreira = "SELECT * FROM carreira"
    comandoAposentados = "SELECT * FROM aposentados"

    if condicoesCarreira:
        comandoCarreira += " WHERE " + " AND ".join(condicoesCarreira)

    if condicoesAposentados:
        comandoAposentados += " WHERE " + " AND ".join(condicoesAposentados)

    # O limite é aplicado somente quando foi solicitado.
    if limite is not None:
        comandoCarreira += " LIMIT %s"
        comandoAposentados += " LIMIT %s"

        parametrosCarreira.append(limite)
        parametrosAposentados.append(limite)


    cur.execute(comandoCarreira, parametrosCarreira)
    nomesColunaCarreira = [desc[0] for desc in cur.description]
    resultadoCarreira = cur.fetchall()

    cur.execute(comandoAposentados, parametrosAposentados)
    nomesColunaAposentados = [desc[0] for desc in cur.description]
    resultadoAposentados = cur.fetchall()
    

    print(f'----------resultado CARREIRA---------: {resultadoCarreira}')
    print(f'----------resultado APOSENTADOS--------: {resultadoAposentados}')

    
    jsonOutput = {
        "carreira": [
            dict(zip(nomesColunaCarreira, resultado))
            for resultado in resultadoCarreira
        ],
        "aposentados": [
            dict(zip(nomesColunaAposentados, resultado))
            for resultado in resultadoAposentados
        ]
    }

    if not jsonOutput["carreira"] and not jsonOutput["aposentados"]:
        jsonOutput["mensagem"] = ("Nenhum registro foi encontrado para essa consulta.")

    
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
