from flask import Flask, redirect, url_for, render_template, request
import psycopg2

# host = db-server 
# port = 5432
# database = dados_governo
# user = postgres
# password = postgres

app = Flask(__name__)

try:
    conn = psycopg2.connect(host="localhost",
                            port="5432",
                            database="dados_governo",
                            user="postgres",
                            password="postgres")
    
    print("Banco de dados conectado")

except:
    print(f"Erro ao conectar o db!")

@app.route("/api/servidores", methods=["POST", "GET"])
def consulta():
    args = request.args.to_dict()

    argsCarreiras = {"nome": "nome",
                     "cargo": "descricao_cargo_emprego",
                     "uf": "uf_upag_vinculacao",
                     "orgao": "denominacao_orgao_atuacao"
                     }

    print(args)

    cur = conn.cursor()

    parametros = []
    condicoes = []
    limite = None

    for arg, value in args.items():
        if arg == "limite":
            limite = int(value)
        else:
            condicoes.append(f'{argsCarreiras[arg]} = %s')
            parametros.append(value)

    comando = "SELECT * FROM carreira" # aposentados / carreira

    if condicoes:
        comando += " WHERE " + " AND ".join(condicoes)

    if limite:
        comando += " LIMIT %s"
        parametros.append(limite)

    print(comando)
    print(parametros)

    conn.rollback() # debug
    cur.execute(comando, parametros)

    print(condicoes)

    resultado = cur.fetchall()

    print(f'resultado: {resultado}')

    cur.close()

    return resultado

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