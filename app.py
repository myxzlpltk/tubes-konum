from flask import Flask, render_template, request
import base64
import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'id_ID')

app = Flask(__name__)

ORDE_POLINOMIAL = 3

@app.route('/', methods=['GET'])
def index():
    data = pd.read_csv("data/dataset.csv")
    data = data[['tahun', 'jumlah_pengguna_internet']]
    return render_template('index.html', data=data.to_dict())

@app.route('/predictions', methods=['POST'])
def predictions():
    min_year = int(request.form.get('min_year'))
    max_year = int(request.form.get('max_year'))
    range_predictions = np.arange(min_year, max_year+1, 1)

    data = pd.DataFrame({
        'tahun': request.form.getlist('tahun[]'),
        'jumlah_pengguna_internet': request.form.getlist('jumlah_pengguna_internet[]')
    }).astype({'tahun': 'int64', 'jumlah_pengguna_internet': 'int64'})

    X = data['tahun']
    y = data['jumlah_pengguna_internet']

    model = np.poly1d(np.polyfit(X, y, ORDE_POLINOMIAL))

    predictions = model(range_predictions)
    result = pd.DataFrame({
        'tahun': range_predictions,
        'jumlah_pengguna_internet': [round(x) for x in predictions]
    }).astype({'tahun': 'int64', 'jumlah_pengguna_internet': 'int64'}).sort_values(by='tahun')

    # Plot
    new_X = np.concatenate([X, range_predictions])
    new_y = np.concatenate([y, predictions])
    plt.scatter(new_X, new_y, color='blue')
    line = np.linspace(X.min(), range_predictions.max(), 100)
    plt.plot(line, model(line), color='red')
    plt.title('Polynomial Regression')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Pengguna Internet')

    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

    return render_template('predictions.html', plot=s, data=result)

if __name__ == '__main__':
    app.run(debug=True)
