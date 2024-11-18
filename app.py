from flask import Flask, render_template, request, jsonify
import xmltodict
import json
import os

app = Flask(__name__)

def converter_xml_para_json(arquivo_xml, caminho_json):
    try:
        with open(arquivo_xml, 'r', encoding='utf-8') as xml_file:
            dados_xml = xml_file.read()
            if not dados_xml.strip():
                raise ValueError("O arquivo XML está vazio")
            dados_json = xmltodict.parse(dados_xml)
            
            if not os.path.exists('arquivos_convertidos'):
                os.makedirs('arquivos_convertidos')
            
            with open(caminho_json, 'w', encoding='utf-8') as json_file:
                json.dump(dados_json, json_file, indent=4, ensure_ascii=False)

            return dados_json
    except Exception as e:
        raise ValueError(f"Erro ao converter XML: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi anexado"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo foi selecionado"}), 400

    caminho_arquivo_xml = os.path.join(os.getcwd(), file.filename)
    file.save(caminho_arquivo_xml)

    nome_arquivo_json = os.path.splitext(file.filename)[0] + '.json'
    caminho_arquivo_json = os.path.join('arquivos_convertidos', nome_arquivo_json)

    try:
        dados_json = converter_xml_para_json(caminho_arquivo_xml, caminho_arquivo_json)
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
    finally:
        if os.path.exists(caminho_arquivo_xml):
            os.remove(caminho_arquivo_xml)

    return jsonify({"json": dados_json, "arquivo_json": caminho_arquivo_json}), 200

if __name__ == '__main__':
    app.run(debug=True)
