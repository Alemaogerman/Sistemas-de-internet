import requests
from pathlib import Path
import re


# config


arquivo_nome = "APOSENTADOS_072026.csv"

url = (
    "https://repositorio.dados.gov.br/"
    "segrt/Aposentados/2026/"
    + arquivo_nome
)

arquivo_original = Path(arquivo_nome)
arquivo_limpo = Path("APOSENTADOS_072026_limpo_com_cabecalho.csv")



print("Baixando arquivo...")

resposta = requests.get(url, timeout=60)
resposta.raise_for_status()

arquivo_original.write_bytes(resposta.content)

print(f"Download concluído: {arquivo_original}")



# cabeçalho pq o arquivo n tem (os nomes vem do dicio de dados)


cabecalho = (
    "Nome;"
    "CPF;"
    "Matrícula do Servidor;"
    "Nome do órgão;"
    "Sigla do órgão;"
    "Código do órgão superior;"
    "Cargo;"
    "Classe;"
    "Padrão;"
    "Referência;"
    "Nível;"
    "Tipo de Aposentadoria;"
    "Fundamentação da inatividade;"
    "Nome Diploma Legal;"
    "Data publicação do Diploma Legal;"
    "Ocorrência de ingresso no serviço público;"
    "Data de ocorrência de ingresso no serviço público;"
    "Valor do Rendimento Líquido"
)




print("Limpando")

with open(arquivo_original, "r", encoding="cp1252") as f:
    linhas = f.readlines()

linhas_limpas = []

for linha in linhas:

    #expressão regular
    linha = re.sub(r'[^A-Za-z0-9\s;,.\-]', '', linha)

    linhas_limpas.append(linha.rstrip("\r\n"))



# novo arq


with open(arquivo_limpo, "w", encoding="cp1252", newline="") as f:

    f.write(cabecalho + "\n")
    f.write("\n".join(linhas_limpas))


print()
print("Processamento concluído!")
print(f"Original: {arquivo_original}")
print(f"Tratado:  {arquivo_limpo}")