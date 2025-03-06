from flask import Flask, request, jsonify, send_file
import mysql.connector
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)  # Esto nos permite que el frontend pueda acceder al backend

# Creamos la función para conectar con la base de datos de mysql
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="192.168.1.105",
            user="dabir",
            password="76811927",
            database="inventario"
        )
        return conn
    except mysql.connector.Error:
        return None

# Es la ruta para poder obtener los productos con las imágenes
@app.route("/get_products", methods=["GET"])
def get_products():
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"error": "❌ No se pudo conectar a la base de datos"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, id_categoria, precio, id_marca, descripcion, cantidad FROM productos")
        productos = cursor.fetchall()

        # Generamos la URL para cada imagen del producto
        for producto in productos:
            producto["imagen_url"] = f"http://localhost:5000/get_image/{producto['id']}"

        cursor.close()
        conn.close()
        
        return jsonify(productos)
    except mysql.connector.Error as err:
        return jsonify({"error": f"❌ Error en la base de datos: {err}"}), 500
    
    
# Esto nos permite agregar un producto a la base de datos mysql
@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.form
    nombre = data.get("nombre")
    id_categoria = data.get("id_categoria")
    precio = data.get("precio")
    id_marca = data.get("id_marca")
    descripcion = data.get("descripcion", "")
    cantidad = data.get("cantidad")
    imagen = request.files.get("imagen")

    if not all([nombre, id_categoria, precio, id_marca, cantidad]):
        return jsonify({"error": "❌ Faltan datos obligatorios"}), 400

    imagen_data = imagen.read() if imagen else None

    try:
        conn = connect_db()
        if not conn:
            return jsonify({"error": "❌ Error de conexión a la base de datos"}), 500
        
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO productos (nombre, id_categoria, precio, id_marca, descripcion, cantidad, imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (nombre, id_categoria, precio, id_marca, descripcion, cantidad, imagen_data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "✅ Producto agregado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"❌ Error en la base de datos: {err}"}), 500
    
    

# Es la ruta para obtener la imagen de un producto
@app.route("/get_image/<int:product_id>")
def get_image(product_id):
    try:
        conn = connect_db()
        if not conn:
            return "❌ Error de conexión a la base de datos", 500

        cursor = conn.cursor()
        cursor.execute("SELECT imagen FROM productos WHERE id = %s", (product_id,))
        row = cursor.fetchone()

        if row and row[0]:  # Si existe la imagen
            return send_file(io.BytesIO(row[0]), mimetype="image/jpeg")  # Se ajusta el tipo de imagen si es PNG

        return "❌ Imagen no encontrada", 404
    except mysql.connector.Error:
        return "❌ Error al obtener la imagen", 500

if __name__ == "__main__":
    app.run(debug=True)
    
    