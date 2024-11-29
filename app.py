from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
import certifi
import requests
import uvicorn
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
import json

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],
)

uri = "mongodb+srv://rohitprabhu:roomstop123@roomstopcluster.w3zqf.mongodb.net/?retryWrites=true&w=majority&appName=RoomStopCluster"
db_name = "roomstop"
collection_room = "rooms"
collection_users = "users"
collection_room_users = 'userrooms'

# client connection
client = MongoClient(uri, tlsCAFile=certifi.where())

class House(BaseModel):
    apartment_id: int

##Routes
@app.get('/')
def home_route():
    return {"msg":"This route works"}

@app.get('/rooms/getapartments')
async def list_apartments():
    db = client[db_name]
    rooms = db[collection_room]
    return dumps(rooms.find())

@app.get('/rooms/show_shortlisted_apartments')
async def list_shortlisted_apartments():
    db = client[db_name]
    rooms = db[collection_room_users]
    return dumps(rooms.find())

@app.post('/rooms/shortlistapartments')
async def shortlist_apartments(house: House = Body(...)):
    db = client[db_name]
    rooms = db[collection_room]
    room_shortlist =  json.loads(dumps(rooms.find_one({'Apartment_ID': house.apartment_id})))
    room_shortlist.update({'_id': ObjectId(room_shortlist['_id']['$oid'])})
    userrooms = db[collection_room_users]
    userrooms.insert_one(room_shortlist)
    return {"msg":"Room Added Successfully!"}

@app.delete('/rooms/deleteapartment')
async def delete_apartments(house: House = Body(...)):
    db = client[db_name]
    userrooms = db[collection_room_users]
    userrooms.find_one_and_delete({'Apartment_ID': house.apartment_id})
    return {"msg":"Room Deleted Successfully!"}

@app.post('/model')
async def model_route(request: Request):
    form_data = await request.json()
    model_api = "https://roomstop-modelapi-production.up.railway.app/model"
    response = requests.post(model_api, json = form_data)
    return response.json()

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=4000)



