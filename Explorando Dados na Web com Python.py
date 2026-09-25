import io
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning


# ============================================================
# NÍVEL 1 — URLs, parâmetros e cabeçalhos
# ============================================================

print("\n===== NÍVEL 1 =====")

url_posts = "https://jsonplaceholder.typicode.com/posts"

headers = {
    "User-Agent": "Atividade-Pratica-Web-Python"
}

params = {
    "userId": 2,
    "_limit": 5
}

resposta_posts = requests.get(
    url_posts,
    params=params,
    headers=headers,
    timeout=10
)

print("Status HTTP:", resposta_posts.status_code)
print("URL final:", resposta_posts.url)

posts = resposta_posts.json()

for post in posts:
    print(post["id"], "-", post["title"])


# ============================================================
# NÍVEL 2 — JSON, erros e arquivos binários
# ============================================================

print("\n===== NÍVEL 2 =====")

# Exercício 2.1 — Consulta de CEPs
ceps = [
    "01001000",
    "20040002",
    "24220000"
]

resultados_ceps = []

for cep in ceps:
    url_cep = f"https://viacep.com.br/ws/{cep}/json/"

    resposta_cep = requests.get(
        url_cep,
        headers=headers,
        timeout=10
    )

    dados_cep = resposta_cep.json()

    if "erro" not in dados_cep:
        resultados_ceps.append(dados_cep)
    else:
        print(f"CEP não encontrado: {cep}")

df_ceps = pd.DataFrame(resultados_ceps)

print("\nDataFrame dos CEPs:")
print(df_ceps)


# Exercício 2.2 — Função segura de download
def baixar_arquivo(url, nome_arquivo):
    try:
        resposta = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        resposta.raise_for_status()

        with open(nome_arquivo, "wb") as arquivo:
            arquivo.write(resposta.content)

        print(f"Download concluído: {nome_arquivo}")

    except requests.exceptions.RequestException as erro:
        print(f"Não foi possível fazer o download: {erro}")


# Exercício 2.3 — Download de imagem
url_imagem = "https://picsum.photos/400/400"

baixar_arquivo(
    url_imagem,
    "imagem_aleatoria.jpg"
)


# ============================================================
# NÍVEL 3 — Webscraping e ética
# ============================================================

print("\n===== NÍVEL 3 =====")

# Exercício 3.1 — Consulta ao robots.txt
url_robots = "https://books.toscrape.com/robots.txt"

resposta_robots = requests.get(
    url_robots,
    headers=headers,
    timeout=10
)

print("\nRobots.txt:")
print(resposta_robots.text)


# Exercício 3.2 — Extração dos 5 primeiros livros
url_livros = "https://books.toscrape.com/"

resposta_livros = requests.get(
    url_livros,
    headers=headers,
    timeout=10
)

resposta_livros.raise_for_status()

soup = BeautifulSoup(
    resposta_livros.text,
    "html.parser"
)

livros = soup.select("article.product_pod")[:5]

dados_livros = []

for livro in livros:
    titulo = livro.h3.a["title"]
    preco = livro.select_one(".price_color").get_text(strip=True)

    dados_livros.append({
        "titulo": titulo,
        "preco": preco
    })

    print(f"{titulo} — {preco}")


# Exercício 3.3 — Salvar livros em CSV
df_livros = pd.DataFrame(dados_livros)

df_livros.to_csv(
    "livros.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo livros.csv salvo com sucesso.")


# Exercício 3.4 — Tabela da Wikipedia
# Usamos uma página em inglês e um User-Agent.
# O verify=False evita erro de certificado em algumas redes.
url_wikipedia = (
    "https://en.wikipedia.org/wiki/"
    "List_of_countries_and_dependencies_by_population"
)

warnings.simplefilter("ignore", InsecureRequestWarning)

try:
    resposta_wikipedia = requests.get(
        url_wikipedia,
        headers=headers,
        timeout=10,
        verify=False
    )

    resposta_wikipedia.raise_for_status()

    tabelas = pd.read_html(
        io.StringIO(resposta_wikipedia.text)
    )

    df_populacao = tabelas[0]

    print("\nTabela da Wikipedia:")
    print(df_populacao.head())

    df_populacao.to_csv(
        "populacao_paises.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nArquivo populacao_paises.csv salvo com sucesso.")

except requests.exceptions.RequestException as erro:
    print(f"Não foi possível acessar a Wikipedia: {erro}")

except ValueError as erro:
    print(f"Não foi possível ler a tabela: {erro}")