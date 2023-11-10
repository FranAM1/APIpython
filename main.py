from fastapi.responses import RedirectResponse
import requests
from pathlib import Path
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

class Residuo(BaseModel):
    municipio: str

class Actividad(BaseModel):
    actividad: str

app = FastAPI()

static_dir = Path('./static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
    return RedirectResponse(url="/static/formulario.html", status_code=status.HTTP_302_FOUND)

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

@app.post("/residuos/percentage")
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
        if feature['MUNICIPIO'] == municipio:
            countMunicipio += 1
        allMunicipios += 1


    percentage = countMunicipio / allMunicipios
    
    return percentage



@app.post("/residuos/actividad/percentage")
async def porcentajeActividades(actividad: Actividad):
    percentage = 0
    allActividades = 0
    countActividades = 0
    actividadFiltro = actividad.actividad

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
        if feature['ACTIVIDAD'] == actividadFiltro:
            countActividades += 1
        allActividades += 1


    percentage = countActividades / allActividades
    
    print(percentage)

    return percentage

    
    

    
