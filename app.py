from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    data = pd.read_csv("data/dataset.csv")
    data = data[['tahun', 'jumlah_pengguna_internet']]
    return render_template('index.html', data=data.to_dict())

@app.route('/predictions', methods=['POST'])
def predictions():
    data = pd.DataFrame({
        'tahun': request.form.getlist('tahun[]'),
        'jumlah_pengguna_internet': request.form.getlist('jumlah_pengguna_internet[]')
    })
    return data.to_html()

if __name__ == '__main__':
    app.run(debug=True)
