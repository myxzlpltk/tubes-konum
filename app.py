from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

ORDE_POLINOMIAL = 3

@app.route('/', methods=['GET'])
def index():
    data = pd.read_csv("data/dataset.csv")
    data = data[['tahun', 'jumlah_pengguna_internet']]
    return render_template('index.html', data=data.to_dict())

@app.route('/predictions', methods=['POST'])
def predictions():
    tahun_prediksi_awal = int(request.form.get('min_year'))
    tahun_prediksi_akhir = int(request.form.get('max_year'))
    range_predictions = [x for x in range(tahun_prediksi_awal, tahun_prediksi_akhir+1)]

    data = pd.DataFrame({
        'tahun': request.form.getlist('tahun[]'),
        'jumlah_pengguna_internet': request.form.getlist('jumlah_pengguna_internet[]')
    }).astype({
    'tahun': 'int64',
    'jumlah_pengguna_internet': 'int64',
    })
    print(data['tahun'])
    polynoms = np.polyfit(data['tahun'], data['jumlah_pengguna_internet'], ORDE_POLINOMIAL)
    model = np.poly1d(polynoms)
    predictions = model(range_predictions)
    df_pred = pd.DataFrame({
        'tahun': range_predictions,
        'jumlah_pengguna_internet': [round(x) for x in predictions]
    })
    print(df_pred)
    data = data.append(df_pred, ignore_index=True)

    return data.to_html()

if __name__ == '__main__':
    app.run(debug=True)
