from flask import Flask, request, jsonify
from flask_cors import CORS
from lexico import get_all_tokens
from sintactico import parse_for_loop

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json['code']
    
    # Análisis léxico
    tokens = get_all_tokens(code)
    token_list = [{"token": t[0], "lexeme": str(t[1]), "line": t[2]} for t in tokens]
    
    # Análisis sintáctico
    parse_for_loop(code)
    from sintactico import errors as syntax_errors
    
    return jsonify({
        "tokens": token_list,
        "errors": syntax_errors
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')