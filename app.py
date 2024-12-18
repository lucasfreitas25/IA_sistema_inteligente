import base64
import io
import sqlite3
from flask import Flask, render_template, request
from matplotlib import pyplot as plt
import pandas as pd
from tensorflow.keras.models import load_model
from datetime import datetime
import numpy as np
import holidays
from sklearn.preprocessing import MinMaxScaler


feriados_brasil = holidays.Brazil()
app = Flask(__name__)


def determinar_estacao(data):
    if data.month == 12 and data.day >= 21 or data.month <= 2 or data.month == 3 and data.day < 21:
        return 0
    elif data.month == 3 and data.day >= 21 or data.month <= 5 or data.month == 6 and data.day < 21:
        return 1
    elif data.month == 6 and data.day >= 21 or data.month <= 8 or data.month == 9 and data.day < 23:
        return 2
    else:
        return 3
    
def fim_do_mes(data):

    return data.is_month_end.astype(int)
          
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
model = load_model("model\\modelo_sist_inteligente_att.h5")
total_vendido = np.array([100, 200, 300, 400, 500, 600])  

scaler_y = MinMaxScaler()
scaler_y.fit(total_vendido.reshape(-1, 1))
historical_predictions = []
dias = []

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None 
    global historical_predictions
    global dias
    start_date = ""
    end_date = ""
    plot_url = ""
    if request.method == "POST":
        
        #PASSANDO A ENTRADA DOS DADOS 
        start_date = request.form.get("start-date")
        end_date = request.form.get("end-date")
        prod_gratis = int(request.form.get("prod_gratis"))  
        combos = int(request.form.get("combo"))  
        lancamento_prod = 1 if request.form.get("Lancamento_prod") else 0  
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        date_range = pd.date_range(start=start_date_obj, end=end_date_obj)
        feriados = [d in feriados_brasil for d in date_range]
        Dia_da_Semana = date_range.weekday
        Dia_util = np.where(Dia_da_Semana.isin([5, 6]), 0, 1)
        estacao = [determinar_estacao(d) for d in date_range]
        

        sales_data = pd.DataFrame({
            "date": date_range,
            "fim_do_mes": fim_do_mes(date_range),
            "prod_gratis": prod_gratis,
            "Lancamento_prod": lancamento_prod,
            "Combo_promo": combos,  
            "feriado": feriados,
            "Dia_da_Semana": Dia_da_Semana,
            "Dia_util": Dia_util,
            "estacao": estacao,
            "dias": (date_range - date_range.min()).days  
        })
        
        # print(sales_data)  
        
        scaler_X = MinMaxScaler()
        features = sales_data[['fim_do_mes', 'prod_gratis', 'Lancamento_prod', 'Combo_promo', 'feriado', 'Dia_da_Semana', 'Dia_util', 'estacao', 'dias']]
        features_scaled = scaler_X.fit_transform(features)


        time_steps = 7  
        input_data = features_scaled[-time_steps:].reshape(1, time_steps, features.shape[1])  # (1, 1, n_features)

        # PREVISÃO UTILIZANDO O MODELO
        predicted_sales = model.predict(input_data)
        predicted_sales = scaler_y.inverse_transform(predicted_sales)  
        prediction = int(predicted_sales.flatten()[0])
        
        
    
        start_day = f'{start_date_obj.day}/{start_date_obj.month}'
        end_day = f'{end_date_obj.day}/{end_date_obj.month}'

        semana_prev = f"{start_day} - {end_day}"
        dias.append(semana_prev)
        historical_predictions.append(prediction)
        plt.figure(figsize=(10, 6))
        plt.plot(dias, historical_predictions, marker='o', color='b', label='Previsão de Vendas')
        plt.xlabel("Semana prevista")
        plt.ylabel("Vendas")
        plt.title("Histórico de Previsões de Vendas")
        plt.legend()


        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        

    return render_template("index.html", prediction=prediction, data_inicio = start_date, data_final = end_date, plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
