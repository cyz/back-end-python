from fastapi import FastAPI, HTTPException
from uuid import UUID
from typing import List
from models import UserBase, UserCreate, UserUpdate, Role

app = FastAPI()

db: List[UserBase] = [
    UserCreate(
        id=UUID("caad4458-72e3-4703-adce-c9fe80ffe723"),
        first_name="Ana", 
        last_name="Maria", 
        email="email@gmail.com",
        role=[Role.role_1]
    ),
    UserCreate(
        id=UUID("cbc7d7e4-89a9-4bcb-ac77-564ee3c466c5"),
        first_name="Cynthia", 
        last_name="Zanoni", 
        email="email@gmail.com",
        role=[Role.role_2]
    ),
    UserCreate(
        id=UUID("dacbc6b5-d88a-4ec7-a8c1-2312282bb347"),
        first_name="Camila", 
        last_name="Silva", 
        email="email@gmail.com",
        role=[Role.role_3]
    )
]

@app.get("/api/users")
async def get_users():
    return db;

@app.get("/api/users/{id}")
async def get_user(id: UUID):
    for user in db:
        if user.id == id:
            return user
    return {"message": "Usuário não encontrado!"}

@app.post("/api/users")
async def create_user(user: UserCreate):
    db.append(user)
    return user

@app.delete("/api/users/{id}")
async def delete_user(id: UUID):
    for user in db:
        if user.id == id:
            db.remove(user)
            return {"message": "Usuário removido com sucesso!"}
    return {"message": "Usuário não encontrado!"}