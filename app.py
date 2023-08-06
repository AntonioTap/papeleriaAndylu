#app.py
from flask import Flask, render_template, redirect, request, url_for, session
from views.viewUsuario import mostrar_lista_usuarios, agregar_usuario, eliminar_usuario, obtener_usuario_por_id, guardar_cambios_usuario
from views.viewCategoria import mostrar_lista_categoria, agregar_categoria, obtener_categoria_por_id, eliminar_categoria, guardar_cambios_categoria
from views.viewProducto import mostrar_lista_productos, agregar_producto, obtener_producto_por_id, eliminar_producto, guardar_cambios_producto
from views.viewMarca import agregar_marca, mostrar_lista_marca, guardar_cambios_marca, eliminar_marca
from controllers.conexion import validar_credenciales

app = Flask(__name__)

# Configuración para utilizar sesiones
app.secret_key = 'mi_clave_secreta'

# Rutas y lógica de la aplicación
@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        resultado = validar_credenciales(correo, contraseña)

        if resultado:
            id_rol = resultado[0]
            if id_rol == 1:  # Si el rol es 1, redirigir a la página del administrador
                session['rol'] = 'administrador'
                return redirect('/admin')
            elif id_rol == 2:  # Si el rol es 2, redirigir a la página del cajero
                session['rol'] = 'cajero'
                return redirect('/cajero')

    # Renderizar el formulario si el método de solicitud es GET
    return render_template('login.html')

@app.route('/admin')
def admin():
    # Verificar si el usuario tiene permiso para acceder a la página de administrador
    if 'rol' in session and session['rol'] == 'administrador':
        return render_template('admin.html')
    else:
        return redirect('/login')


#usuarios
@app.route('/nuevo_usuario', methods=['GET', 'POST'])
def nuevo_usuario():
    return agregar_usuario()

#lista usuarios
@app.route('/lista_usuarios')
def lista_usuarios():
    usuarios = mostrar_lista_usuarios()  # Obtener la lista de usuarios desde la función de vista
    return render_template('lista_usuarios.html', usuarios=usuarios)

#editar usuarios
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario_route(id):
    usuario = obtener_usuario_por_id(id)
    
    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        apet_pat = request.form['apet_pat']
        ape_mat = request.form['ape_mat']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        id_rol = request.form['id_rol']

        # Llamar a la función para guardar los cambios en el usuario
        guardar_cambios_usuario(id, nombre, apet_pat, ape_mat, telefono, direccion, correo, contraseña, id_rol)
        return redirect('/lista_usuarios')

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario_route(id):
    if 'rol' in session and session['rol'] == 'administrador':
        return eliminar_usuario(id)
    else:
        return redirect('/login') 


# Rutas y lógica para la tabla "productos"
@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    return agregar_producto() 

@app.route('/lista_productos')
def lista_productos():
    productos = mostrar_lista_productos()
    return render_template('lista_productos.html', productos=productos)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto_route(id):
    producto = obtener_producto_por_id(id)
    
    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        precio = request.form['precio']

        # Llamar a la función para guardar los cambios en el producto
        guardar_cambios_producto(id, nombre, precio)
        return redirect('/lista_productos')

    return render_template('editar_producto.html', producto=producto) 

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto_route(id):
    return eliminar_producto(id)


@app.route('/nueva_marca', methods=['GET', 'POST'])
def nueva_marca():
    return agregar_marca() 

@app.route('/lista_marca')
def lista_marca():
    marca = mostrar_lista_marca()
    return render_template('lista_marca.html', marca=marca)

@app.route('/editar_marca/<int:id>', methods=['GET', 'POST'])
def editar_marca_route(id):
    marca= obtener_categoria_por_id(id)

    if request.method == 'POST':
        marca = request.form['marca']
        guardar_cambios_marca(id, marca)
        return redirect('/lista_marca')
    
    return render_template ('editar_marca.html', marca=marca)

@app.route('/eliminar_marca/<int:id>')
def eliminar_marca_route(id):
    return eliminar_marca(id)
    

@app.route('/nueva_categoria', methods=['GET', 'POST'])
def nueva_categoria():
    return agregar_categoria()

@app.route('/lista_categorias')
def lista_categorias():
    categorias = mostrar_lista_categoria()
    return render_template('lista_categorias.html', categorias=categorias)

# Editar Categoria
@app.route('/editar_categoria/<int:id>', methods=['GET', 'POST'])
def editar_categoria_route(id):
    categoria = obtener_categoria_por_id(id)
    
    if request.method == 'POST':
        # Obtener los valores del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        proveedor = request.form['proveedor']

        # Llamar a la función para guardar los cambios en la categoría
        guardar_cambios_categoria(id, nombre, descripcion, proveedor)
        return redirect('/lista_categorias')

    return render_template('editar_categoria.html', categoria=categoria)

@app.route('/eliminar_categoria/<int:id>')
def eliminar_categoria_route(id):
    return eliminar_categoria(id)


# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    # Lógica para cerrar sesión
    session.clear()
    return redirect(url_for('inicio'))

#cajero
@app.route('/cajero')
def cajero():
    # Verificar si el usuario tiene permiso para acceder a la página del cajero
    if 'rol' in session and session['rol'] == 'cajero':
        return render_template('cajero.html')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
