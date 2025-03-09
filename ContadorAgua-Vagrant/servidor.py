from flask import Flask, request, jsonify
import psycopg2

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
DB_HOST = "localhost"  # PostgreSQL está en la misma máquina
DB_NAME = "agua"
DB_USER = "postgres"
DB_PASSWORD = "vagrant"

# Función para conectar a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Crear la tabla si no existe
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS consumo_agua (
            id SERIAL PRIMARY KEY,
            hora_consumo TEXT,
            consumo REAL,
            tipo_contador TEXT,
            num_serie TEXT,
            titular TEXT,
            localidad TEXT,
            municipio TEXT,
            codigo_postal TEXT,
            direccion TEXT    
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Llamamos a la función para asegurarnos de que la tabla existe antes de recibir datos
create_table()

# Ruta principal de prueba
@app.route('/')
def home():
    return "Servidor Flask funcionando correctamente", 200

# Ruta para obtener un consumo de agua específico de un usuario
@app.route('/consumo/<int:id>', methods=['GET'])
def obtener_consumo(id):
    try:
        # Conectar a PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener el consumo de agua con el ID especificado
        cur.execute("SELECT * FROM consumo_agua WHERE id = %s", (id,))
        consumo = cur.fetchone()

        cur.close()
        conn.close()

        # Verificar si se encontró el consumo
        if consumo is None:
            return jsonify({"error": "Consumo no encontrado"}), 404

        # Convertir el resultado a un formato JSON
        consumo_json = {
            "id": consumo[0],
            "HoraConsumo": consumo[1],
            "Consumo": consumo[2],
            "TipoContador": consumo[3],
            "NumSerie": consumo[4],
            "Titular": consumo[5],
            "Localidad": consumo[6],
            "Municipio": consumo[7],
            "CodigoPostal": consumo[8],
            "Direccion": consumo[9]
        }

        return jsonify(consumo_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para obtener todos los consumos de agua
@app.route('/cosumoGlobal', methods=['GET'])
def obtener_consumos():
    try:
        # Conectar a PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()

        # Obtener los consumos de agua
        cur.execute("SELECT * FROM consumo_agua")
        consumos = cur.fetchall()

        cur.close()
        conn.close()

        # Convertir los resultados a un formato JSON
        consumos_json = []
        for consumo in consumos:
            consumo_json = {
                "id": consumo[0],
                "HoraConsumo": consumo[1],
                "Consumo": consumo[2],
                "TipoContador": consumo[3],
                "NumSerie": consumo[4],
                "Titular": consumo[5],
                "Localidad": consumo[6],
                "Municipio": consumo[7],
                "CodigoPostal": consumo[8],
                "Direccion": consumo[9]
            }
            consumos_json.append(consumo_json)

        return jsonify(consumos_json), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para recibir el consumo de agua
@app.route('/consumo', methods=['POST'])
def registrar_consumo():
    data = request.json  # Obtener los datos en formato JSON

    # Verificar que los datos estén completos
    required_fields = ["HoraConsumo", "Consumo", "TipoContador", "NumSerie", "Titular", "Localidad", "Municipio",
                       "CodigoPostal", "Direccion"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo requerido: {field}"}), 400

    try:
        # Conectar a PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar los datos en la base de datos
        cur.execute("""
            INSERT INTO consumo_agua (hora_consumo, consumo, tipo_contador, num_serie, titular, localidad, municipio,
                                      codigo_postal, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["HoraConsumo"],
            data["Consumo"],
            data["TipoContador"],
            data["NumSerie"],
            data["Titular"],
            data["Localidad"],
            data["Municipio"],
            data["CodigoPostal"],
            data["Direccion"]
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Consumo registrado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
