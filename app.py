import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    df = pd.read_csv("startup_data.csv")

    colunas_interesse = [
        "name",
        "city",
        "state_code",
        "category_code",
        "funding_total_usd",
        "funding_rounds",
        "status"
    ]

    df = df[colunas_interesse]

    dados = df.to_dict(orient="records")
    colunas = df.columns.tolist()

    return render_template("index.html", colunas=colunas, dados=dados)

if __name__ == "__main__":
    app.run()
