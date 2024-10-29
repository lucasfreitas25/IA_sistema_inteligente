import sqlite3
from flask import Flask, render_template
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
app = Flask(__name__)


# def create_table():
#     conn = sqlite3.connect('sales_data.db')
#     cursor = conn.cursor()

#     # Criação da tabela 'sale' se não existir
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS sale (
#             id_venda INTEGER PRIMARY KEY,
#             data_prev TEXT NOT NULL,
#             venda_prev INTEGER NOT NULL
#         )
#     ''')
    
#     conn.commit()  
#     conn.close()  


# create_table()

# # Carregue o modelo de IA
# model = load_model("C:\\Users\\Lucas Freitas\\Documents\\Faculdade\\Optativas\\Sistemas Inteligentes\\Trabalho_final\\model\\modelo_sist_inteligente.h5")

# # Rota principal para exibir a previsão da semana
# @app.route("/", methods=["GET", "POST"])
# def index():
#     # Conecte-se ao banco de dados e recupere dados usando o cursor
#     conn = sqlite3.connect('sales_data.db')
#     cursor = conn.cursor()
    
#     # Recupere os dados de vendas
#     cursor.execute("SELECT data_prev, venda_prev FROM sale")
#     sales_data = cursor.fetchall()  # Lista de tuplas com os resultados
#     conn.close()

#     # Converta os dados para um DataFrame para usar com o modelo de IA
#     data = pd.DataFrame(sales_data, columns=["date", "sales_amount"])
    
#     # Use o modelo para prever as vendas da semana
#     predicted_sales = model.predict(data)
    
#     # Renderize o resultado na página
#     return render_template("index.html", prediction=predicted_sales)
@app.route("/")
def index():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
