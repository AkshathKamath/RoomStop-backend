from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import certifi
import requests
import uvicorn
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
import json

app = FastAPI()

origins = [
    "http://localhost:3000",  # For local development
    "https://your-react-app.com",  # Deployed React app URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

##Routes
@app.get('/')
def home_route():
    return {"msg":"This route works"}

@app.get('/rooms/getapartments')
async def list_apartments():
    db = client[db_name]
    rooms = db[collection_room]
    return dumps(rooms.find())

@app.post('/rooms/shortlistapartments')
async def shortlist_apartments(apartment_id, user_id):
    db = client[db_name]
    rooms = db[collection_room]
    room_shortlist =  json.loads(dumps(rooms.find_one({'Apartment_ID': int(apartment_id)})))
    room_shortlist.update({'_id': ObjectId(room_shortlist['_id']['$oid']), 'shortlister': int(user_id)})
    userrooms = db[collection_room_users]
    userrooms.insert_one(room_shortlist)

@app.delete('/rooms/deleteapartment')
async def delete_apartments(apartment_id, user_id):
    db = client[db_name]
    userrooms = db[collection_room_users]
    userrooms.find_one_and_delete({'Apartment_ID': int(apartment_id), "shortlister": int(user_id)})

@app.post('/model')
async def model_route(request: Request):
    form_data = await request.json()
    model_api = "https://roomstop-modelapi-production.up.railway.app/model"
    response = requests.post(model_api, json = form_data)
    return response.json()

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=4000)



