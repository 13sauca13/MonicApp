from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
from bson.objectid import ObjectId

app = Flask(__name__)

# Carga variables de entorno
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client.get_database('MonicApp')  # Base de datos MonicApp
ubicaciones_collection = db['ubicaciones']  # Colección ubicaciones
contactos_collection = db['contactos']  # Colección contactos

@app.route('/')
def index():
    return render_template('index.html', documentos=ubicaciones_collection.find())

@app.route('/ubicaciones', methods=['GET', 'POST'])
def ubicaciones():
    if request.method == 'POST':
        # Obtener datos del formulario
        sitio_id = request.form.get('sitio_id')
        latitud = request.form.get('latitud')
        longitud = request.form.get('longitud')
        sitio = {
            'nombre': request.form.get('nombre'),
            'ubicacion': request.form.get('ubicacion'),
            'capacidad': int(request.form.get('capacidad')) if request.form.get('capacidad') else 0,
            'servicios': request.form.get('servicios') or '',
            'contacto': request.form.get('contacto') or '',
            'notas': request.form.get('notas') or ''
        }
        # Añadir coordenadas si se proporcionan
        if latitud and longitud:
            sitio['coordenadas'] = {
                'latitud': float(latitud),
                'longitud': float(longitud)
            }
        
        # Actualizar o insertar
        if sitio_id:
            # Actualizar sitio existente
            ubicaciones_collection.update_one({'_id': ObjectId(sitio_id)}, {'$set': sitio})
        else:
            # Insertar nuevo sitio
            ubicaciones_collection.insert_one(sitio)
        
        return redirect(url_for('ubicaciones'))
    
    # GET: Mostrar todos los sitios
    sitios = ubicaciones_collection.find()
    # Obtener ubicacion_id de la query string (desde contactos)
    ubicacion_id = request.args.get('ubicacion_id')
    if ubicacion_id:
        # Redirigir a la vista de detalle si se proporciona ubicacion_id
        return redirect(url_for('ubicacion_detalle', ubicacion_id=ubicacion_id))
    return render_template('ubicaciones.html', sitios=sitios, sitio=None, sitio_id=None, accordion_open=False)

@app.route('/editar/<sitio_id>')
def editar_sitio(sitio_id):
    # Obtener el sitio para editar
    sitio = ubicaciones_collection.find_one({'_id': ObjectId(sitio_id)})
    sitios = ubicaciones_collection.find()
    return render_template('ubicaciones.html', sitios=sitios, sitio=sitio, sitio_id=sitio_id, accordion_open=True)

@app.route('/eliminar/<sitio_id>', methods=['POST'])
def eliminar_sitio(sitio_id):
    # Eliminar el sitio
    ubicaciones_collection.delete_one({'_id': ObjectId(sitio_id)})
    return redirect(url_for('ubicaciones'))

@app.route('/ubicacion/<ubicacion_id>', methods=['GET', 'POST'])
def ubicacion_detalle(ubicacion_id):
    # Obtener la ubicación
    ubicacion = ubicaciones_collection.find_one({'_id': ObjectId(ubicacion_id)})
    if not ubicacion:
        return "Ubicación no encontrada", 404
    
    if request.method == 'POST':
        # Obtener datos del formulario
        latitud = request.form.get('latitud')
        longitud = request.form.get('longitud')
        ubicacion_data = {
            'nombre': request.form.get('nombre'),
            'ubicacion': request.form.get('ubicacion'),
            'capacidad': int(request.form.get('capacidad')) if request.form.get('capacidad') else 0,
            'servicios': request.form.get('servicios') or '',
            'contacto': request.form.get('contacto') or '',
            'notas': request.form.get('notas') or ''
        }
        # Añadir coordenadas si se proporcionan
        if latitud and longitud:
            ubicacion_data['coordenadas'] = {
                'latitud': float(latitud),
                'longitud': float(longitud)
            }
        # Actualizar ubicación
        ubicaciones_collection.update_one({'_id': ObjectId(ubicacion_id)}, {'$set': ubicacion_data})
        return redirect(url_for('ubicacion_detalle', ubicacion_id=ubicacion_id))
    
    # GET: Mostrar detalles de la ubicación
    return render_template('ubicacion_detail.html', ubicacion=ubicacion, accordion_open=False)

@app.route('/contactos', methods=['GET', 'POST'])
def contactos():
    if request.method == 'POST':
        # Obtener datos del formulario
        contacto_id = request.form.get('contacto_id')
        ubicacion_id = request.form.get('ubicacion_id')
        # Obtener el nombre de la ubicación para almacenarlo
        ubicacion = ubicaciones_collection.find_one({'_id': ObjectId(ubicacion_id)}) if ubicacion_id else None
        contacto = {
            'nombre': request.form.get('nombre'),
            'telefono': request.form.get('telefono') or '',
            'mail': request.form.get('mail') or '',
            'empresa': request.form.get('empresa') or '',
            'ubicacion_id': ObjectId(ubicacion_id) if ubicacion_id else None,
            'ubicacion_nombre': ubicacion['nombre'] if ubicacion else ''
        }
        
        # Actualizar o insertar
        if contacto_id:
            # Actualizar contacto existente
            contactos_collection.update_one({'_id': ObjectId(contacto_id)}, {'$set': contacto})
        else:
            # Insertar nuevo contacto
            contactos_collection.insert_one(contacto)
        
        return redirect(url_for('contactos'))
    
    # GET: Mostrar todos los contactos y ubicaciones para el formulario
    contactos = contactos_collection.find()
    ubicaciones = ubicaciones_collection.find()
    return render_template('contactos.html', contactos=contactos, ubicaciones=ubicaciones, contacto=None, contacto_id=None, accordion_open=False)

@app.route('/editar_contacto/<contacto_id>')
def editar_contacto(contacto_id):
    # Obtener el contacto para editar
    contacto = contactos_collection.find_one({'_id': ObjectId(contacto_id)})
    contactos = contactos_collection.find()
    ubicaciones = ubicaciones_collection.find()
    return render_template('contactos.html', contactos=contactos, ubicaciones=ubicaciones, contacto=contacto, contacto_id=contacto_id, accordion_open=True)

@app.route('/eliminar_contacto/<contacto_id>', methods=['POST'])
def eliminar_contacto(contacto_id):
    # Eliminar el contacto
    contactos_collection.delete_one({'_id': ObjectId(contacto_id)})
    return redirect(url_for('contactos'))

if __name__ == '__main__':
    app.run(debug=True)