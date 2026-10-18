import requests
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# funções

def converter_data(data):
    data = data.strip()

    if not data:
        return ""

    return datetime.strptime(data, "%d%m%Y").strftime("%Y-%m-%d")



def baixar_arquivo(url, arquivo):

    print("Baixando arquivo...")

    resposta = requests.get(url, timeout=60)

    resposta.raise_for_status()

    arquivo.write_bytes(resposta.content)

    print(f"Download concluído: {arquivo}")

# expressao regular
def limpar_texto(texto):

    texto = re.sub(r"[^A-Za-z0-9\s;,.\-*]", "",  texto)
    return texto.strip()


def converter_valor(valor):

    # 1.621,00 -> 1621.00
    # 35.684,22 -> 35684.22

    valor = valor.strip()

    if not valor:
        return ""

    # formato br: 16.321,29
    if "," in valor:
        return valor.replace(".", "").replace(",", ".")

    # formato PostgreSQL: 16321.29
    return valor


#carreira

def limpar_carreira():

    
    print("\nCARREIRA")
    




    url_pasta = (
        "https://repositorio.dados.gov.br/"
        "segrt/Cargos%20e%20Carreiras/2026/"
    )

    nome_arquivo = "CARREIRA_072026.txt"

    arquivo_original = Path(nome_arquivo)

    arquivo_saida = Path("CARREIRA_072026_limpo.csv")


    

    print("Acessando a pasta...")

    resposta = requests.get(url_pasta,  timeout=60)
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")

    url_arquivo = None


    for link in soup.find_all("a", href=True):

        href = link["href"]

        if nome_arquivo.lower() in href.lower():

            url_arquivo = urljoin(url_pasta, href)
            break


    if url_arquivo is None:

        raise ValueError(
            f"Não foi encontrado o arquivo "
            f"{nome_arquivo}."
        )


    print("Arquivo encontrado:")
    print(url_arquivo)




    baixar_arquivo(url_arquivo, arquivo_original)

   # ler

    with open(arquivo_original, "r", encoding="cp1252") as arquivo:
        linhas = arquivo.readlines()


    print(f"Linhas encontradas: {len(linhas)}")
    linhas = linhas[2:]   
    linha_modelo = None


    for linha in linhas:

        linha = linha.rstrip("\r\n")

        if linha.strip():
            linha_modelo = linha
            break


    if linha_modelo is None:

        raise ValueError(
            "Não foi encontrada nenhuma "
            "linha de dados válida."
        )


    #tira o ; final
    linha_modelo = linha_modelo.rstrip(";")

    posicoes = [i for i, caractere in enumerate(linha_modelo) if caractere == ";"]

    
    print("\nÍndices encontrados:")
    print(posicoes)


    if len(posicoes) != 7:

        raise ValueError(
            f"Quantidade inesperada de "
            f"separadores: {len(posicoes)}. "
            f"Esperado: 7."
        )


    
    larguras = []

    inicio = 0


    for posicao in posicoes:

        largura = (posicao - inicio)
        larguras.append(largura)
        inicio = posicao + 1


    

    larguras.append(len(linha_modelo) - inicio)


    print()
    print("Larguras dos campos:")
    print(larguras)


 
    def corrigir_linha(linha):

        linha = linha.rstrip("\r\n")
        campos = []
        indice = 0


        for largura in larguras:

            campo = ""


            while (len(campo) < largura and indice < len(linha)):

                caractere = linha[indice]
                indice += 1
                # ; dentro do campo é removido
                if caractere == ";":
                    continue

                campo += caractere

            campos.append(campo)


            # pular  ; separadores

            while (indice < len(linha) and linha[indice] == ";"):
                indice += 1


        return campos



    linhas_processadas = []

    quantidade_linhas = 0


    for linha in linhas:

        if not linha.strip():
            continue

        campos = corrigir_linha(linha)


        # limpar caracteres estranhos

        campos = [limpar_texto(campo) for campo in campos]

        campos[-1] = converter_valor(campos[-1])
        

        linha_final = ";".join(campos)

        linhas_processadas.append(linha_final)

        quantidade_linhas += 1



    with open(arquivo_saida, "w", encoding="cp1252", newline="") as arquivo:

        
        arquivo.write("\n".join(linhas_processadas))


    #resultado
    
    print("\nCARREIRA concluído!")
    print(f"Original: {arquivo_original}")
    print(f"Tratado:  {arquivo_saida}")
    print(f"Linhas processadas: " f"{quantidade_linhas}")  
    print("\nÍndices utilizados:")
    print(posicoes)
    print("\nLarguras utilizadas:")
    print(larguras)


def limpar_aposen():

    
    print("APOSENTADOS")
    arquivo_nome = ("APOSENTADOS_072026.csv")

    url = (
        "https://repositorio.dados.gov.br/"
        "segrt/Aposentados/2026/"
        + arquivo_nome
    )

    arquivo_original = Path(arquivo_nome)
    arquivo_saida = Path("APOSENTADOS_072026_limpo_com_cabecalho.csv")




    baixar_arquivo(url, arquivo_original)


    




    print("Limpando...")


    with open(arquivo_original,  "r", encoding="cp1252") as arquivo:
        linhas = arquivo.readlines()




    linhas_limpas = []


    for linha in linhas:

        linha = limpar_texto(linha)
        linha = linha.rstrip("\r\n")

        if not linha:
            continue


        # separar campos
        campos = linha.split(";")

        if len(campos) >= 18:
            campos[-1] = converter_valor(campos[-1])
            campos[1] =  limpar_texto(campos[1])
            campos[14] = converter_data(campos[14])
            campos[16] = converter_data(campos[16])
            campos[-1] = converter_valor(campos[-1])
        linha = ";".join(campos)
        linhas_limpas.append(linha)




    with open(arquivo_saida, "w", encoding="cp1252", newline="") as arquivo:
        arquivo.write("\n".join(linhas_limpas))


    
    # rresultado
    
    print("\nAPOSENTADOS concluído!")
    print(f"Original: {arquivo_original}")
    print(f"Tratado:  {arquivo_saida}")
    print(f"Linhas processadas: " f"{len(linhas_limpas)}")


    # TESTE
    with open(arquivo_saida, "r", encoding="cp1252") as f:
        linhas = f.readlines()

    print("Quantidade de linhas:", len(linhas))

    for i, linha in enumerate(linhas[:10], start=1):
        print(f"\nLINHA {i}")
        print("Quantidade de ;:", linha.count(";"))
        print("Quantidade de campos:", len(linha.rstrip("\n").split(";")))
        print(repr(linha))



# roda funções


limpar_carreira()

limpar_aposen()


print()
print("#" * 60)
print("TERMINOU")
print("#" * 60)