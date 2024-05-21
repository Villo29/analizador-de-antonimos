from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Diccionario de sinónimos
sinonimos = {
    "fácil": "sencillo",
    "morir": "fallecer",
    "rápido": "veloz",
    "feliz": "contento",
    "triste": "deprimido",
    "enojado": "iracundo",
    "amable": "cordial",
    "valiente": "intrépido",
    "hermoso": "bello",
    "feo": "horrible",
    "grande": "enorme",
    "pequeño": "diminuto",
    "alto": "elevado",
    "bajo": "reducido",
    "gordo": "obeso",
    "delgado": "esbelto",
    "inteligente": "listo",
    "tonto": "necio",
    "difícil": "complicado",
    "fuerte": "robusto",
    "débil": "fragil",
    "rápido": "expedito",
    "lento": "pausado",
    "brillante": "luminoso",
    "oscuro": "tenebroso",
    "caliente": "ardiente",
    "frío": "helado",
    "cálido": "templado",
    "helado": "gélido",
    "mojado": "húmedo",
    "seco": "árido",
    "viejo": "antiguo",
    "joven": "juvenil",
    "nuevo": "moderno",
    "antiguo": "veterano",
    "cansado": "agotado",
    "descansado": "repuesto",
    "rápido": "presto",
    "despacio": "lento",
    "diligente": "laborioso",
    "perezoso": "haragán",
    "rico": "opulento",
    "pobre": "necesitado",
    "sabio": "erudito",
    "ignorante": "iletrado",
    "paciente": "sosegado",
    "impaciente": "ansioso",
    "fresco": "refrescante",
    "caluroso": "sofocante",
    "feliz": "dichoso",
    "afligido": "atribulado",
    "tranquilo": "sereno",
    "alterado": "perturbado",
    "nervioso": "ansioso",
    "calmado": "apacible",
    "libre": "desocupado",
    "ocupado": "atareado",
    "limpio": "aseado",
    "sucio": "mugriento",
    "ordenado": "organizado",
    "desordenado": "caótico",
    "humilde": "modesto",
    "arrogante": "presuntuoso",
    "sabroso": "delicioso",
    "desagradable": "repugnante",
    "claro": "evidente",
    "oscuro": "sombrío",
    "resplandeciente": "radiante",
    "apagado": "opaco",
    "alegre": "contento",
    "serio": "grave",
    "generoso": "dadivoso",
    "tacaño": "avariento",
    "amistoso": "afable",
    "hostil": "antipático",
    "tranquilo": "plácido",
    "inquieto": "agitado",
    "silencioso": "callado",
    "ruidoso": "estruendoso",
    "sano": "saludable",
    "enfermo": "achacoso",
    "nuevo": "inédito",
    "usado": "gastado",
    "viejo": "anciano",
    "antiguo": "venerable",
    "alegre": "júbilo",
    "triste": "melancólico",
    "valiente": "osado",
    "cobarde": "pusilánime",
    "decidido": "resuelto",
    "dudoso": "vacilante",
    "leal": "fiel",
    "traidor": "desleal",
    "realista": "pragmático",
    "idealista": "utópico",
    "práctico": "funcional",
    "teórico": "hipotético"
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
            if word_lower in sinonimos:
                output_line.append(sinonimos[word_lower])
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
