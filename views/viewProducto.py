# views/viewProducto.py
from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

# Función para obtener la lista de productos desde la base de datos
def mostrar_lista_productos():
    # Obtener la lista de productos desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT id_producto, nombre, precio FROM productos"
    cursor.execute(consulta)

    productos_tuplas = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Convertir cada tupla en un diccionario con claves adecuadas
    productos = [{'id': producto[0], 'nombre': producto[1],  'precio': producto[2]} for producto in productos_tuplas]

    return productos

# Función para agregar un nuevo producto a la base de datos
def agregar_producto():
    # Lógica para agregar un nuevo producto a la base de datos
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        precio = request.form['precio']


        # Realizar la inserción en la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO productos (nombre,  precio) VALUES (%s, %s)"
        cursor.execute(consulta, (nombre, precio))
        conexion.commit()
        cursor.close()
        conexion.close()

        # Redirigir a la lista de productos después de agregar uno nuevo
        return redirect('/lista_productos')

    # Renderizar el formulario si el método de solicitud es GET
    return render_template('nuevo_producto.html')

# Función para obtener la información de un producto por su ID
def obtener_producto_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT * FROM productos WHERE id_producto = %s"
    cursor.execute(consulta, (id,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    return producto

# Función para eliminar un producto por su ID
def eliminar_producto(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "DELETE FROM productos WHERE id_producto = %s"
    cursor.execute(consulta, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    # Redirigir a la lista de productos después de eliminar uno
    return redirect('/lista_productos')

# Función para guardar los cambios en un producto
def guardar_cambios_producto(id, nombre,  precio):
    # Realizar la actualización en la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "UPDATE productos SET nombre = %s, precio = %s WHERE id_producto = %s"
    cursor.execute(consulta, (nombre, precio, id))
    conexion.commit()
    cursor.close()
    conexion.close()

    # Redirigir a la lista de productos después de guardar los cambios
    return redirect('/lista_productos')

def obtener_lista_nombres_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT nombre FROM productos"
    cursor.execute(consulta)

    nombres_productos = [producto[0] for producto in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return nombres_productos