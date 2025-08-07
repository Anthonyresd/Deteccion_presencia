from flask import Flask, jsonify
import requests

app = Flask(__name__)

# URL base de Firebase Realtime Database (lecturas)
FIREBASE_URL = "https://sensor-presencia-default-rtdb.firebaseio.com/lecturas.json"

@app.route('/datos')
def obtener_datos():
    try:
        res = requests.get(FIREBASE_URL)
        res.raise_for_status()
        data = res.json()
        
        if not data:
            return jsonify({"error": "No hay datos en Firebase"}), 404
        
        # Filtrar claves que son timestamps numéricos
        timestamps = [k for k in data.keys() if k.isdigit()]
        timestamps.sort()
        if not timestamps:
            return jsonify({"error": "No hay lecturas válidas"}), 404
        
        last_key = timestamps[-1]
        last_reading = data[last_key]

        return jsonify(last_reading)

    except requests.RequestException as e:
        return jsonify({"error": f"Error consultando Firebase: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
