from flask import Flask, request, jsonify
from flask_cors import CORS
from lexico import get_all_tokens
from combined import get_analyzer

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json['code']
    language = request.json['language']  # Nuevo parámetro para el lenguaje
    
    # Análisis léxico
    tokens = get_all_tokens(code)
    token_list = [
        {
            "token": t[0],
            "lexeme": str(t[1]),
            "wordReserv": t[2],
            "identifier": t[3],
            "cadena": t[4],
            "numero": t[5],
            "simbolo": t[6],
            "line": t[7]
        }
        for t in tokens
    ]

    # Análisis sintáctico
    analyzer = get_analyzer(language)
    syntax_errors = analyzer.parse(code)
    
    return jsonify({
        "tokens": token_list,
        "errors": syntax_errors
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')