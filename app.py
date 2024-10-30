import sqlite3
from flask import Flask, render_template, request
import pandas as pd
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)


def create_table():
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale (
            id_venda INTEGER PRIMARY KEY,
            data_prev TEXT NOT NULL,
            venda_prev INTEGER NOT NULL
        )
    ''')
    
    conn.commit()  
    conn.close()  


create_table()
model = load_model("model\\modelo_sist_inteligente.h5")


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None 

    if request.method == "POST":
        
        start_date = request.form.get("start-date")
        end_date = request.form.get("end-date")

       
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        
        
        # date_range = pd.date_range(start=start_date_obj, end=end_date_obj)
        # sales_data = pd.DataFrame(date_range, columns=["date"])
        
        # # Se o modelo espera múltiplas características, você deve adicionar as colunas necessárias
        # # Aqui estamos apenas usando 'date' como exemplo
        # # Adicione aqui as colunas adicionais que seu modelo precisa

        
        # sales_data["date"] = (sales_data["date"].astype(np.int64) // 10**9).values  
        # input_data = sales_data.values[-8:].reshape(1, 8, 1)  

        # #PREVISÃO UTILIZANDO O MODELO
        # predicted_sales = model.predict(input_data)

        # # Converta as previsões em lista para renderizar na template
        # prediction = predicted_sales.flatten().tolist()
        prediction  = 40

    #RETORNA COM PREVISAO NO HTML
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
