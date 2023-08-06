from flask import render_template, request, redirect
from controllers.conexion import conectar_bd

# Función para obtener la lista de marcas desde la base de datos
def mostrar_lista_marca():
    # Obtener la lista de marcas desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT id_marca, marca FROM marca"
    cursor.execute(consulta)

    marcas_tuplas = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Convertir cada tupla en un diccionario con claves adecuadas
    marcas = [{'id_marca': marca[0], 'marca': marca[1]} for marca in marcas_tuplas]

    return marcas

# Función para agregar una nueva marca a la base de datos
def agregar_marca():
    # Lógica para agregar una nueva marca a la base de datos
    if request.method == 'POST':
        # Obtener los datos del formulario
        marca = request.form['marca']

        # Realizar la inserción en la base de datos
        conexion = conectar_bd()
        cursor = conexion.cursor()
        consulta = "INSERT INTO marca (marca) VALUES (%s)"
        cursor.execute(consulta, (marca,))
        conexion.commit()
        cursor.close()
        conexion.close()

        # Redirigir a la lista de marcas después de agregar una nueva
        return redirect('/lista_marca')

    # Renderizar el formulario si el método de solicitud es GET
    return render_template('nueva_marca.html')

# Función para obtener la información de una marca por su ID
def obtener_marca_por_id(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT * FROM marca WHERE id_marca = %s"
    cursor.execute(consulta, (id,))
    marca = cursor.fetchone()

    cursor.close()
    conexion.close()

    return marca

# Función para eliminar una marca por su ID
def eliminar_marca(id):
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "DELETE FROM marca WHERE id_marca = %s"
    cursor.execute(consulta, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    # Redirigir a la lista de marcas después de eliminar una
    return redirect('/lista_marca')

# Función para guardar los cambios en una marca
def guardar_cambios_marca(id, marca):
    # Realizar la actualización en la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = "UPDATE marca SET marca = %s WHERE id_marca = %s"
    cursor.execute(consulta, (marca, id))
    conexion.commit()
    cursor.close()
    conexion.close()

    # Redirigir a la lista de marcas después de guardar los cambios
    return redirect('/lista_marca')

def obtener_lista_nombres_marcas():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    consulta = "SELECT marca FROM marca"
    cursor.execute(consulta)

    nombres_marcas = [marca[0] for marca in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return nombres_marcas