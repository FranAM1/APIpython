import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Residuo(BaseModel):
    municipio: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


API_URL = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/ResiduosPeligrosos/FeatureServer/0/query"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/residuos")
async def residuos():
    params = {
        'where': '1=1',
        'outFields': '*',
        'outSR': '4326',
        'f': 'json'
    }
    
    response = requests.get(API_URL, params = params)
    data = response.json()

    features = data['features']

    return features
    



@app.post("/residuos")
async def residuosMunicipio(residuo: Residuo):
    municipio = residuo.municipio

    params = {
        'where': f"municipio = '{municipio}'",
        'outFields': '*',
        'outSR': '4326',
        'f': 'json'
    }

    response = requests.get(API_URL, params = params)
    data = response.json()

    features = data['features']
    parsed_features = []

    for feature in features:
        parsed_features.append(feature['attributes'])

    return parsed_features

@app.post("/residuos/porcentage")
async def porcentajeResiduos(residuo: Residuo):
    percentage = 0
    allMunicipios = 0
    countMunicipio = 0
    municipio = residuo.municipio

    params = {
        'where': '1=1',
        'outFields': '*',
        'outSR': '4326',
        'f': 'json'
    }

    response = requests.get(API_URL, params = params)
    data = response.json()

    features = data['features']
    parsed_features = []

    for feature in features:
        parsed_features.append(feature['attributes'])
    
    for feature in parsed_features:
        if feature['municipio'] == municipio:
            countMunicipio += 1
        allMunicipios += 1


    percentage = countMunicipio / allMunicipios
    
    return percentage

    
    

    
