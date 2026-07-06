import sqlite3
import hashlib
from flask import Flask, request, render_template_string

app = Flask(__name__)
DB_NAME = "usuarios_examen.db"

def inicializar_base_de_datos():
    """Crea la tabla e inserta los usuarios con sus contraseñas en hash si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Integrantes y contraseñas de ejemplo (se guardarán como Hash)
    # Puedes cambiar 'claveMelissa123' y 'claveJordan123' por las que prefieran
    integrantes = {
        "Melissa": "claveMelissa123",
        "Jordan": "claveJordan123"
    }
    
    for nombre, clave_plana in integrantes.items():
        # Crear el Hash SHA-256 de la contraseña plana
        hash_resultado = hashlib.sha256(clave_plana.encode()).hexdigest()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, hash_resultado))
        except sqlite3.IntegrityError:
            # Si el usuario ya existe en la BD, no lo duplica
            pass
            
    conn.commit()
    conn.close()

def validar_usuario(username, password_plana):
    """Valida si el usuario existe y si el hash de la clave ingresada coincide."""
    hash_ingresado = hashlib.sha256(password_plana.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and resultado[0] == hash_ingresado:
        return True
    return False

# Plantilla HTML básica integrada para no requerir archivos externos en carpetas
HTML_LOGIN = '''
<!DOCTYPE html>
<html>
<head>
    <title>Examen DRY7122 - Login Seguro</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; margin-top: 100px; }
        .login-box { background: white; padding: 30px; display: inline-block; border-radius: 8px; box-shadow: 0px 0px 10px #ccc; }
        input { display: block; margin: 10px auto; padding: 10px; width: 200px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .error { color: red; } .success { color: green; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Inicio de Sesión - Ítem 3</h2>
        <h4>Integrantes: Melissa & Jordan</h4>
        {% if mensaje %}
            <p class="{{ clase_mensaje }}">{{ mensaje }}</p>
        {% endif %}
        <form method="POST">
            <input type="text" name="usuario" placeholder="Nombre de Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Validar Credenciales</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = None
    clase_mensaje = ""
    
    if request.method == 'POST':
        usuario_ingresado = request.form['usuario']
        password_ingresada = request.form['password']
        
        # Validar usando la función respectiva
        if validar_usuario(usuario_ingresado, password_ingresada):
            mensaje = f"✅ ¡Acceso concedido! Bienvenido/a, {usuario_ingresado}."
            clase_mensaje = "success"
        else:
            mensaje = "❌ Credenciales incorrectas. Intente nuevamente."
            clase_mensaje = "error"
            
    return render_template_string(HTML_LOGIN, mensaje=mensaje, clase_mensaje=clase_mensaje)

if __name__ == '__main__':
    # Inicializa la base de datos SQLite de forma local
    inicializar_base_de_datos()
    print("[INFO] Base de datos SQLite inicializada correctamente.")
    print("[INFO] Iniciando servidor web en el puerto 5800...")
    # Ejecuta la app web en el puerto exigido 5800
    app.run(host='0.0.0.0', port=5800, debug=True)
