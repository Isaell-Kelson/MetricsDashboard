from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(filepath)

        
        df = pd.read_excel(filepath)
        
        quantidade_de_cobrancas = int(df.iloc[:, 0].sum())  
        media_de_cobranca_a_cada_dias = float(df.iloc[:, 1].mean())  
        
        status_count = df['status'].value_counts()
        
        df['data início'] = pd.to_datetime(df['data início'], errors='coerce')
        data_inicio_min = df['data início'].min()
        data_inicio_max = df['data início'].max()
        
        df['data cancelamento'] = pd.to_datetime(df['data cancelamento'], errors='coerce')
        data_cancelamento_min = df['data cancelamento'].min()
        data_cancelamento_max = df['data cancelamento'].max()
        
        intervalo_tempo_total = data_cancelamento_max - data_cancelamento_min
        
        dados_para_json = {
            "quantidade_de_cobrancas": quantidade_de_cobrancas,
            "media_de_cobranca_a_cada_dias": media_de_cobranca_a_cada_dias,
            "status_count": status_count.to_dict(),
            "data_inicio_min": str(data_inicio_min),
            "data_inicio_max": str(data_inicio_max),
            "data_cancelamento_min": str(data_cancelamento_min),
            "data_cancelamento_max": str(data_cancelamento_max),
            "intervalo_tempo_total": str(intervalo_tempo_total)
        }
        
        os.remove(filepath)

        return jsonify(dados_para_json), 200

    else:
        return jsonify({'error': 'Tipo de arquivo não permitido. Envie um arquivo .xlsx ou .csv.'}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
