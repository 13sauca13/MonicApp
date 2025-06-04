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
db = client.get_database('MonicApp')
collection = db['ubicaciones']

@app.route('/')
def index():
    return render_template('index.html', documentos=collection.find())

@app.route('/ubicaciones', methods=['GET', 'POST'])
def ubicaciones():
    if request.method == 'POST':
        # Obtener datos del formulario
        sitio_id = request.form.get('sitio_id')
        sitio = {
            'nombre': request.form.get('nombre'),
            'ubicacion': request.form.get('ubicacion'),
            'capacidad': int(request.form.get('capacidad')) if request.form.get('capacidad') else 0,
            'servicios': request.form.get('servicios') or '',
            'contacto': request.form.get('contacto') or '',
            'notas': request.form.get('notas') or ''
        }
        
        # Actualizar o insertar
        if sitio_id:
            # Actualizar sitio existente
            collection.update_one({'_id': ObjectId(sitio_id)}, {'$set': sitio})
        else:
            # Insertar nuevo sitio
            collection.insert_one(sitio)
        
        return redirect(url_for('ubicaciones'))
    
    # GET: Mostrar todos los sitios
    sitios = collection.find()
    return render_template('ubicaciones.html', sitios=sitios, sitio=None, sitio_id=None, accordion_open=False)

@app.route('/editar/<sitio_id>')
def editar_sitio(sitio_id):
    # Obtener el sitio para editar
    sitio = collection.find_one({'_id': ObjectId(sitio_id)})
    sitios = collection.find()
    return render_template('ubicaciones.html', sitios=sitios, sitio=sitio, sitio_id=sitio_id, accordion_open=True)

@app.route('/eliminar/<sitio_id>', methods=['POST'])
def eliminar_sitio(sitio_id):
    # Eliminar el sitio
    collection.delete_one({'_id': ObjectId(sitio_id)})
    return redirect(url_for('ubicaciones'))

if __name__ == '__main__':
    app.run(debug=True)