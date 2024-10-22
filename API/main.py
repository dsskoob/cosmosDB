from fastapi import FastAPI, HTTPException
from azure.cosmos import exceptions
from database import container

app = FastAPI(title='CRUD FastAPI')

@app.get('/')
def home():
    return "Mi primera api con FastAPI"

@app.post('/productos/',status_code=201)
def crear_producto(producto: dict):
    try:
        # insertar elemento
        container.create_item(body=producto, pre_trigger_include='validarDatos')
        return 'Item creado correctamente'
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail="El producto ya existe")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.get('/productos/{producto_id}')
def obtener_producto(producto_id:str,categoria:str):
    try:
        producto = container.read_item(item=producto_id, partition_key=categoria)
        return producto
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.get('/productos/')
def obtener_lista_productos():
    try:
        script = 'select * from c'
        items = list(container.query_items(script,enable_cross_partition_query=True))
        return items
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="No contiene productos")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.put('/productos/{producto_id}')
def actualizar_producto(producto_id:str,categoria:str, producto: dict):
    try:
        item = container.read_item(item=producto_id, partition_key=categoria)
        
        producto['id'] = producto_id
        producto['categoria'] = categoria

        update_item = container.replace_item(item=producto_id, body=producto)
        return update_item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
 

@app.delete('/productos/{producto_id}')
def elimina_producto(producto_id:str,categoria:str):
    try:
        container.delete_item(item=producto_id, partition_key=categoria)
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail= str(e))
    