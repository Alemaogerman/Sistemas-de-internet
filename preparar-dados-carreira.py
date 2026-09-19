import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


#configs

url_pasta = "https://repositorio.dados.gov.br/segrt/Cargos%20e%20Carreiras/2026/"

nome_arquivo = "CARREIRA_072026.txt"

arquivo_original = "CARREIRA_072026.txt"
arquivo_saida = "CARREIRA_072026_limpo.csv"



print("Acessando a pasta...")

resposta = requests.get(url_pasta)
resposta.raise_for_status()

soup = BeautifulSoup(resposta.text, "html.parser")

url_arquivo = None

for link in soup.find_all("a", href=True):

    href = link["href"]

    if nome_arquivo.lower() in href.lower():

        url_arquivo = urljoin(
            url_pasta,
            href
        )

        break


if url_arquivo is None:

    raise ValueError(f"Não foi encontrado o arquivo "  f"{nome_arquivo} na página.")


print("Arquivo encontrado:")
print(url_arquivo)


# baixar arq

print()
print("Baixando arquivo...")

resposta = requests.get(url_arquivo)
resposta.raise_for_status()

with open(arquivo_original, "wb") as arquivo:
    arquivo.write(resposta.content)

print("Download concluído.")



# ler arq


with open(arquivo_original, "r", encoding="cp1252") as arquivo:
    linhas = arquivo.readlines()


print(f"Linhas encontradas no arquivo: {len(linhas)}")



linhas = linhas[2:]



# cabeçalho


cabecalho = (
    "Nome;"
    "CPF;"
    "Código da carreira;"
    "Descrição do cargo emprego;"
    "UF da UPAG de vinculação;"
    "Denominação do órgão de atuação;"
    "Mês de referência;"
    "Valor da remuneração"
)




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



# remover a coluna final ; 


linha_modelo = linha_modelo.rstrip(";")


#encontrar índices

posicoes = [i  for i, caractere in enumerate(linha_modelo)  if caractere == ";"]


print()
print("Índices encontrados:")
print(posicoes)



if len(posicoes) != 7:

    raise ValueError(
        f"Quantidade inesperada de separadores: "
        f"{len(posicoes)}. "
        f"Esperado: 7."
    )



larguras = []

inicio = 0

for posicao in posicoes:
    largura = posicao - inicio
    larguras.append(largura)
    inicio = posicao + 1




larguras.append(len(linha_modelo) - inicio)


print()
print("Larguras dos campos:")
print(larguras)


#corrigir uma linha

def corrigir_linha(linha):

    linha = linha.rstrip("\r\n")
    campos = []
    indice = 0

    for largura in larguras:

        campo = ""
        while (len(campo) < largura  and indice < len(linha)):
            caractere = linha[indice]
            indice += 1

            # ; dentro do campo é apagado

            if caractere == ";":
                continue

            campo += caractere

        campos.append(campo)
  
        while (indice < len(linha) and linha[indice] == ";"):
            indice += 1

    return campos


#expressão regular


def limpar_texto(texto):

    texto = re.sub(r"[^A-Za-z0-9\s;,.\-]", "", texto)
    return texto.strip()




linhas_processadas = []

quantidade_linhas = 0


for linha in linhas:
    if not linha.strip():
        continue

    campos = corrigir_linha(linha)   
    campos = [limpar_texto(campo)  for campo in campos]


    #converter pro dbeaver

    campos[-1] = (campos[-1].replace(".", "").replace(",", "."))


    

    linha_final = ";".join(campos)

    linhas_processadas.append(linha_final)

    quantidade_linhas += 1

# arq final
with open(arquivo_saida, "w", encoding="cp1252", newline="") as arquivo:
    arquivo.write(cabecalho + "\n")


    

    for linha in linhas_processadas:
        arquivo.write(linha + "\n")




print()
print("=" * 60)
print("PROCESSAMENTO CONCLUÍDO")
print("=" * 60)

print(f"Arquivo original : {arquivo_original}")

print(f"Arquivo final    : {arquivo_saida}")

print(f"Linhas processadas: {quantidade_linhas}")


print("\nÍndices utilizados:")

print(posicoes)


print("\nLarguras utilizadas:")

print(larguras)


print("\nArquivo pronto para importar no Power BI.")