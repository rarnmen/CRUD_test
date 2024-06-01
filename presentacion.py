from flask import Flask, jsonify, request
from uses_case import OrdenCasoUso, EstadoCasoUso
from repositories import RepositorioOrdenPostgres, RepositorioOrdenEstadoPostgres
from entities import Orden, OrdenEstado
from trigger_dags import trigger_dag

app = Flask(__name__)

repo_orden = RepositorioOrdenPostgres()
repo_estado = RepositorioOrdenEstadoPostgres()

orden_caso_uso = OrdenCasoUso(repo_orden)
estado_caso_uso = EstadoCasoUso(repo_estado)



@app.route('/orden/create', methods=['POST'])
def crear_orden():
    data = request.json
    orden = Orden(**data)
    nueva_orden = orden_caso_uso.crear_orden(orden)
    try:
        trigger_dag('etl', nueva_orden.id)
    except Exception as e:
        print(e)
    return jsonify(nueva_orden.__dict__)

@app.route('/orden/eliminar', methods=['GET'])
def eliminar_orden():
    id = request.args.get('id')
    eliminado = orden_caso_uso.eliminar_orden(id)
    print(trigger_dag('etl'))
    return {'data': eliminado}

@app.route('/orden/list', methods=['GET'])
def orden_list():
    list_ = orden_caso_uso.ordenes()
    return jsonify({'data':list_})

@app.route('/orden/actualizar', methods=['POST'])
def actualizar_orden():
    data = request.json
    orden = Orden(**data)
    update = orden_caso_uso.actualizar_orden(orden)
    return jsonify(update.__dict__)

@app.route('/orden/estado/actualizar', methods=['POST'])
def actualizar_estado():
    data = request.json
    estado = OrdenEstado(**data)
    update = estado_caso_uso.actualizar_estado(estado)
    return jsonify(update.__dict__)




if __name__ == '__main__':
    app.run(debug=True)