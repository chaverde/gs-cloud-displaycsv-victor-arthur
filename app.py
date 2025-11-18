import pandas as pd
from flask import Flask, render_template, abort
 
app = Flask(__name__)
 
# Nome do arquivo CSV no diretório /wwwroot
CSV_FILE = "startup_data.csv"
 
def carregar_csv():
    """
    Lê o CSV de forma segura, tratando:
    - encoding UTF-8 e fallback para Latin-1
    - separador automático (vírgula ou ponto e vírgula)
    """
 
    # Tenta UTF-8 primeiro
    try:
        df = pd.read_csv(CSV_FILE, sep=None, engine="python", encoding="utf-8")
        return df
 
    # Se não funcionar, tenta Latin-1
    except Exception:
        try:
            df = pd.read_csv(CSV_FILE, sep=None, engine="python", encoding="latin-1")
            return df
        except Exception as e:
            print("Erro ao carregar CSV:", e)
            abort(500)
 
@app.route("/")
def index():
 
    df = carregar_csv()
 
    # Lista de colunas que queremos exibir
    colunas_interesse = [
        "name",
        "city",
        "state_code",
        "category_code",
        "funding_total_usd",
        "funding_rounds",
        "status"
    ]
 
    # Mantém apenas as colunas que existem no CSV
    colunas_existentes = [col for col in colunas_interesse if col in df.columns]
 
    if not colunas_existentes:
        return "<h2>Erro: Nenhuma das colunas esperadas existe no CSV.</h2>"
 
    df = df[colunas_existentes]
 
    # converter para lista de dicionários
    dados = df.to_dict(orient="records")
    colunas = colunas_existentes
 
    return render_template("index.html", colunas=colunas, dados=dados)
 
if __name__ == "__main__":
    app.run(debug=True)
