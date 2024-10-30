from fastapi import FastAPI, Request
import uvicorn
import requests

app = FastAPI()


##Routes
@app.get('/')
def home_route():
    return {"msg":"This route works"}

@app.post('/model')
async def model_route(request: Request):
    form_data = await request.json()
    model_api = "https://roomstop-modelapi-production.up.railway.app/model"
    response = requests.post(model_api, json = form_data)
    return response.json()



if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=4000)



