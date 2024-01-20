from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/birthday', methods=['POST'])
def calculate_age():
    # Obtener los datos del JSON enviado en el request
    data = request.get_json()
    name = data['name']
    birth_date_str = data['date']
    
    # Convertir la fecha de nacimiento a objeto datetime
    birth_date = datetime.strptime(birth_date_str, '%d-%m-%Y')
    
    # Calcular la edad
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # Comprobar si la fecha es futura
    if birth_date > today:
        return jsonify({'error': 'The date provided is in the future'}), 400
    
    # Devolver la respuesta
    return jsonify({'data': f'{name} is {age} years old'})

# Iniciar la aplicación en modo debug para desarrollo
if __name__ == '__main__':
    app.run(debug=True)
