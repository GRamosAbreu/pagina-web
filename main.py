from fastapi import FastAPI,HTTPException,status
import flet as ft
import flet.fastapi as flet_fastapi
import httpx
from pydantic import BaseModel
from db import db_client
from schema import user_schema, users_schema
from bson import ObjectId
app = FastAPI() 

class User(BaseModel):
    username: str
    contrasena: int 
    

@app.post('/crear-usuario')
async def get_list(user: User):
    user_dict = dict(user)
    if db_client.test.users.find_one({"username":user.username}):
        raise HTTPException(status.HTTP_409_CONFLICT,detail={"error":"usuario en uso"})
    db_client.test.users.insert_one(user_dict)

    return 


@app.get('/usuarios')
async def get_users():
    return users_schema(db_client.test.users.find())

@app.get('/usuario/{id}')
async def get_user(id: str):
    try:
        return user_schema(db_client.test.users.find_one({"_id":ObjectId(id)}))
    except:
        return {"error": "el id introducido es incorrecto"}


@app.delete('/borrar/{id}')
async def borrar(id: str):
    try:
        db_client.test.users.find_one_and_delete({"_id": ObjectId(id)})
    except:
        return {"Error":"no se ha borrado el usuario"}
    
        
    

@app.put('/remplazar')
async def replace(id:str,user:dict):
    db_client.test.users.find_one_and_replace({"_id":ObjectId(id)}, user)
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"mensaje":"se ha remplazado el usuario correctamente"})

def search_users(field: str, value):
    try:
        user = user_schema(db_client.test.users.find_one({field,value}))
        return User(**user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"mensaje":"No se ha encontrado el usuario"})


         

