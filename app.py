from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Diccionario de antónimos
antonimos = {
    "fácil": "difícil",
    "morir": "vivir",
    "rápido": "lento",
    "feliz": "triste",
    "triste": "feliz",
    "enojado": "calmado",
    "amable": "grosero",
    "valiente": "cobarde",
    "hermoso": "feo",
    "feo": "hermoso",
    "grande": "pequeño",
    "pequeño": "grande",
    "alto": "bajo",
    "bajo": "alto",
    "gordo": "delgado",
    "delgado": "gordo",
    "inteligente": "tonto",
    "tonto": "inteligente",
    "difícil": "fácil",
    "fuerte": "débil",
    "débil": "fuerte",
    "brillante": "oscuro",
    "oscuro": "brillante",
    "caliente": "frío",
    "frío": "caliente",
    "mojado": "seco",
    "seco": "mojado",
    "viejo": "joven",
    "joven": "viejo",
    "nuevo": "viejo",
    "cansado": "descansado",
    "descansado": "cansado",
    "sabio": "ignorante",
    "ignorante": "sabio",
    "paciente": "impaciente",
    "impaciente": "paciente",
    "rico": "pobre",
    "pobre": "rico",
    "libre": "ocupado",
    "ocupado": "libre",
    "limpio": "sucio",
    "sucio": "limpio",
    "ordenado": "desordenado",
    "desordenado": "ordenado",
    "humilde": "arrogante",
    "arrogante": "humilde",
    "claro": "oscuro",
    "alegre": "triste",
    "serio": "alegre",
    "generoso": "tacaño",
    "tacaño": "generoso",
    "amistoso": "hostil",
    "hostil": "amistoso",
    "tranquilo": "nervioso",
    "nervioso": "tranquilo",
    "silencioso": "ruidoso",
    "ruidoso": "silencioso",
    "sano": "enfermo",
    "enfermo": "sano",
    "nuevo": "viejo",
    "usado": "nuevo",
    "decidido": "dudoso",
    "dudoso": "decidido",
    "leal": "traidor",
    "traidor": "leal",
    "realista": "idealista",
    "idealista": "realista",
    "práctico": "teórico",
    "teórico": "práctico"
}

# Diccionario de operadores
operadores = {
    '+': 'operador suma',
    '-': 'operador resta',
    '*': 'operador multiplicación',
    '/': 'operador división',
    '(': 'paréntesis apertura',
    ')': 'paréntesis cierre',
    ',': 'coma',
    '.': 'punto'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data['text']
    lines = text.split('\n')
    results = []

    for line in lines:
        words = line.split()
        output_line = []
        changed_words = []
        has_number = False
        has_symbol = False

        for word in words:
            word_lower = word.lower()
            if word_lower in antonimos:
                output_line.append(antonimos[word_lower])
                changed_words.append('x')
            elif word in operadores:
                output_line.append(operadores[word])
                changed_words.append('')
                has_symbol = True
            elif re.match(r'^\d+$', word):
                output_line.append('número')
                changed_words.append('')
                has_number = True
            else:
                output_line.append(word)
                changed_words.append('')
                if re.search(r'\d', word):
                    has_number = True
                if re.search(r'[^\w\s]', word):
                    has_symbol = True

        results.append({
            'input': line,
            'output': ' '.join(output_line),
            'changed': ' '.join(changed_words).strip(),
            'number': 'x' if has_number else '',
            'symbol': 'x' if has_symbol else '',
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
