from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid

app = FastAPI()

# Models
class Program(BaseModel):
    id: str
    name: str

class Client(BaseModel):
    id: str
    name: str
    age: int
    enrolled_programs: List[str] = []

# In-memory databases
programs_db: Dict[str, Program] = {}
clients_db: Dict[str, Client] = {}

# Endpoints

@app.post("/programs/", response_model=Program)
def create_program(name: str):
    program_id = str(uuid.uuid4())
    program = Program(id=program_id, name=name)
    programs_db[program_id] = program
    return program

@app.post("/clients/", response_model=Client)
def register_client(name: str, age: int):
    client_id = str(uuid.uuid4())
    client = Client(id=client_id, name=name, age=age)
    clients_db[client_id] = client
    return client

@app.post("/clients/{client_id}/enroll", response_model=Client)
def enroll_client_in_program(client_id: str, program_ids: List[str]):
    client = clients_db.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for pid in program_ids:
        if pid not in programs_db:
            raise HTTPException(status_code=404, detail=f"Program {pid} not found")
    
    client.enrolled_programs.extend(pid for pid in program_ids if pid not in client.enrolled_programs)
    return client

@app.get("/clients/", response_model=List[Client])
def list_clients():
    return list(clients_db.values())

@app.get("/clients/search/", response_model=Client)
def search_client(name: str):
    for client in clients_db.values():
        if client.name.lower() == name.lower():
            return client
    raise HTTPException(status_code=404, detail="Client not found")

@app.get("/clients/{client_id}", response_model=Client)
def view_client_profile(client_id: str):
    client = clients_db.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
